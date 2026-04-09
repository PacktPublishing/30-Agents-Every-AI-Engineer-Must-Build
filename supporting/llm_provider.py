"""
Multi-provider LLM support for all chapters.
Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)

Provides:
    - detect_provider(): Auto-detect which API keys are available
    - get_llm(): Return a LangChain-compatible chat model for any provider
    - get_client(): Return a raw API client for direct-access chapters
    - PROVIDER_MODELS: Default model names per provider

Supported providers: openai, anthropic, google
Fallback: Simulation Mode (MockLLM) when no API key is found.

Usage in notebooks:
    from supporting.llm_provider import detect_provider, get_llm

    provider, api_key, mode = detect_provider()
    llm = get_llm(provider=provider)  # Returns ChatOpenAI, ChatAnthropic, or ChatGoogleGenerativeAI
"""

import os
import sys

# ============================================================
# Default model names per provider
# ============================================================

PROVIDER_MODELS = {
    "openai": {
        "default": "gpt-4o",
        "fast": "gpt-4o-mini",
        "legacy": "gpt-3.5-turbo",
    },
    "anthropic": {
        "default": "claude-sonnet-4-20250514",
        "fast": "claude-haiku-4-5-20251001",
        "legacy": "claude-sonnet-4-20250514",
    },
    "google": {
        "default": "gemini-2.0-flash",
        "fast": "gemini-2.0-flash",
        "legacy": "gemini-1.5-flash",
    },
}

# Map of env var → provider name
_PROVIDER_ENV_KEYS = {
    "OPENAI_API_KEY": "openai",
    "ANTHROPIC_API_KEY": "anthropic",
    "GOOGLE_API_KEY": "google",
}


# ============================================================
# Provider Detection
# ============================================================

def detect_provider(preferred=None):
    """Detect which LLM provider to use based on available API keys.

    Resolution order:
        1. LLM_PROVIDER env var (explicit override)
        2. preferred parameter (caller preference)
        3. First available key: OPENAI → ANTHROPIC → GOOGLE
        4. Simulation Mode (no key found)

    Args:
        preferred: Optional provider name ("openai", "anthropic", "google").

    Returns:
        tuple: (provider_name, api_key_or_None, mode)
            provider_name: "openai", "anthropic", "google", or "simulation"
            api_key: The API key string, or None for simulation
            mode: "LIVE" or "SIMULATION"
    """
    # Load .env if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Check explicit override
    explicit = os.getenv("LLM_PROVIDER", "").strip().lower()
    if explicit and explicit != "auto":
        key_var = f"{explicit.upper()}_API_KEY" if explicit != "google" else "GOOGLE_API_KEY"
        if explicit == "openai":
            key_var = "OPENAI_API_KEY"
        elif explicit == "anthropic":
            key_var = "ANTHROPIC_API_KEY"
        key = _get_valid_key(key_var)
        if key:
            return explicit, key, "LIVE"
        print(f"[WARNING] LLM_PROVIDER={explicit} but {key_var} not set. Falling back.")

    # Check preferred provider
    if preferred:
        preferred = preferred.lower()
        for env_var, provider in _PROVIDER_ENV_KEYS.items():
            if provider == preferred:
                key = _get_valid_key(env_var)
                if key:
                    return provider, key, "LIVE"

    # Auto-detect: first available key wins
    for env_var, provider in _PROVIDER_ENV_KEYS.items():
        key = _get_valid_key(env_var)
        if key:
            return provider, key, "LIVE"

    # Interactive prompt (TTY only)
    if sys.stdin and sys.stdin.isatty():
        try:
            import getpass
            key = getpass.getpass(
                "Enter API key (OpenAI/Anthropic/Google) or press Enter for Simulation: "
            )
            if key and key.strip():
                provider = _guess_provider_from_key(key.strip())
                return provider, key.strip(), "LIVE"
        except (EOFError, OSError):
            pass

    return "simulation", None, "SIMULATION"


def _get_valid_key(env_var):
    """Return the key from env_var if it's set and not a placeholder."""
    key = os.getenv(env_var, "").strip()
    if not key:
        return None
    if any(p in key.lower() for p in ["your-key", "your_key", "xxx", "placeholder"]):
        return None
    return key


