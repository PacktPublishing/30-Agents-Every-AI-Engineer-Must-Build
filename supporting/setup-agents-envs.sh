#!/usr/bin/env bash
# =============================================================================
# setup-agents-envs.sh
# Master Environment Setup for: 30 Agents Every AI Engineer Must Build
# Author: Imran Ahmad — auto-generated workflow
# =============================================================================
set -euo pipefail

REPO_DIR="${1:-$(pwd)/30-Agents-Every-AI-Engineer-Must-Build}"
VENVS_DIR="$HOME/.venvs/agents"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[  OK]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

# ── 0. Preflight checks ─────────────────────────────────────────────────────
info "Preflight checks..."

command -v "$PYTHON_BIN" >/dev/null 2>&1 || fail "$PYTHON_BIN not found. Install it first."
PY_VER=$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
[[ "$PY_MAJOR" -ge 3 && "$PY_MINOR" -ge 10 ]] || fail "Python 3.10+ required (found $PY_VER)"
ok "Python $PY_VER detected at $(command -v $PYTHON_BIN)"

# ── 1. System packages (Ubuntu) ─────────────────────────────────────────────
info "Installing system prerequisites..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
    build-essential \
    python3-dev \
    python3-venv \
    python3-pip \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    git \
    curl \
    jq \
    2>/dev/null
ok "System packages installed"

# ── 2. Clone repo (if not present) ──────────────────────────────────────────
if [ ! -d "$REPO_DIR" ]; then
    info "Cloning repository..."
    git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git "$REPO_DIR"
    ok "Repository cloned to $REPO_DIR"
else
    ok "Repository already exists at $REPO_DIR"
fi

# ── 3. Create venvs directory ───────────────────────────────────────────────
mkdir -p "$VENVS_DIR"
ok "Venvs root: $VENVS_DIR"

# ── Helper: create venv + install ────────────────────────────────────────────
create_env() {
    local name="$1"
    local req_file="$2"
    local env_path="$VENVS_DIR/$name"

    if [ -d "$env_path" ]; then
        warn "Venv '$name' already exists — skipping (delete it to rebuild)"
        return 0
    fi

    info "Creating venv: $name"
    "$PYTHON_BIN" -m venv "$env_path"
    source "$env_path/bin/activate"
    pip install --upgrade pip setuptools wheel -q
    pip install -r "$req_file" -q
    # Register Jupyter kernel for this env
    python -m ipykernel install --user --name "$name" --display-name "Python ($name)"
    deactivate
    ok "Venv '$name' ready  →  source $env_path/bin/activate"
}

# ── 4. Generate consolidated requirements files ─────────────────────────────
REQ_DIR="$REPO_DIR/.envs"
mkdir -p "$REQ_DIR"

# --- agents-foundation (Ch01, 04, 05, 07, 08, 15, 17) ---
cat > "$REQ_DIR/agents-foundation.txt" << 'EOF'
# agents-foundation — Chapters 01, 04, 05, 07, 08, 15, 17
# Lightweight: openai + standard data science, no LangChain
openai>=1.40.0,<2.0.0
python-dotenv>=1.0.1
numpy>=1.26.0,<2.1
pandas>=2.2.0,<3.0
matplotlib>=3.9.0,<4.0
statsmodels>=0.14.0,<1.0
tenacity>=9.1.0
httpx>=0.28.0
networkx==3.3
dataclasses-json>=0.6.0,<1.0
scipy>=1.12.0,<2.0
jupyter>=1.0.0
notebook>=7.2.0
ipykernel>=6.29.0
EOF

# --- agents-langchain-modern (Ch03, 09, 12) ---
cat > "$REQ_DIR/agents-langchain-modern.txt" << 'EOF'
# agents-langchain-modern — Chapters 03, 09, 12
# LangChain 0.3.x + LangGraph 0.3.x + XAI
langchain>=0.3.0,<0.4.0
langchain-core>=0.3.0,<0.4.0
langchain-openai>=0.3.0,<0.4.0
langgraph>=0.3.0,<0.4.0
openai>=1.40.0,<2.0.0
pydantic>=2.7.0,<3.0.0
python-dotenv>=1.0.1
typing-extensions>=4.9.0
shap>=0.45.1,<0.47.0
lime>=0.2.0.1,<0.3.0
scikit-learn>=1.5.0,<1.7.0
numpy>=1.26.4,<2.1.0
pandas>=2.1.0,<2.4.0
matplotlib>=3.8.0,<3.11.0
seaborn>=0.13.0,<0.15.0
jupyter>=1.0.0
ipykernel>=6.29.0
EOF

