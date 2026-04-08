#!/usr/bin/env bash
# =============================================================================
# verify-setup.sh
# Post-install verification for fresh Ubuntu + agents environments
# =============================================================================
set -uo pipefail

PASS=0; FAIL=0; WARN=0
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

pass() { ((PASS++)); echo -e "  ${GREEN}✓${NC}  $*"; }
fail() { ((FAIL++)); echo -e "  ${RED}✗${NC}  $*"; }
skip() { ((WARN++)); echo -e "  ${YELLOW}⊘${NC}  $*"; }

section() { echo -e "\n${CYAN}── $* ──${NC}"; }

check_cmd() {
    local name="$1" cmd="$2"
    if eval "$cmd" &>/dev/null; then
        local ver
        ver=$(eval "$cmd" 2>&1 | head -1)
        pass "$name  →  $ver"
    else
        fail "$name  →  NOT FOUND"
    fi
}

# ═══════════════════════════════════════════════════════════════
section "SYSTEM TOOLS"
# ═══════════════════════════════════════════════════════════════
check_cmd "gcc"        "gcc --version"
check_cmd "make"       "make --version"
check_cmd "cmake"      "cmake --version"
check_cmd "curl"       "curl --version"
check_cmd "jq"         "jq --version"
check_cmd "git"        "git --version"
check_cmd "git-lfs"    "git lfs version"

# ═══════════════════════════════════════════════════════════════
section "PYTHON"
# ═══════════════════════════════════════════════════════════════
check_cmd "python3"       "python3 --version"
check_cmd "python3.11"    "python3.11 --version"
check_cmd "pip (3.11)"    "python3.11 -m pip --version"
check_cmd "venv (3.11)"   "python3.11 -c 'import venv; print(\"venv OK\")'"

if command -v python3.12 &>/dev/null; then
    check_cmd "python3.12" "python3.12 --version"
else
    skip "python3.12 (optional — not installed)"
fi

# Check default python3 points to 3.11
PY_VER=$(python3 --version 2>&1)
if echo "$PY_VER" | grep -q "3.11"; then
    pass "python3 default → 3.11"
else
    skip "python3 default is $PY_VER (expected 3.11 — not critical)"
fi

# ═══════════════════════════════════════════════════════════════
section "JUPYTER & PYTHON TOOLS"
# ═══════════════════════════════════════════════════════════════
check_cmd "JupyterLab"   "jupyter lab --version"
check_cmd "jupyter"      "jupyter --version"
check_cmd "pipx"         "pipx --version"

if command -v black &>/dev/null; then
    check_cmd "black" "black --version"
else
    skip "black (optional formatter)"
fi

if command -v ruff &>/dev/null; then
    check_cmd "ruff" "ruff --version"
else
    skip "ruff (optional linter)"
fi

# ═══════════════════════════════════════════════════════════════
section "VS CODE"
# ═══════════════════════════════════════════════════════════════
if command -v code &>/dev/null; then
    check_cmd "VS Code" "code --version"
    echo ""
    echo "    Installed extensions:"
    code --list-extensions 2>/dev/null | while read ext; do
        echo -e "      ${GREEN}•${NC} $ext"
    done
else
    fail "VS Code → NOT FOUND"
fi

# ═══════════════════════════════════════════════════════════════
section "OCR / MEDIA TOOLS (needed by book chapters)"
# ═══════════════════════════════════════════════════════════════
check_cmd "tesseract"   "tesseract --version"
check_cmd "pdftoppm"    "pdftoppm -v"
check_cmd "ffmpeg"      "ffmpeg -version"

# ═══════════════════════════════════════════════════════════════
section "NODE.js"
# ═══════════════════════════════════════════════════════════════
check_cmd "node"  "node --version"
check_cmd "npm"   "npm --version"

# ═══════════════════════════════════════════════════════════════
section "DOCKER"
# ═══════════════════════════════════════════════════════════════
if command -v docker &>/dev/null; then
    check_cmd "docker" "docker --version"
    if docker ps &>/dev/null; then
        pass "docker daemon running & accessible"
    else
        skip "docker installed but daemon not accessible (may need logout/login for group)"
    fi
else
    skip "docker (optional — not installed)"
fi

# ═══════════════════════════════════════════════════════════════
section "GPU (optional)"
# ═══════════════════════════════════════════════════════════════
if command -v nvidia-smi &>/dev/null; then
    check_cmd "nvidia-smi" "nvidia-smi --query-gpu=name,driver_version --format=csv,noheader"
    if python3.11 -c "import torch; print(f'CUDA {torch.version.cuda}, device: {torch.cuda.get_device_name(0)}')" 2>/dev/null; then
        pass "PyTorch CUDA operational"
    else
        skip "PyTorch CUDA not available (will be available inside agents-multimodal venv)"
    fi
