import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "ViraIntelligentDataMining/PersianLLaMA-13B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_8bit=True,
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

\
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.5,
    do_sample=True,
    repetition_penalty=1.1,
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
