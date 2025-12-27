import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import torch
from peft import PeftModel
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoTokenizer,
    AutoModelForVision2Seq,
    Trainer,
    TrainingArguments,
    BitsAndBytesConfig,
    AutoProcessor,
)


def merge_lora_into_base(
    base_model_path: str,
    adapter_path: str,
    merged_out_path: str,
    dtype: torch.dtype = torch.float16,
):
    os.makedirs(merged_out_path, exist_ok=True)

    base_model = AutoModelForVision2Seq.from_pretrained(
        base_model_path,
        trust_remote_code=True,
        torch_dtype=dtype,
        device_map="auto",
        low_cpu_mem_usage=True,
    )

    peft_model = PeftModel.from_pretrained(
        base_model,
        adapter_path,
        device_map="auto",
    )

    merged_model = peft_model.merge_and_unload()

    merged_model.save_pretrained(merged_out_path, safe_serialization=True)

    try:
        processor = AutoProcessor.from_pretrained(base_model_path, trust_remote_code=True)
        processor.save_pretrained(merged_out_path)
    except Exception as e:
        print(f"[warn] AutoProcessor save failed: {e}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
        tokenizer.save_pretrained(merged_out_path)
    except Exception as e:
        print(f"[warn] AutoTokenizer save failed: {e}")

    print(f"✅ Merged model saved to: {merged_out_path}")


