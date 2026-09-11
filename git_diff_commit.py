#!/usr/bin/env python3
"""
Auto Git Commit Message Generator (Single-file utility)

Description:
    Inspects staged git changes (`git diff --staged`) and prompts an LLM
    to generate a concise, conventional commit message with an optional body.

Usage:
    git add .
    python git_diff_commit.py
    python git_diff_commit.py --commit          # Auto-commits without confirmation
    python git_diff_commit.py --model gpt-4o-mini
"""

import sys
import subprocess
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Generate a conventional git commit message from staged changes."
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Automatically run `git commit -m` with the generated message",
    )
    parser.add_argument(
        "--model",
        default="deepseek-v4-flash",
        help="Model identifier to use (default: deepseek-v4-flash)",
    )
    args = parser.parse_args()

    try:
        diff = subprocess.check_output(
            ["git", "diff", "--staged"], text=True
        ).strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        sys.exit(1)

    if not diff:
        print("No staged changes found. Run `git add <files>` first.")
        sys.exit(0)

    # Truncate diff if excessively large
    max_chars = 12000
    truncated_diff = diff[:max_chars]
    if len(diff) > max_chars:
        truncated_diff += "\n\n[...diff truncated for context length...]"

    prompt = (
        "You are an expert software developer. Generate a clean conventional commit message "
        "for the following staged git diff. Format with a single-line title (e.g. `feat(scope): summary` "
        "or `fix(scope): summary`), followed by a blank line and brief bullet points if needed. "
        "Do not include markdown code fence formatting (no backticks around the entire message).\n\n"
        f"{truncated_diff}"
    )

    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": prompt}],
        )
        commit_msg = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error communicating with LLM API: {e}")
        sys.exit(1)

    print("\n--- Proposed Commit Message ---")
    print(commit_msg)
    print("--------------------------------\n")

    if args.commit:
        subprocess.run(["git", "commit", "-m", commit_msg])
    else:
        choice = input("Commit with this message? [y/N/e (edit)]: ").strip().lower()
        if choice == "y":
            subprocess.run(["git", "commit", "-m", commit_msg])
        elif choice == "e":
            edited_msg = input("Enter customized commit message: ").strip()
            if edited_msg:
                subprocess.run(["git", "commit", "-m", edited_msg])


if __name__ == "__main__":
    main()
