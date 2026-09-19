import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

def main():
    # step 1: read tickets in folder /root/tickets
    file = Path("/root/tickets")
    outdir = Path("/root/triaged")
    outdir.mkdir(parents=True, exist_ok=True)
    for f in file.glob("*"):
        t = f.read_text()
        messages=[
            {"role":"system","content":"classify it and return JSON with at least these two fields: category - one of billing, technical, account, or other priority - one of low, medium, or high"},
            {"role":"user","content": t}
        ]

        response=client.chat.completions.create(
            model="claude-sonnet-5",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0,
        )
        result = response.choices[0].message.content
        parsed = json.loads(result)
        if not {"category", "priority"} <= parsed.keys():
            raise ValueError(f"Missing category/priority in classification for {f.name}: {result}")
        outname = outdir / f"{f.stem}.json"
        outname.write_text(result)
        print(f"Saved classification for {f.name} ---> {outname}")


if __name__ == "__main__":
    main()
