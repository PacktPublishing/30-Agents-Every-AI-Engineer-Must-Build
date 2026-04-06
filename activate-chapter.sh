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