def _guess_provider_from_key(key):
    """Guess provider from key prefix pattern."""
    if key.startswith("sk-"):
        return "openai"
    elif key.startswith("sk-ant-"):
        return "anthropic"
    else:
        return "openai"  # default assumption


# ============================================================
# LangChain Chat Model Factory
# ============================================================

def get_llm(provider="openai", model=None, api_key=None, temperature=0, **kwargs):
    """Return a LangChain-compatible chat model for the specified provider.

    Args:
        provider: "openai", "anthropic", or "google"
        model: Model name override. If None, uses PROVIDER_MODELS default.
        api_key: API key override. If None, reads from environment.
        temperature: Model temperature (default 0 for deterministic output).
        **kwargs: Additional kwargs passed to the model constructor.

    Returns:
        A LangChain BaseChatModel instance.

    Raises:
        ImportError: If the provider's LangChain package is not installed.
        ValueError: If provider is not recognized.
    """
    if provider == "simulation":
        raise ValueError(
            "Cannot create LLM for simulation mode. Use MockLLM instead."
        )

    model = model or PROVIDER_MODELS.get(provider, {}).get("default")

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            **kwargs,
        )

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model,
            temperature=temperature,
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
            **kwargs,
        )

    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=api_key or os.getenv("GOOGLE_API_KEY"),
            **kwargs,
        )

    else:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Supported: openai, anthropic, google"
        )


# ============================================================
# Raw Client Factory (for direct-API chapters)
# ============================================================

def get_client(provider="openai", api_key=None):
    """Return a raw API client for the specified provider.

    For chapters that use the OpenAI client directly (1, 8, 15) rather
    than LangChain wrappers.

    Args:
        provider: "openai", "anthropic", or "google"
        api_key: API key override.

    Returns:
        Provider-specific client object.
    """
    if provider == "openai":
        from openai import OpenAI
        return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    elif provider == "anthropic":
        import anthropic
        return anthropic.Anthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
        )

    elif provider == "google":
        import google.generativeai as genai
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        return genai

    else:
        raise ValueError(f"Unknown provider: {provider}")


# ============================================================
# Chat Completion Adapter (normalizes responses across providers)
# ============================================================

def chat_completion(client, provider, messages, model=None, temperature=0):
    """Send a chat completion request and return the response text.

    Normalizes the different response formats across OpenAI, Anthropic,
    and Google into a single string return.

    Args:
        client: Provider client from get_client().
        provider: "openai", "anthropic", or "google".
        messages: List of {"role": ..., "content": ...} dicts.
        model: Model name override.
        temperature: Model temperature.

    Returns:
        str: The assistant's response text.
    """
    model = model or PROVIDER_MODELS.get(provider, {}).get("default")

    if provider == "openai":
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content

    elif provider == "anthropic":
        # Anthropic separates system message from user messages
        system_msg = None
        user_messages = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                user_messages.append(m)

        kwargs = {"model": model, "messages": user_messages, "max_tokens": 4096, "temperature": temperature}
        if system_msg:
            kwargs["system"] = system_msg

        response = client.messages.create(**kwargs)
        return response.content[0].text

    elif provider == "google":
        # Google Gemini uses a different conversation format
        genai_model = client.GenerativeModel(model)
        # Convert messages to Gemini format
        prompt_parts = []
        for m in messages:
            prompt_parts.append(f"{m['role']}: {m['content']}")
        response = genai_model.generate_content("\n".join(prompt_parts))
        return response.text

    else:
        raise ValueError(f"Unknown provider: {provider}")


# ============================================================
# Display Utilities
# ============================================================

def print_provider_banner(provider, mode, model=None):
    """Print a colored banner showing the active provider and mode."""
    model = model or PROVIDER_MODELS.get(provider, {}).get("default", "N/A")
    banner = "=" * 60
    if mode == "LIVE":
        color = "\033[92m"  # green
        print(f"\n{color}\033[1m{banner}")
        print(f"   LIVE MODE — Provider: {provider.upper()}")
        print(f"   Model: {model}")
        print(f"{banner}\033[0m\n")
    else:
        color = "\033[93m"  # yellow
        print(f"\n{color}\033[1m{banner}")
        print(f"   SIMULATION MODE ACTIVE")
        print(f"   Using MockLLM — no API key required")
        print(f"{banner}\033[0m\n")
