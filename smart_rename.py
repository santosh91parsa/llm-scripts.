#!/usr/bin/env python3
"""
Smart Content-Based File Renamer (Single-file utility)

Description:
    Inspects text files in a directory, reads initial content, and prompts an LLM
    to generate meaningful, clean snake_case filenames (e.g., `scan_001.txt` -> `aws_march_invoice.txt`).

Usage:
    python smart_rename.py --dir ./my_files --dry-run   # Preview changes without renaming
    python smart_rename.py --dir ./my_files             # Apply renames
"""

import os
import glob
import re
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def clean_filename(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^\w\-_]", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "untitled"


def main():
    parser = argparse.ArgumentParser(
        description="Intelligently rename files based on their content."
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Directory containing files to rename (default: current directory)",
    )
    parser.add_argument(
        "--pattern",
        default="*.txt",
        help="Glob pattern for files to target (default: *.txt)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Display proposed renames without changing files",
    )
    parser.add_argument(
        "--model",
        default="deepseek-v4-flash",
        help="Model identifier to use (default: deepseek-v4-flash)",
    )
    args = parser.parse_args()

    files = glob.glob(os.path.join(args.dir, args.pattern))
    if not files:
        print(f"No files matching '{args.pattern}' in '{args.dir}'.")
        return

    client = OpenAI()
    print(f"Analyzing {len(files)} file(s)... (dry-run: {args.dry_run})\n")

    for file_path in files:
        old_name = os.path.basename(file_path)
        ext = os.path.splitext(old_name)[1]

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content_sample = f.read(3000)

        if not content_sample.strip():
            print(f"Skipping empty file: {old_name}")
            continue

        prompt = (
            "Suggest a concise, descriptive filename (maximum 5 words, snake_case, no file extension) "
            "that clearly describes what this document is about:\n\n"
            f"{content_sample}"
        )

        try:
            res = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": prompt}],
            )
            raw_title = res.choices[0].message.content.strip()
            new_name = clean_filename(raw_title) + ext
            new_path = os.path.join(args.dir, new_name)

            if old_name == new_name:
                print(f"  - {old_name} (already optimal)")
                continue

            print(f"  {old_name}  -->  {new_name}")
            if not args.dry_run:
                os.rename(file_path, new_path)
        except Exception as e:
            print(f"  Error processing {old_name}: {e}")

    print("\nCompleted!")


if __name__ == "__main__":
    main()
