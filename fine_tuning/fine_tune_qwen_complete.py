import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import torch
from constants.paths import MODEL_QWEN_PATH
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForVision2Seq,
    Trainer,
    TrainingArguments
)


MODEL_PATH = MODEL_QWEN_PATH
OUTPUT_DIR = "./qwen_qa_modular"
TRAIN_FILE = "./dataset/train.jsonl"
VALID_FILE = None

MAX_LENGTH = 8192
BATCH_SIZE = 1
GRAD_ACCUM = 8
EPOCHS = 3
LR = 2e-5
FP16 = False



def load_model_and_tokenizer(model_path, fp16=True):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForVision2Seq.from_pretrained(
        model_path,
        trust_remote_code=True,
        dtype=torch.float16 if fp16 else torch.float32,
        device_map="auto"
    )
    model.train()
    for p in model.parameters():
        p.requires_grad = True

    return model, tokenizer


def load_qa_dataset(train_file, valid_file=None):
    data_files = {"train": train_file}
    if valid_file:
        data_files["validation"] = valid_file
    return load_dataset("json", data_files=data_files)


def preprocess_sql_qa(example, tokenizer, max_length=2048):
    # Combine system prompt + user question
    user_part = (
        "<|im_start|>user\n"
        f"{example['system_prompt']}\n{example['question']}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    assistant_part = f"{example['answer']}\n<|im_end|>"

    # Tokenize
    user_tokens = tokenizer(user_part, add_special_tokens=False)
    assistant_tokens = tokenizer(assistant_part, add_special_tokens=False)

    input_ids = user_tokens["input_ids"] + assistant_tokens["input_ids"]

    # Mask user tokens
    labels = [-100] * len(user_tokens["input_ids"]) + assistant_tokens["input_ids"]

    # Truncate
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



def get_training_args(output_dir):
    return TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        num_train_epochs=EPOCHS,
        learning_rate=LR,
        fp16=FP16,
        logging_steps=10,
        save_steps=500,
        save_total_limit=2,
        evaluation_strategy="no",
        report_to="none",
        gradient_checkpointing=True,
        optim="adamw_torch",
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        weight_decay=0.01,
        dataloader_num_workers=4
    )



def train_model(model, tokenizer, dataset, output_dir):
    # Preprocess dataset
    dataset = dataset.map(
        lambda x: preprocess_sql_qa(x, tokenizer, MAX_LENGTH),
        remove_columns=dataset["train"].column_names,
        num_proc=4
    )

    # Create data collator
    data_collator = get_data_collator(tokenizer)

    # Create training args
    training_args = get_training_args(output_dir)

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        data_collator=data_collator
    )

    # Train
    trainer.train()

    # Save
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("✅ QA fine-tuning completed!")


if __name__ == "__main__":
    model, tokenizer = load_model_and_tokenizer(MODEL_PATH, FP16)
    dataset = load_qa_dataset(TRAIN_FILE, VALID_FILE)
    train_model(model, tokenizer, dataset, OUTPUT_DIR)