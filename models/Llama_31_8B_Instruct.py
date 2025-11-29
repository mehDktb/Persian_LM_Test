from model_manager import get_model, _schedule_auto_unload

def llama_chat(text: str) -> str:
    """
    Chat with Llama 3.1 8B.
    Loads on demand, unloads after inactivity.
    """
    model, tokenizer = get_model("llama")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text},
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
        )

    # Remove the prompt from result
    generated_only = generated_ids[0, inputs.shape[-1]:]

    reply = tokenizer.decode(
        generated_only,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    _schedule_auto_unload()
    return reply
