# Troubleshooting Guide — Chapter 11

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Chapter:** 11 — Multi-Modal Perception Agents

---

## Quick Diagnostic

Run this in the notebook's first cell to see your environment status:
- `SIMULATION_MODE = True/False`
- If `True`, the notebook uses mock backends — no GPU or API key needed.
- If `False`, you are in Live Mode with full model inference.

---

## Issue 1: `ModuleNotFoundError: No module named 'torch'`

**Cause:** torch is not installed. This is expected in Simulation Mode.

**Fix:** If you want Live Mode, install PyTorch for your CUDA version:
- Visit https://pytorch.org/get-started/locally/
- Select your OS, CUDA version, and package manager
- Example: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121`

**If you just want to run the notebook:** No fix needed.
Simulation Mode runs without torch.

---

## Issue 2: `numpy.dtype size changed` or NumPy 2.0 ABI errors

**Cause:** NumPy 2.0 broke the C-level ABI. Libraries compiled against
NumPy 1.x crash when NumPy 2.x is present.

**Fix:**
```bash
pip install "numpy>=1.24,<2.0"
pip install --force-reinstall transformers torch
```

---

## Issue 3: `OutOfMemoryError: CUDA out of memory`

**Cause:** LLaVA 1.5 (7B parameters) requires ~14 GB VRAM in float16.

**Fix options (pick one):**

1. **Use Simulation Mode** (set `HUGGINGFACE_TOKEN=""` in `.env`)
2. **Use 4-bit quantization:**
   ```bash
   pip install bitsandbytes>=0.43.0
   ```
   Then modify model loading:
   ```python
   model = LlavaForConditionalGeneration.from_pretrained(
       model_id, load_in_4bit=True, device_map="auto"
   )
   ```
3. **Use CPU** (very slow but functional):
   ```python
   model = LlavaForConditionalGeneration.from_pretrained(
       model_id, torch_dtype=torch.float32, device_map="cpu"
   )
   ```

---

## Issue 4: `OSError: You are not authorized to access llava-hf/llava-1.5-7b-hf`

**Cause:** Hugging Face gated model access not granted.

**Fix:**
1. Go to https://huggingface.co/llava-hf/llava-1.5-7b-hf
2. Accept the model license
3. Generate a token at https://huggingface.co/settings/tokens
4. Add to your `.env` file: `HUGGINGFACE_TOKEN=your_hugging_face_token_here`

---

## Issue 5: `ImportError: cannot import name 'LlavaForConditionalGeneration'`

**Cause:** transformers version is too old.

**Fix:**
```bash
pip install "transformers>=4.40.0"
```

---

## Issue 6: Pillow `DecompressionBombError` on large images

**Cause:** Pillow's safety limit (178 million pixels) is exceeded.

**Fix:** The notebook's Vision agent section includes a resize step.
If you encounter this with your own images:
```python
from PIL import Image
Image.MAX_IMAGE_PIXELS = 300_000_000  # Raise limit cautiously
```

---

## Issue 7: ANSI color codes display as raw text

**Cause:** Your Jupyter environment doesn't render ANSI escape codes.

**Fix options:**
- Use JupyterLab (supports ANSI natively)
- Install: `pip install ipywidgets`
- Or set `AgentLogger.USE_ANSI = False` (falls back to prefix-only mode)

---

## Issue 8: `accelerate` version conflicts with transformers

**Cause:** Mismatched versions of accelerate and transformers.

**Fix:**
```bash
pip install "accelerate>=0.28.0" "transformers>=4.40.0" --upgrade
```

---

## Environment Compatibility Matrix

| Setup                       | Mode       | Works? | Notes                    |
|-----------------------------|------------|--------|--------------------------|
| No GPU, no token            | Simulation | Yes    | Full notebook runs       |
| GPU < 16GB VRAM, has token  | Simulation | Yes    | Auto-detected            |
| GPU >= 16GB, has token      | Live       | Yes    | Full inference           |
| Apple Silicon (MPS)         | Simulation | Yes    | MPS not yet reliable     |
| Google Colab (free T4)      | Simulation | Yes    | T4 has 16GB but is slow  |
| Google Colab (A100)         | Live       | Yes    | Best free option         |

---

## Still stuck?

Open an issue on the book's GitHub repository:
https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build/issues

---

*Author: Imran Ahmad — Packt Publishing, 2026*
