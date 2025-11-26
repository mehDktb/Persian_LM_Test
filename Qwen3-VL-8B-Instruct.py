from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
import torch

model_name = "Qwen/Qwen3-VL-8B-Instruct"

# 1) Load model (will go to GPU if available thanks to device_map="auto")
model = Qwen3VLForConditionalGeneration.from_pretrained(
    model_name,
    dtype="auto",           # or torch.bfloat16 if your GPU supports it
    device_map="auto",
)

# 2) Load processor (tokenizer + image preprocessor)
processor = AutoProcessor.from_pretrained(model_name)

# 3) Build a simple chat with a Persian prompt
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "سلام. می‌تونی فارسی صحبت کنی؟ دو جمله دربارهٔ هوش مصنوعی به فارسی بنویس.",
            },
        ],
    }
]

# 4) Convert messages to model inputs
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
)

# Move tensors to the same device as the model
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# 5) Generate
generated_ids = model.generate(
    **inputs,
    max_new_tokens=256,
    do_sample=True,
    top_p=0.9,
    temperature=0.7,
)

# 6) Strip the prompt tokens from the output so we only decode the answer
generated_ids_trimmed = [
    out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs["input_ids"], generated_ids)
]

# 7) Decode to text
output_text = processor.batch_decode(
    generated_ids_trimmed,
    skip_special_tokens=True,
    clean_up_tokenization_spaces=False,
)

print("MODEL ANSWER (Persian test):")
print(output_text[0])
