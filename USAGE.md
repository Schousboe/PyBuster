# USAGE.md — PyBuster Usage Guide

#### This document explains common usage patterns, examples, and troubleshooting for **PyBuster**.

> [!WARNING]
> Only run PyBuster against targets you have explicit written permission to test.

---

## Basic command

```bash
python3 PyBuster.py -f path/to/wordlist.txt -o path/to/output.txt example.com
```
* Default output file is `directories.txt` if `-o` is omitted.

---

## Common examples

### 1) Barebones

```bash
python3 PyBuster.py -f wordlists/common.txt example.com
```

### 2) Subdirectories only (no extensions)

```bash
python3 PyBuster.py -f wordlists/common.txt -s -o subs.txt example.com
```

### 3) Try extensions and save JSON

```bash
python3 PyBuster.py -f wordlists/common.txt --ext .php,.html --output-format json -o results.json example.com
```

The `--ext` list accepts values with or without a leading dot; `.php` and `php` are normalized the same.

### 4) Resume an interrupted run (safe — won't delete previous results)

```bash
python3 PyBuster.py -f wordlists/biglist.txt --resume -o results.txt example.com
```

`--resume` loads URLs from `results.txt` and **skips** those when scanning. It also implicitly enables appending so your previous file is preserved.

---

## Output formats

* `raw` — one URL per line (default). Good for piping to other tools. 
* `json` — array of objects: `[{"url":"http://...","status":200}, ...]`.
* `csv` — CSV rows `url,status` with a header when creating a new file.

---

## Flags quick reference

* `-f, --file <path>` (required) — wordlist file, one word per line.
* `-o, --output <path>` — output file (default `directories.txt`).
* `--ext <comma list>` — extensions to try (e.g. `.php,.html`).
* `-s, --subs-only` — only try raw directory paths (no extensions).
* `--resume` — load existing output and skip those URLs (implies append).
* `--append` — append to the output file instead of overwriting.
* `--output-format` — `raw|json|csv`.
* `--version` — print version and exit.

---

## Troubleshooting

* **Duplicates in output** — resume matching is exact string based. `http://` vs `https://` are treated as different URLs.
* **IndentationError / unexpected indent** — convert all tabs to spaces (4 spaces per indent) in `PyBuster.py`.

