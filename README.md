# llm-scripts

> **Ad-hoc useful leverage LLM-based python scripts.**

A curated collection of standalone, single-file Python automation utilities leveraging LLM APIs (DeepSeek, OpenAI, etc.) for daily developer workflows, batch file processing, and terminal productivity.

---

## ⚡ Design Principles

* **Single-File Standalone**: Every script in this repository is 100% self-contained. No local cross-module imports—you can copy, curl, or run any individual script anywhere.
* **CLI-Ready**: All scripts include standard argument parsing (`--help`, configurable input/output paths, and model flags).
* **Provider Agnostic**: Built on the OpenAI-compatible standard interface, allowing drop-in compatibility with OpenAI, DeepSeek, OpenRouter, or local engines (Ollama, vLLM).

---

## 📦 Quickstart

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/santosh91parsa/llm-scripts..git
cd llm-scripts.
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env`:
```bash
OPENAI_API_KEY=your_api_key_here

# Optional: Set base URL for DeepSeek or local endpoint
# OPENAI_BASE_URL=https://api.deepseek.com/v1
```

---

## 🛠 Script Catalog

| Script | Category | Purpose | Quick Command |
| :--- | :--- | :--- | :--- |
| [`summarize_inbox.py`](summarize_inbox.py) | Batch Processing | Batch 1-sentence summarization of text files | `python summarize_inbox.py --inbox ./inbox --out ./summaries` |
| [`git_diff_commit.py`](git_diff_commit.py) | Git Automation | Generates conventional commit message from staged diff | `python git_diff_commit.py --commit` |
| [`explain_error_log.py`](explain_error_log.py) | CLI / Debugging | Diagnoses piped error logs & suggests terminal fixes | `cat error.log \| python explain_error_log.py` |
| [`unstructured_to_json.py`](unstructured_to_json.py) | Data Extraction | Extracts structured JSON conforming to custom schema | `python unstructured_to_json.py --input raw.txt` |
| [`smart_rename.py`](smart_rename.py) | Organization | Renames mystery files based on their actual content | `python smart_rename.py --dir ./downloads --dry-run` |

---

## 📖 Usage Guides

### 1. Batch Summarizer (`summarize_inbox.py`)
Scans an inbox directory for raw `.txt` files, generates a one-sentence summary for each using an LLM, and saves the outputs preserving filenames.
```bash
python summarize_inbox.py --inbox ./inbox --out ./summaries --model deepseek-v4-flash
```

### 2. Auto Git Commit (`git_diff_commit.py`)
Inspects your staged git changes (`git diff --staged`) and creates a concise conventional commit message.
```bash
git add .
python git_diff_commit.py          # Interactive prompt to accept or edit
python git_diff_commit.py --commit # Auto-commit immediately
```

### 3. Error Log Diagnoser (`explain_error_log.py`)
Pipe logs or stack traces directly into the script to get root-cause analysis and actionable terminal commands.
```bash
# Pipe any error log
cat crash.log | python explain_error_log.py

# Pipe docker or script outputs
docker logs web-api 2>&1 | python explain_error_log.py
python manage.py runserver 2>&1 | python explain_error_log.py
```

### 4. Unstructured Text to JSON (`unstructured_to_json.py`)
Converts messy, unstructured documents (emails, invoices, receipts) into structured JSON.
```bash
python unstructured_to_json.py --input invoice.txt --schema "invoice_id, vendor, total_amount, due_date"
```

### 5. Smart File Renamer (`smart_rename.py`)
Reads the first few paragraphs of unorganized text files and renames them to clean, descriptive snake_case titles.
```bash
# Preview what files would be renamed
python smart_rename.py --dir ./my_notes --dry-run

# Execute rename
python smart_rename.py --dir ./my_notes
```

---

## 📄 License
MIT
