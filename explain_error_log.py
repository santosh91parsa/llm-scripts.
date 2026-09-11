#!/usr/bin/env python3
"""
Terminal Error Log & Stacktrace Diagnoser (Single-file utility)

Description:
    Accepts piped terminal output, stack traces, or log files via standard input (stdin)
    and uses an LLM to explain the root cause and provide actionable fixes.

Usage:
    cat error.log | python explain_error_log.py
    docker logs my-container 2>&1 | python explain_error_log.py
    python my_broken_script.py 2>&1 | python explain_error_log.py
"""

import sys
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Diagnose error logs and stack traces piped from stdin."
    )
    parser.add_argument(
        "--model",
        default="deepseek-v4-flash",
        help="Model identifier to use (default: deepseek-v4-flash)",
    )
    args = parser.parse_args()

    if sys.stdin.isatty():
        print("Usage: Pipe error logs into this script via stdin.")
        print("Example: cat error.log | python explain_error_log.py")
        sys.exit(1)

    raw_log = sys.stdin.read().strip()
    if not raw_log:
        print("Received empty input from stdin.")
        sys.exit(0)

    # Focus on the most recent part of the log if very long
    max_chars = 10000
    log_content = raw_log[-max_chars:]

    prompt = (
        "You are an expert system engineer and troubleshooter. "
        "Analyze this error log / stacktrace and provide:\n"
        "1. Root Cause Summary (1-2 sentences)\n"
        "2. Key Diagnostic Clues\n"
        "3. Recommended Fix / Command(s) to run to resolve it\n\n"
        f"--- LOG START ---\n{log_content}\n--- LOG END ---"
    )

    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": prompt}],
        )
        print("\n" + response.choices[0].message.content.strip() + "\n")
    except Exception as e:
        print(f"Error communicating with LLM API: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
