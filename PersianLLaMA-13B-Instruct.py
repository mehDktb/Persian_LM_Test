import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "ViraIntelligentDataMining/PersianLLaMA-13B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_8bit=True,

)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=2000,
    temperature=0.5,
    do_sample=True,
)












# model_id = "ViraIntelligentDataMining/PersianLLaMA-13B-Instruct"

# tokenizer = AutoTokenizer.from_pretrained(model_id)
#
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     device_map="auto",
#     load_in_4bit=True,
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.float16,
#     low_cpu_mem_usage=True,
# )
#
# pipe = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_new_tokens=200,
#     temperature=0.7,
#     do_sample=True,
# )
