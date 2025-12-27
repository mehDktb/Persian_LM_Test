import re
import json
from textwrap import dedent
from system_contents.Qwen_sql_system_content import SQL_SYSTEM_PROMPT



INPUT_TXT = "./results/query_getdate.txt"
OUTPUT_JSONL = "dataset/train.jsonl"


def extract_examples(text):
    # Split by the separator
    blocks = re.split(r'--############################\s*', text.strip())

    examples = []
    for block in blocks:
        if not block.strip():
            continue

        lines = block.strip().split('\n')

        question = None
        sql_start_idx = None

        # Find the question: line starting with -- but not containing ####
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('--') and '####' not in stripped:
                question = stripped[2:].strip()  # Remove '--' and extra spaces
                if question:  # Make sure it's not empty
                    sql_start_idx = i + 1
                    break

        if question is None or sql_start_idx is None or sql_start_idx >= len(lines):
            print(f"Warning: Skipped a block without a valid question: {block[:100]}...")
            continue

        # Extract SQL part and dedent it
        sql_lines = lines[sql_start_idx:]
        sql = dedent('\n'.join(sql_lines)).strip()

        # Optional: remove trailing semicolon for cleaner answers
        if sql.endswith(';'):
            sql = sql[:-1].rstrip()

        examples.append({
            "system_prompt": SQL_SYSTEM_PROMPT,
            "question": question,
            "answer": sql
        })

    return examples


# Main execution
if __name__ == "__main__":
    with open(INPUT_TXT, "r", encoding="utf-8") as f:
        raw_text = f.read()

    examples = extract_examples(raw_text)

    print(f"Extracted {len(examples)} examples.")

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as out_file:
        for ex in examples:
            out_file.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Conversion complete! Saved to {OUTPUT_JSONL}")
    print("You can now use this file as TRAIN_FILE in your fine-tuning script.")