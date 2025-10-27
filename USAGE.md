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
> This will return a list of sub-domain's and directories to the default ***directories.txt***

### 2) Subdirectories only (no extensions)

```bash
python3 PyBuster.py -f wordlists/common.txt -d -o subs.txt example.com
```
> This will return a list of directory path's in a file called ***subs.txt***

### 3) Try extensions and save JSON

```bash
python3 PyBuster.py -f wordlists/common.txt --ext php, html --output-format json -o results.json example.com
```
> This will return all extension's containing php and html in json format to a file called ***results.json***

> [!NOTE] 
> The `--ext` list accepts values with or without a leading dot; `.php` and `php` are normalized the same.

### 4) Resume an interrupted run (safe — won't delete previous results)

```bash
python3 PyBuster.py -f wordlists/biglist.txt --resume -o results.txt example.com
```
> This will return all subdomain's and directory path's to a file called results.txt if they aren't already there

### 5) Search directories from multiple domain's 

```bash
python3 PyBuster.py -f path/to/wordlist -mT path/to/targets.txt -oF json -o results.json -d
```
> This will return all directories from the domain's in path/to/targets.txt in json format to a file called ***result.json***

---

## Output formats

* `raw` — one URL per line (default). Good for piping to other tools. 
* `json` — array of objects: `[{"url":"http://...","status":200}, ...]`.
* `csv` — CSV rows `url,status` with a header when creating a new file.

---

## How to use the flags

- `-f, --file /path/to/wordlist.txt` - path to wordlist (required)

- `-o, --output /path/to/output` - output file (default: directories.txt)

- `-x, --ext php, html, json` - comma separated extensions (e.g. php, html)

- `-d, --dirs-only`- only try directory paths (no extensions)

- `-r, --resume` - skip URLs already present in output

- `-a, --append` - append to output file instead of overwrite

- `-oF, --output-format json` - raw / json / csv

- `-mT, --multiple-targets /path/to/targets` - file with multiple domains (one per line)

---

## Troubleshooting

* **Duplicates in output** — resume matching is exact string based. `http://` vs `https://` are treated as different URLs.
* **IndentationError / unexpected indent** — convert all tabs to spaces (4 spaces per indent) in `PyBuster.py`.

