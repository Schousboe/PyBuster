# PyBuster


## Overview
PyBuster is a lightweight, opinionated directory buster written in Python for authorized penetration testing and security assessments. It probes a target for directory paths (and optional file extensions) using a user-supplied wordlist and writes discoveries to an output file.

<br/>


> [!WARNING]  
> Use only against targets you have explicit written permission to  test. Misuse may be illegal.

---

## Features

- Probes HTTP/HTTPS (auto-fallback when no scheme is provided)

- Try raw directories and optional file extensions

- Output formats: raw, JSON, CSV

- Resume mode (skip already-recorded URLs)

- Append mode (preserve previous results)

- Subs-only mode to only try directory paths like /admin, /login etc.

- Scan many different domains in one with `-mT`

---

## Quick install

```bash
git clone github.com/Schousboe/PyBuster.git
```

---

## How to use


### Bare bones

```bash
python3 PyBuster.py -f path/to/wordlist.txt website.com
```
> This returns the raw data in a file called ***directories.txt***
 
### Searching for path's with the extensions .php, .html and outputting the answer as JSON data

```bash
python3 PyBuster.py -f path/to/wordlist.txt -x .php,.html 
--output-format json -o results.json example.com
```
> This returns all php and html files in JSON format to a file called ***results.json***

---

## Supported flags

- **-f, --file** - path to wordlist (required)

- **-o, --output** - output file (default: directories.txt)

- **-x, --ext** - comma separated extensions (e.g. php, html)

- **-d, --dirs-only**- only try directory paths (no extensions)

- **-r, --resume** - skip URLs already present in output

- **-a, --append** - append to output file instead of overwrite

- **-oF, --output-format** - raw / json / csv

- **mT, --multiple-targets** - file with multiple domains (one per line)