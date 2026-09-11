#!/usr/bin/env python3
"""
Batch Text Summarizer (Single-file utility)

Description:
    Scans an inbox directory for text files (*.txt), generates a 1-sentence
    summary for each file using an LLM chat completion model, and writes the
    resulting summary to a target directory preserving the original filenames.

Usage:
    python summarize_inbox.py
    python summarize_inbox.py --inbox ./inbox --out ./summaries --model deepseek-v4-flash
"""

import os
import glob
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Batch summarize text files from an inbox directory using an LLM."
    )
    parser.add_argument(
        "--inbox",
        default="./inbox",
        help="Path to directory containing input .txt files (default: ./inbox)",
    )
    parser.add_argument(
        "--out",
        default="./summaries",
        help="Path to directory where summaries will be saved (default: ./summaries)",
    )
    parser.add_argument(
        "--model",
        default="deepseek-v4-flash",
        help="Model identifier to use (default: deepseek-v4-flash)",
    )
    args = parser.parse_args()

    client = OpenAI()
    os.makedirs(args.out, exist_ok=True)

    files = sorted(glob.glob(os.path.join(args.inbox, "*.txt")))
    if not files:
        print(f"No .txt files found in '{args.inbox}'.")
        return

    print(f"Found {len(files)} file(s) in '{args.inbox}'. Processing with model '{args.model}'...")

    for path in files:
        filename = os.path.basename(path)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        try:
            reply = client.chat.completions.create(
                model=args.model,
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize this in a sentence:\n\n{text}",
                    }
                ],
            )
            summary = reply.choices[0].message.content.strip()
            out_file = os.path.join(args.out, filename)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(summary + "\n")
            print(f"  ✓ {filename} -> {out_file}")
        except Exception as e:
            print(f"  ✗ Error summarizing {filename}: {e}")

    print("Done!")


if __name__ == "__main__":
    main()
