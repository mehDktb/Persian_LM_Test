from constants.paths import MODEL_QWEN_PATH
from fine_tuning.fine_tune_qwen_lora import *




MODEL_PATH = MODEL_QWEN_PATH
LORA_ADAPTER_PATH = "./qwen_qa_modular"
MERGED_OUT_PATH = "./qwen_merged_full"
TRAIN_FILE = "./dataset/train.jsonl"



DTYPE = torch.float16
VALID_FILE = None
MAX_LENGTH = 2048
BATCH_SIZE = 1
GRAD_ACCUM = 8
EPOCHS = 3
LR = 2e-5
FP16 = False



fine_tuning_parameters = {
        "output_dir" : LORA_ADAPTER_PATH,
        "overwrite_output_dir":True,
        "per_device_train_batch_size":BATCH_SIZE,
        "gradient_accumulation_steps":GRAD_ACCUM,
        "num_train_epochs":EPOCHS,
        "learning_rate":LR,
        "fp16":FP16,
        "max_length": MAX_LENGTH,
        "logging_steps":10,
        "save_steps":500,
        "save_total_limit":2,
        "report_to":"none",
        "gradient_checkpointing":True,
        "optim":"paged_adamw_8bit",
        "lr_scheduler_type":"cosine",
        "warmup_ratio":0.03,
        "weight_decay":0.01,
        "dataloader_num_workers":4
    }




if __name__ == "__main__":
    model, tokenizer = load_model_and_tokenizer(MODEL_PATH, FP16)
    dataset = load_qa_dataset(TRAIN_FILE, VALID_FILE)
    train_model(model, tokenizer, dataset, fine_tuning_parameters)
    merge_lora_into_base(MODEL_PATH, LORA_ADAPTER_PATH, MERGED_OUT_PATH, DTYPE)