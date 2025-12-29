import torch
from threading import Timer
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from constants.paths import MODEL_QWEN_PATH, MODEL_QWEN_PATH_FINE_TUNED
MODEL_TTL_SECONDS = 600  # 10 minutes


# Global state for the currently loaded model
ACTIVE_MODEL = {
    "name": None,
    "model": None,
    "processor": None,
    "timer": None,
}


def _unload_active_model():
    """Free the current model from memory (GPU + CPU)"""
    global ACTIVE_MODEL

    if ACTIVE_MODEL["timer"] is not None:
        ACTIVE_MODEL["timer"].cancel()
        ACTIVE_MODEL["timer"] = None

    if ACTIVE_MODEL["model"] is not None:
        try:
            # Drop references
            del ACTIVE_MODEL["model"]
            del ACTIVE_MODEL["processor"]
            # Try to free GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception as e:
            print(f"[WARN] Error while unloading model: {e}")

    ACTIVE_MODEL["name"] = None
    ACTIVE_MODEL["model"] = None
    ACTIVE_MODEL["processor"] = None


def _schedule_auto_unload():
    """Reset timer: unload model after MODEL_TTL_SECONDS of inactivity."""
    global ACTIVE_MODEL

    # Cancel old timer if exists
    if ACTIVE_MODEL["timer"] is not None:
        ACTIVE_MODEL["timer"].cancel()

    t = Timer(MODEL_TTL_SECONDS, _unload_active_model)
    t.daemon = True  # don't block process exit
    ACTIVE_MODEL["timer"] = t
    t.start()


def _load_qwen():
    """Actually load Qwen model + processor into memory."""
    model_name = MODEL_QWEN_PATH_FINE_TUNED

    print(f"[INFO] Loading {model_name} model into memory...")
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        model_name,
        dtype="auto",
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(model_name)
    return model, processor

def _load_llama():
    print("[INFO] Loading Llama 3.1 8B model into memory...")

    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    return model, tokenizer


def _load_gpt_oss():
    """
    Load openai/gpt-oss-20b with its own quantization (MxFP4).
    Returns (model, tokenizer).
    """
    print("[INFO] Loading gpt-oss-20b into memory (MxFP4)...")

    model_path = "/home/ubuntu/model/gpt-oss-20b"

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        local_files_only=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype="auto",
        local_files_only=True,
    )

    model.eval()
    return model, tokenizer



# Map from logical model name → loader function
MODEL_LOADERS = {
    "qwen": _load_qwen,
    "llama_3.1_8B": _load_llama,
    "gpt_oss": _load_gpt_oss,
}


def get_model(model_name: str):
    """
    Get a model by name.

    - If the requested model is already loaded and not expired:
      reuse it and refresh the auto-unload timer.
    - If another model is loaded: unload it immediately and load the new one.
    """
    global ACTIVE_MODEL

    # If same model already loaded, just refresh TTL
    if ACTIVE_MODEL["name"] == model_name and ACTIVE_MODEL["model"] is not None:
        _schedule_auto_unload()
        return ACTIVE_MODEL["model"], ACTIVE_MODEL["processor"]

    # Different model loaded → unload it
    if ACTIVE_MODEL["model"] is not None and ACTIVE_MODEL["name"] != model_name:
        print(f"[INFO] Switching model from {ACTIVE_MODEL['name']} to {model_name}")
        _unload_active_model()

    if model_name not in MODEL_LOADERS:
        raise ValueError(f"Unknown model '{model_name}'")

    # Load new model
    model, processor = MODEL_LOADERS[model_name]()
    ACTIVE_MODEL["name"] = model_name
    ACTIVE_MODEL["model"] = model
    ACTIVE_MODEL["processor"] = processor

    # Arm the TTL
    _schedule_auto_unload()

    return model, processor
