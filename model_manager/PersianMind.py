from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

model_id = "universitytehran/PersianMind-v1.0"

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
    max_new_tokens=512,
    temperature=0.5,
    do_sample=True,
)


#persian template
# TEMPLATE = (
#     "در ادامه یک دستور داده شده است. "
#     "پاسخی مناسب و کامل ارائه بده.\n\n"
#     "### دستور:\n{prompt}\n\n### پاسخ:\n"
# )

TEMPLATE = "{context}\nYou: {prompt}\nPersianMind: "

CONTEXT = "This is a conversation with PersianMind. It is an artificial intelligence model designed by a team of " \
    "NLP experts at the University of Tehran to help you with various tasks such as answering questions, " \
    "providing recommendations, and helping with decision making. You can ask it anything you want and " \
    "it will do its best to give you accurate and relevant information."

PROMPT = "یک نامه اداری به اقای غلامی بنویس و بگو عصر بیاد جلسه "

model_input = TEMPLATE.format(context=CONTEXT, prompt=PROMPT)


result = pipe(model_input)[0]["generated_text"]
print(result)

