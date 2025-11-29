import torch
from threading import Timer
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor

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
    model_name = "Qwen/Qwen3-VL-8B-Instruct"

    print("[INFO] Loading Qwen model into memory...")
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        model_name,
        dtype="auto",
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(model_name)
    return model, processor


# Map from logical model name → loader function
MODEL_LOADERS = {
    "qwen": _load_qwen,
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