# --- agents-rag-research (Ch06, 13) ---
cat > "$REQ_DIR/agents-rag-research.txt" << 'EOF'
# agents-rag-research — Chapters 06, 13
# LangChain 0.3 + PyTorch/transformers + RAG + healthcare
langchain>=0.3.0,<0.4.0
langchain-core>=0.3.0,<0.4.0
langchain-openai>=0.3.0,<0.4.0
langchain-community>=0.3.0,<0.4.0
langchain-text-splitters>=0.3.0
faiss-cpu>=1.9.0
sentence-transformers>=3.3.0
transformers>=4.40.0,<5.0
nltk>=3.9.0
scikit-learn>=1.5.0
arxiv>=2.1.0
Pillow>=10.4.0
pytesseract>=0.3.13
pdf2image>=1.17.0
rapidfuzz>=3.10.0
fhir.resources>=7.0,<8.0
aiohttp>=3.9,<4.0
nest-asyncio>=1.6,<2.0
scipy>=1.12,<2.0
numpy>=1.26.0,<2.1
pandas>=2.2.0
python-dotenv>=1.0.1
jupyter>=1.0.0
ipykernel>=6.29.0
EOF

# --- agents-legacy-conversational (Ch10) ---
cat > "$REQ_DIR/agents-legacy-conversational.txt" << 'EOF'
# agents-legacy-conversational — Chapter 10
# Pinned LangChain 0.2.16
langchain==0.2.16
langchain-openai==0.1.23
langchain-community==0.2.16
langchain-core==0.2.38
openai==1.40.0
faiss-cpu==1.8.0
numpy>=1.24.0,<2.0.0
tiktoken>=0.7.0
python-dotenv==1.0.1
jupyter>=1.0.0
ipykernel>=6.29.0
EOF

# --- agents-legacy-finance (Ch14) ---
cat > "$REQ_DIR/agents-legacy-finance.txt" << 'EOF'
# agents-legacy-finance — Chapter 14
# Pinned LangChain 0.2.16 + LangGraph 0.2.28 + financial data
langchain==0.2.16
langchain-openai==0.1.23
langchain-community==0.2.16
langgraph==0.2.28
openai==1.40.0
pydantic==2.8.2
numpy==1.26.4
yfinance==0.2.41
finnhub-python==2.4.19
tavily-python==0.3.3
python-dotenv==1.0.1
jupyter>=1.0.0
ipykernel>=6.29.0
EOF

# --- agents-legacy-embodied (Ch16) ---
cat > "$REQ_DIR/agents-legacy-embodied.txt" << 'EOF'
# agents-legacy-embodied — Chapter 16
# Pinned LangChain 0.2.16 + LangGraph 0.1.4
langchain==0.2.16
langchain-openai==0.1.23
langchain-core>=0.2.38,<0.3.0
langgraph==0.1.4
openai==1.40.0
pydantic==2.8.2
python-dotenv==1.0.1
jupyter>=1.0.0
ipykernel>=6.29.0
EOF

# --- agents-multimodal (Ch11 — GPU only, optional) ---
cat > "$REQ_DIR/agents-multimodal.txt" << 'EOF'
# agents-multimodal — Chapter 11 (GPU/Live mode only)
# Skip this if running simulation mode — use agents-foundation instead
numpy>=1.24.0,<2.0
Pillow>=10.0.0
python-dotenv>=1.0.0
torch>=2.2.0
transformers>=4.40.0
accelerate>=0.28.0
jupyter>=1.0.0
ipykernel>=6.29.0
EOF

ok "Consolidated requirements written to $REQ_DIR/"

# ── 5. Build all environments ───────────────────────────────────────────────
info "Building environments (this may take several minutes)..."
echo ""

create_env "agents-foundation"            "$REQ_DIR/agents-foundation.txt"
create_env "agents-langchain-modern"      "$REQ_DIR/agents-langchain-modern.txt"
create_env "agents-rag-research"          "$REQ_DIR/agents-rag-research.txt"
create_env "agents-legacy-conversational" "$REQ_DIR/agents-legacy-conversational.txt"
create_env "agents-legacy-finance"        "$REQ_DIR/agents-legacy-finance.txt"
create_env "agents-legacy-embodied"       "$REQ_DIR/agents-legacy-embodied.txt"

