import os
from openai import OpenAI
from system_contents.Qwen_sql_system_content import SQL_SYSTEM_PROMPT

api_key = os.environ.get("OPENAI_API_KEY_ECC")
if api_key is None:
    raise ValueError(
        "API key not found. Please set the OPENAI_API_KEY_ECC environment variable."
    )

client = OpenAI(api_key=api_key)

def ask_openai(prompt: str, model: str = "gpt-5.2") -> str:
    """
    Sends a system prompt and a user question to an OpenAI model
    and returns the model's response as a string.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SQL_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()
