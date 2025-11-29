import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig

model_id = "ViraIntelligentDataMining/PersianLLaMA-13B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# configuration for 4-bit quantization
# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16,
# )

#configuration for 8-bit quantization
bnb_config = BitsAndBytesConfig(load_in_8bit=True)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",                 # let HF place layers on GPU/CPU
)

prompt_template = (
    "Below is an instruction that describes a task. "
    "Write a response that appropriately completes the request.\n\n"
    "### Instruction:\n\n{instruction}\n\n### Response:\n"
)

def build_prompt(instruction, extra_input=None):
    if extra_input:
        instruction = instruction + "\n" + extra_input
    return prompt_template.format(instruction=instruction)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.5,
    do_sample=True,
    repetition_penalty=1.2,
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id,
    return_full_text=False,
)

def ask(instruction, extra_input=None):
    prompt = build_prompt(instruction, extra_input)
    out = pipe(prompt)[0]["generated_text"]
    return out.strip()

answer = ask("در مورد هوش مصنوعی توضیح بده.")
print(answer)
