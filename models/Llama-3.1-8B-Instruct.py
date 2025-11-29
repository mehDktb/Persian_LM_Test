from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Chat messages (same structure as before)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": "سلام. در دو جمله توضیح بده هوش مصنوعی چیست.",
    },
]

# Use the built-in chat template to turn messages → prompt text
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
).to(model.device)

with torch.no_grad():
    generated_ids = model.generate(
        inputs,
        max_new_tokens=256,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
    )

# Remove the prompt part so we only decode the answer
generated_only = generated_ids[0, inputs.shape[-1]:]

text = tokenizer.decode(
    generated_only,
    skip_special_tokens=True,
    clean_up_tokenization_spaces=False,
)

print(text)