else
    skip "No NVIDIA GPU detected (Ch11 GPU mode unavailable — simulation mode still works)"
fi

# ═══════════════════════════════════════════════════════════════
section "AGENTS VIRTUAL ENVIRONMENTS"
# ═══════════════════════════════════════════════════════════════
VENVS_DIR="$HOME/.venvs/agents"

EXPECTED_ENVS=(
    "agents-foundation"
    "agents-langchain-modern"
    "agents-rag-research"
    "agents-legacy-conversational"
    "agents-legacy-finance"
    "agents-legacy-embodied"
)

if [ -d "$VENVS_DIR" ]; then
    for env in "${EXPECTED_ENVS[@]}"; do
        env_path="$VENVS_DIR/$env"
        if [ -f "$env_path/bin/activate" ]; then
            # Quick sanity: activate, check pip list length, deactivate
            pkg_count=$(source "$env_path/bin/activate" && pip list --format=columns 2>/dev/null | tail -n +3 | wc -l && deactivate)
            pass "$env  →  $pkg_count packages"
        else
            fail "$env  →  NOT FOUND (run setup-agents-envs.sh)"
        fi
    done

    # Optional multimodal
    if [ -f "$VENVS_DIR/agents-multimodal/bin/activate" ]; then
        pass "agents-multimodal  →  present (GPU env)"
    else
        skip "agents-multimodal  →  not created (no GPU, or not yet run)"
    fi
else
    fail "Venvs directory $VENVS_DIR does not exist — run setup-agents-envs.sh first"
fi

# ═══════════════════════════════════════════════════════════════
section "JUPYTER KERNELS"
# ═══════════════════════════════════════════════════════════════
if command -v jupyter &>/dev/null; then
    KERNELS=$(jupyter kernelspec list 2>/dev/null)
    for env in "${EXPECTED_ENVS[@]}"; do
        if echo "$KERNELS" | grep -q "$env"; then
            pass "Kernel: $env"
        else
            fail "Kernel: $env  →  NOT REGISTERED"
        fi
    done
else
    fail "jupyter not found — cannot check kernels"
fi

# ═══════════════════════════════════════════════════════════════
section "QUICK SMOKE TEST — import key packages in each venv"
# ═══════════════════════════════════════════════════════════════
smoke_test() {
    local env_name="$1"; shift
    local imports="$*"
    local env_path="$VENVS_DIR/$env_name"

    if [ ! -f "$env_path/bin/activate" ]; then
        fail "$env_name smoke test — venv missing"
        return
    fi

    local result
    result=$(source "$env_path/bin/activate" && python3 -c "$imports" 2>&1 && deactivate)
    if [ $? -eq 0 ]; then
        pass "$env_name  →  imports OK"
    else
        fail "$env_name  →  import failed: $result"
    fi
}

if [ -d "$VENVS_DIR" ]; then
    smoke_test "agents-foundation" \
        "import openai, numpy, pandas, matplotlib, statsmodels, networkx; print('OK')"

    smoke_test "agents-langchain-modern" \
        "import langchain_core, langchain_openai, pydantic, shap, sklearn; print('OK')"

    smoke_test "agents-rag-research" \
        "import langchain, langchain_community, faiss, sentence_transformers, nltk; print('OK')"

    smoke_test "agents-legacy-conversational" \
        "import langchain, langchain_community, tiktoken; print('OK')"

    smoke_test "agents-legacy-finance" \
        "import langchain, langgraph, yfinance, finnhub; print('OK')"

    smoke_test "agents-legacy-embodied" \
        "import langchain, langgraph, pydantic; print('OK')"
fi

# ═══════════════════════════════════════════════════════════════
section "RESULTS"
# ═══════════════════════════════════════════════════════════════
echo ""
echo -e "  ${GREEN}Passed: $PASS${NC}   ${RED}Failed: $FAIL${NC}   ${YELLOW}Skipped: $WARN${NC}"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo -e "  ${GREEN}══════════════════════════════════════════════════${NC}"
    echo -e "  ${GREEN}  ALL CHECKS PASSED — environment is ready!      ${NC}"
    echo -e "  ${GREEN}══════════════════════════════════════════════════${NC}"
else
    echo -e "  ${RED}══════════════════════════════════════════════════${NC}"
    echo -e "  ${RED}  $FAIL CHECK(S) FAILED — review errors above     ${NC}"
    echo -e "  ${RED}══════════════════════════════════════════════════${NC}"
fi
echo ""
exit $FAIL
