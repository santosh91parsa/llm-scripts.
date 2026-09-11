#!/usr/bin/env python3
"""
Unstructured Text to JSON Extractor (Single-file utility)

Description:
    Reads raw unstructured text (emails, invoices, contracts, receipts)
    and extracts structured JSON conforming to specified fields using
    LLM JSON mode.

Usage:
    python unstructured_to_json.py --input raw_email.txt
    python unstructured_to_json.py --input invoice.txt --schema "invoice_id, vendor, total_amount, due_date"
"""

import sys
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured JSON from raw text files."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input text file",
    )
    parser.add_argument(
        "--schema",
        default="key entities, dates, names, amounts, summary",
        help="Comma-separated fields or description of the schema to extract",
    )
    parser.add_argument(
        "--model",
        default="deepseek-v4-flash",
        help="Model identifier to use (default: deepseek-v4-flash)",
    )
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file '{args.input}': {e}")
        sys.exit(1)

    prompt = (
        f"Extract the following fields from the text below:\n"
        f"Fields to extract: {args.schema}\n\n"
        f"Return ONLY valid JSON matching this schema.\n\n"
        f"Text:\n{text}"
    )

    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=args.model,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        parsed = json.loads(response.choices[0].message.content)
        print(json.dumps(parsed, indent=2))
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
