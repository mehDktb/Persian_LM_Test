from pathlib import Path

from fine_tuning.gpt_dataset_answer_generator import ask_openai
# from model_manager.Qwen3_VL_8B_Instruct import qwen_sql_from_nl




def load_prompts(path: str | Path) -> list[str]:

    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        return []

    raw_blocks = text.split("\n\n")
    prompts = [block.strip() for block in raw_blocks if block.strip()]
    return prompts

def write_queries(
    prompts: list[str],
    output_path: str | Path = "queries",
    model: str = "Qwen",
):
    """
    For each prompt, call qwen_sql_from_nl and write:

    --############################
    --prompt

    model_output
    --############################
    """
    output_path = Path(output_path)

    with output_path.open("w", encoding="utf-8") as f_out:
        for i, prompt in enumerate(prompts, start=1):
            print(f"[{i}/{len(prompts)}] Running model for prompt:")
            print(prompt)
            print("-" * 40)

            if model == "Qwen":
                sql = qwen_sql_from_nl(prompt)
            elif model == "gpt":
                sql = ask_openai(prompt)


            f_out.write("--############################\n")
            for line in prompt.splitlines():
                f_out.write(f"--{line}\n")
            f_out.write("\n")
            f_out.write(sql.rstrip() + "\n")
            f_out.write("--############################\n")
            f_out.write("\n")

def main():
    prompts_file = "samples/samples.txt"
    output_file = "results/gpt_queries.txt"

    prompts = load_prompts(prompts_file)
    if not prompts:
        print(f"No prompts found in {prompts_file}")
        return

    write_queries(prompts, output_file, model="gpt")

    print(f"Done. Results written to {output_file}")

if __name__ == "__main__":
    main()