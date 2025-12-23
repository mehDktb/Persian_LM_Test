import os
import sys
import gc
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



def load_model_and_tokenizer(model_path, fp16=True):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16 if fp16 else torch.float32
    )

    model = AutoModelForVision2Seq.from_pretrained(
        model_path,
        trust_remote_code=True,
        quantization_config=bnb_config,
        device_map="auto"
    )

    model = prepare_model_for_kbit_training(model)

    # LoRA config
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_config)

    model.print_trainable_parameters()

    return model, tokenizer


def load_qa_dataset(train_file, valid_file=None):
    data_files = {"train": train_file}
    if valid_file:
        data_files["validation"] = valid_file
    return load_dataset("json", data_files=data_files)


def preprocess_sql_qa(example, tokenizer, max_length=2048):

    user_part = (
        "<|im_start|>user\n"
        f"{example['system_prompt']}\n{example['question']}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    assistant_part = f"{example['answer']}\n<|im_end|>"

    user_tokens = tokenizer(user_part, add_special_tokens=False)
    assistant_tokens = tokenizer(assistant_part, add_special_tokens=False)

    input_ids = user_tokens["input_ids"] + assistant_tokens["input_ids"]

    labels = [-100] * len(user_tokens["input_ids"]) + assistant_tokens["input_ids"]

    input_ids = input_ids[:max_length]
    labels = labels[:max_length]

    return {"input_ids": input_ids, "labels": labels}



def get_data_collator(tokenizer):
    def data_collator(features):
        max_len = max(len(f["input_ids"]) for f in features)
        input_ids, labels, attention_mask = [], [], []

        for f in features:
            pad_len = max_len - len(f["input_ids"])
            input_ids.append(f["input_ids"] + [tokenizer.pad_token_id]*pad_len)
            labels.append(f["labels"] + [-100]*pad_len)
            attention_mask.append([1]*len(f["input_ids"]) + [0]*pad_len)

        return {
            "input_ids": torch.tensor(input_ids),
            "labels": torch.tensor(labels),
            "attention_mask": torch.tensor(attention_mask)
        }

    return data_collator


def train_model(model, tokenizer, dataset, training_args):
    max_length = training_args["max_length"]
    output_dir = training_args["output_dir"]
    dataset = dataset.map(
        lambda x: preprocess_sql_qa(x, tokenizer, max_length),
        remove_columns=dataset["train"].column_names,
        num_proc=4
    )

    data_collator = get_data_collator(tokenizer)

    ta_kwargs = dict(training_args)
    ta_kwargs.pop("max_length", None)

    args = TrainingArguments(**ta_kwargs)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=dataset["train"],
        data_collator=data_collator
    )

    trainer.train()

    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("✅ QA fine-tuning completed!")
    trainer.model.cpu()
    if hasattr(trainer, "optimizer") and trainer.optimizer is not None:
        trainer.optimizer.zero_grad(set_to_none=True)

    del trainer
    del model
    gc.collect()