# Optional GPU env — only if CUDA is available
if command -v nvidia-smi >/dev/null 2>&1; then
    info "CUDA GPU detected — building agents-multimodal"
    create_env "agents-multimodal" "$REQ_DIR/agents-multimodal.txt"
else
    warn "No CUDA GPU detected — skipping agents-multimodal (Ch11 will use agents-foundation in sim mode)"
fi

# ── 6. Generate the convenience switcher ─────────────────────────────────────
SWITCHER="$REPO_DIR/activate-chapter.sh"
cat > "$SWITCHER" << 'SWITCHER_EOF'
#!/usr/bin/env bash
# activate-chapter.sh — Quick venv switcher for each chapter
# Usage: source activate-chapter.sh <chapter_number>
#   e.g. source activate-chapter.sh 9

VENVS_DIR="$HOME/.venvs/agents"

declare -A CHAPTER_MAP=(
    [1]="agents-foundation"
    [2]="agents-foundation"
    [3]="agents-langchain-modern"
    [4]="agents-foundation"
    [5]="agents-foundation"
    [6]="agents-rag-research"
    [7]="agents-foundation"
    [8]="agents-foundation"
    [9]="agents-langchain-modern"
    [10]="agents-legacy-conversational"
    [11]="agents-foundation"
    [12]="agents-langchain-modern"
    [13]="agents-rag-research"
    [14]="agents-legacy-finance"
    [15]="agents-foundation"
    [16]="agents-legacy-embodied"
    [17]="agents-foundation"
)

if [ -z "${1:-}" ]; then
    echo "Usage: source activate-chapter.sh <chapter_number>"
    echo ""
    echo "Chapter → Environment mapping:"
    for ch in $(echo "${!CHAPTER_MAP[@]}" | tr ' ' '\n' | sort -n); do
        printf "  Ch %2d → %s\n" "$ch" "${CHAPTER_MAP[$ch]}"
    done
    return 0 2>/dev/null || exit 0
fi

CH="$1"
ENV_NAME="${CHAPTER_MAP[$CH]:-}"

if [ -z "$ENV_NAME" ]; then
    echo "ERROR: Unknown chapter number: $CH"
    return 1 2>/dev/null || exit 1
fi

# Deactivate current venv if any
if [ -n "${VIRTUAL_ENV:-}" ]; then
    deactivate 2>/dev/null || true
fi

ENV_PATH="$VENVS_DIR/$ENV_NAME"
if [ ! -d "$ENV_PATH" ]; then
    echo "ERROR: Venv not found at $ENV_PATH — run setup-agents-envs.sh first"
    return 1 2>/dev/null || exit 1
fi

source "$ENV_PATH/bin/activate"
echo "✓ Chapter $CH activated → $ENV_NAME"
echo "  Python: $(python --version)  |  Venv: $VIRTUAL_ENV"
SWITCHER_EOF
chmod +x "$SWITCHER"
ok "Chapter switcher created: $SWITCHER"

# ── 7. Create shared .env template ──────────────────────────────────────────
if [ ! -f "$REPO_DIR/.env" ]; then
    cat > "$REPO_DIR/.env" << 'DOTENV_EOF'
# API Keys — fill in your own values
OPENAI_API_KEY=sk-your-key-here
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# TAVILY_API_KEY=tvly-your-key-here
# FINNHUB_API_KEY=your-key-here
# HUGGINGFACEHUB_API_TOKEN=hf_your-token-here
DOTENV_EOF
    ok ".env template created at $REPO_DIR/.env"
    warn "IMPORTANT: Add your API keys to $REPO_DIR/.env before running notebooks"
else
    ok ".env already exists"
fi

# ── 8. Summary ──────────────────────────────────────────────────────────────
echo ""
echo "================================================================="
echo "  SETUP COMPLETE"
echo "================================================================="
echo ""
echo "  Venvs installed at: $VENVS_DIR/"
ls -1d "$VENVS_DIR"/agents-* 2>/dev/null | while read d; do
    echo "    ✓ $(basename $d)"
done
echo ""
echo "  Quick start:"
echo "    cd $REPO_DIR"
echo "    source activate-chapter.sh 6     # activates agents-rag-research"
echo "    cd chapter06"
echo "    jupyter notebook"
echo ""
echo "  Jupyter kernels are registered — you can also select"
echo "  the right kernel from within any notebook UI."
echo "================================================================="
