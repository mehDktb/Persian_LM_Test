from pathlib import Path

from models.Qwen3_VL_8B_Instruct import qwen_sql_from_nl




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
    schema: str = None,
):
    """
    For each prompt, call qwen_sql_from_nl and write:

    --############################
    --prompt

    model_output
    --############################
    """
    output_path = Path(output_path)

    # Overwrite file each run; use 'a' if you want to append instead
    with output_path.open("w", encoding="utf-8") as f_out:
        for i, prompt in enumerate(prompts, start=1):
            print(f"[{i}/{len(prompts)}] Running model for prompt:")
            print(prompt)
            print("-" * 40)

            sql = qwen_sql_from_nl(prompt, schema=schema) if schema is not None else qwen_sql_from_nl(prompt)

            f_out.write("--############################\n")
            # write prompt as a comment (can be multi-line)
            for line in prompt.splitlines():
                f_out.write(f"--{line}\n")
            f_out.write("\n")
            f_out.write(sql.rstrip() + "\n")
            f_out.write("--############################\n")
            # optional extra blank line between blocks
            f_out.write("\n")

def main():
    prompts_file = "samples/samples.txt"
    output_file = "results/queries.txt"

    prompts = load_prompts(prompts_file)
    if not prompts:
        print(f"No prompts found in {prompts_file}")
        return

    write_queries(prompts, output_file)

    print(f"Done. Results written to {output_file}")

if __name__ == "__main__":
    main()