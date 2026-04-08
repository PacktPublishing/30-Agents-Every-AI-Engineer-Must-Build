#!/usr/bin/env bash
# =============================================================================
# fresh-ubuntu-setup.sh
# Complete developer environment setup for a NEW Ubuntu machine
# Tailored for: AI/ML development, Jupyter Lab, VS Code, Python 3.11
# Author: Imran Ahmad — machine bootstrap
# =============================================================================
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[  OK]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
section() { echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; echo -e "${CYAN}  $*${NC}"; echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"; }

# ═══════════════════════════════════════════════════════════════
section "1/8  SYSTEM UPDATE & CORE BUILD TOOLS"
# ═══════════════════════════════════════════════════════════════
sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install -y \
    build-essential \
    gcc g++ make cmake \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    wget curl jq unzip zip \
    htop tree ncdu \
    net-tools openssh-client \
    libssl-dev libffi-dev \
    libreadline-dev libbz2-dev libsqlite3-dev \
    liblzma-dev libncurses5-dev libncursesw5-dev \
    zlib1g-dev tk-dev

ok "Core build tools installed"

# ═══════════════════════════════════════════════════════════════
section "2/8  GIT"
# ═══════════════════════════════════════════════════════════════
sudo apt-get install -y git git-lfs

# Basic git config (user can override later)
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor "code --wait"

# Prompt user for git identity if not set
if [ -z "$(git config --global user.name 2>/dev/null)" ]; then
    git config --global user.name "Imran Ahmad"
    git config --global user.email "cloudanum@gmail.com"
    warn "Git user set to 'Imran Ahmad <cloudanum@gmail.com>' — change with:"
    warn "  git config --global user.name 'Your Name'"
    warn "  git config --global user.email 'your@email.com'"
fi

ok "Git $(git --version | cut -d' ' -f3) configured"

# ═══════════════════════════════════════════════════════════════
section "3/8  PYTHON 3.11 + 3.12 (deadsnakes PPA)"
# ═══════════════════════════════════════════════════════════════
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update

# Install Python 3.11 (primary — book targets this)
sudo apt-get install -y \
    python3.11 python3.11-venv python3.11-dev python3.11-distutils

# Install Python 3.12 (secondary — good to have)
sudo apt-get install -y \
    python3.12 python3.12-venv python3.12-dev

# Ensure pip is available for 3.11
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.11

# Make python3.11 the default 'python3' (optional but convenient)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2
# Set 3.11 as default since the book targets it
sudo update-alternatives --set python3 /usr/bin/python3.11

# Also set up 'python' alias
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

ok "Python 3.11 ($(python3.11 --version)) installed as default"
ok "Python 3.12 ($(python3.12 --version)) also available"

# ═══════════════════════════════════════════════════════════════
section "4/8  GLOBAL PYTHON TOOLS (pipx)"
# ═══════════════════════════════════════════════════════════════
python3.11 -m pip install --user pipx
python3.11 -m pipx ensurepath
export PATH="$HOME/.local/bin:$PATH"

# Install common global tools via pipx (isolated from venvs)
pipx install --python python3.11 jupyterlab
pipx install --python python3.11 notebook
pipx install --python python3.11 black
pipx install --python python3.11 ruff
pipx install --python python3.11 cookiecutter

# Inject ipykernel into jupyterlab so it can discover venv kernels
pipx inject jupyterlab ipykernel

ok "JupyterLab installed globally via pipx"
ok "  Launch with: jupyter lab"
ok "  Black, Ruff, Cookiecutter also available"

# ═══════════════════════════════════════════════════════════════
section "5/8  VS CODE"
# ═══════════════════════════════════════════════════════════════
if ! command -v code &>/dev/null; then
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/packages.microsoft.gpg
    sudo install -D -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
    echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | \
        sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y code
    rm -f /tmp/packages.microsoft.gpg
    ok "VS Code installed"
else
    ok "VS Code already installed ($(code --version | head -1))"
fi

# Install essential VS Code extensions
info "Installing VS Code extensions..."
code --install-extension ms-python.python              2>/dev/null || true
code --install-extension ms-python.vscode-pylance      2>/dev/null || true
code --install-extension ms-toolsai.jupyter             2>/dev/null || true
code --install-extension ms-toolsai.jupyter-keymap      2>/dev/null || true
code --install-extension ms-toolsai.jupyter-renderers   2>/dev/null || true
code --install-extension GitHub.copilot                 2>/dev/null || true
code --install-extension GitHub.copilot-chat            2>/dev/null || true
code --install-extension eamodio.gitlens                2>/dev/null || true
code --install-extension yzhang.markdown-all-in-one     2>/dev/null || true
code --install-extension ms-vscode.makefile-tools       2>/dev/null || true
code --install-extension streetsidesoftware.code-spell-checker 2>/dev/null || true

ok "VS Code extensions installed"

# ═══════════════════════════════════════════════════════════════
section "6/8  OCR, PDF & MEDIA TOOLS (needed by book chapters)"
# ═══════════════════════════════════════════════════════════════
sudo apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    ffmpeg \
    libsm6 libxext6 libxrender-dev \
    libjpeg-dev libpng-dev

ok "Tesseract OCR, Poppler, FFmpeg installed"

# ═══════════════════════════════════════════════════════════════
section "7/8  NODE.js (LTS — useful for tooling)"
# ═══════════════════════════════════════════════════════════════
if ! command -v node &>/dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
    ok "Node.js $(node --version) + npm $(npm --version) installed"
else
    ok "Node.js already installed ($(node --version))"
fi

# ═══════════════════════════════════════════════════════════════
section "8/8  DOCKER (optional but useful)"
# ═══════════════════════════════════════════════════════════════
if ! command -v docker &>/dev/null; then
    info "Installing Docker..."
    curl -fsSL https://get.docker.com | sudo sh
    sudo usermod -aG docker "$USER"
    ok "Docker installed (log out & back in for group membership)"
else
    ok "Docker already installed ($(docker --version | cut -d' ' -f3 | tr -d ','))"
fi

# ═══════════════════════════════════════════════════════════════
section "FINAL SUMMARY"
# ═══════════════════════════════════════════════════════════════
echo ""
echo "  ┌─────────────────────────────────────────────────────┐"
echo "  │  Tool              Version                          │"
echo "  ├─────────────────────────────────────────────────────┤"
printf "  │  %-18s %-33s│\n" "Python" "$(python3.11 --version 2>&1 | cut -d' ' -f2)"
printf "  │  %-18s %-33s│\n" "Git" "$(git --version | cut -d' ' -f3)"
printf "  │  %-18s %-33s│\n" "VS Code" "$(code --version 2>/dev/null | head -1 || echo 'N/A')"
printf "  │  %-18s %-33s│\n" "JupyterLab" "$(jupyter lab --version 2>/dev/null || echo 'pending PATH')"
printf "  │  %-18s %-33s│\n" "Node.js" "$(node --version 2>/dev/null || echo 'N/A')"
printf "  │  %-18s %-33s│\n" "Docker" "$(docker --version 2>/dev/null | cut -d' ' -f3 | tr -d ',' || echo 'N/A')"
printf "  │  %-18s %-33s│\n" "Tesseract" "$(tesseract --version 2>&1 | head -1 || echo 'N/A')"
echo "  └─────────────────────────────────────────────────────┘"
echo ""
echo "  NEXT STEPS:"
echo "  ─────────────────────────────────────────────────────"
echo "  1. Close & reopen your terminal (for PATH updates)"
echo "  2. Run the agents environment setup:"
echo "     ./setup-agents-envs.sh"
echo "  3. Add API keys to the repo .env file"
echo "  4. Start working:"
echo "     source activate-chapter.sh 1"
echo "     jupyter lab"
echo ""
warn "NOTE: Log out & back in for Docker group membership to take effect."
