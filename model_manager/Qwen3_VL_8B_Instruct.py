from .model_manager import _schedule_auto_unload, get_model
from system_contents.Qwen_sql_system_content import SQL_SYSTEM_PROMPT, SIMPLE_SYS_CONTENT



def qwen_sql_from_nl(user_text: str) -> str:
    """
    Convert a natural-language request (Persian or English) into a T-SQL query
    using Qwen3-VL-8B-Instruct, given a database schema.
    """
    model, processor = get_model("qwen")

    system_prompt = SIMPLE_SYS_CONTENT

    # Use list-of-segments format for both system and user
    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": system_prompt},
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_text},
            ],
        },
    ]

    # 1) Build chat prompt string
    chat_text = processor.apply_chat_template(
        messages,
        tokenize=False,              # get plain text, not tensors
        add_generation_prompt=True,
    )

    # 2) Tokenize – IMPORTANT: use keyword argument text=..., and images=None
    inputs = processor(
        text=[chat_text],            # or text=chat_text, but list is safer (batch dim)
        images=None,
        return_tensors="pt",
    )

    # 3) Move tensors to model device
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # 4) Generate
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=1024,
        do_sample=False,
        top_p=1.0,
        temperature=0.0,
    )

    # 5) Strip prompt tokens
    prompt_len = inputs["input_ids"].shape[1]
    generated_ids_trimmed = generated_ids[:, prompt_len:]

    # 6) Decode
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    _schedule_auto_unload()

    sql = output_text[0].strip()

    # 7) Clean ```sql fences if present
    if sql.startswith("```"):
        sql = sql.strip("`")
        lines = sql.splitlines()
        if lines and lines[0].strip().lower() in ("sql", "tsql", "t-sql"):
            sql = "\n".join(lines[1:]).strip()

    return sql



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
        max_new_tokens=1024,
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
