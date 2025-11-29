from model_manager import _schedule_auto_unload, get_model

def qwen_chat(text: str) -> str:
    """
    Run a single-turn chat with Qwen3-VL-8B-Instruct.
    Model is loaded on demand and auto-unloaded after 10 min of inactivity.
    """
    model, processor = get_model("qwen")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text,
                },
            ],
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )

    # Move tensors to same device as the model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    generated_ids = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
    )

    # Remove prompt tokens
    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(inputs["input_ids"], generated_ids)
    ]

    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    # Refresh TTL again after generation (in case generation took long)
    _schedule_auto_unload()

    return output_text[0]
