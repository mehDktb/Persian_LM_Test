import os
from openai import OpenAI
from system_contents.Qwen_sql_system_content import SQL_SYSTEM_PROMPT, GPT_DATASET_GENERATOR

api_key = os.environ.get("OPENAI_API_KEY_ECC")
if api_key is None:
    raise ValueError(
        "API key not found. Please set the OPENAI_API_KEY_ECC environment variable."
    )

client = OpenAI(api_key=api_key)

def ask_openai(prompt: str, model: str = "gpt-5.2", system_content: str = SQL_SYSTEM_PROMPT) -> str:

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()


def main():
    user_action = input("which system content do want to use?\n1)sql_generation\t2)dataset_generation\n->")
    if user_action not in ["1","2"]:
        raise ValueError("You have to only enter 1 or 2")
    elif user_action == 1:
        system_content = SQL_SYSTEM_PROMPT
    else :
        system_content = GPT_DATASET_GENERATOR
    prompt = input("what do you want to ask from GPT?\n->")
    response = ask_openai(prompt=prompt, system_content=system_content)

    print(response)
if __name__ == "__main__":
    main()