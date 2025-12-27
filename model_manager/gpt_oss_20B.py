import torch
from .model_manager import get_model, _schedule_auto_unload

def gpt_oss_chat(
    text: str,
    system_prompt: str = "You are a helpful assistant. Reasoning: medium.",
) -> str:
    """
    Single-turn chat with openai/gpt-oss-20b (8-bit).
    Model is lazy-loaded and auto-unloaded after inactivity by get_model().
    """
    model, tokenizer = get_model("gpt_oss")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": text},
    ]

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
            pad_token_id=tokenizer.eos_token_id,
        )

    # Drop the prompt part, keep only the answer
    generated_only = generated_ids[:, inputs.shape[-1]:]

    output_text = tokenizer.decode(
        generated_only[0],
        skip_special_tokens=True,
    )

    # refresh TTL in case generation was long
    _schedule_auto_unload()

    return output_text