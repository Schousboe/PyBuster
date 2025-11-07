<div align="center">
 <h1>PyBuster</h1>
  <img src="docs/images/logo.png" alt="PyBuster logo"/>
  <p><b>Fast, lightweight and secure directory brute-forcer written in Python</b></p>

   ![PyBuster-stats](https://github-readme-stats.vercel.app/api/pin/?username=Schousboe&repo=PyBuster&theme=dark&icon_color=00FF88")

  <img src="https://img.shields.io/badge/version-1.1-blue.svg" alt="version">
  <img src="https://img.shields.io/github/license/Schousboe/PyBuster?color=blue" alt="license">
  <img src="https://img.shields.io/github/issues/Schousboe/PyBuster?color=green" alt="issues">

  <br/>

  <p align="center">
    <a href="#features">Features</a> 
    •
    <a href="#install">Install</a> 
    •
    <a href="#usage">Usage</a> 
    •
    <a href="#flags">Flags</a> 
    •
    <a href="LICENSE">License</a>

   Love the project? Please consider leaving a star 🌟
  </p>
</div>

<br/>

<div align="center">
<strong>PyBuster</strong> is a high-performance, lightweight, and secure <strong>directory brute-forcing tool</strong> written in Python — designed for <strong>authorized penetration testing</strong>, <strong>bug bounty hunting</strong>, and <strong>web reconnaissance</strong>.  
It aims to provide a minimal yet powerful CLI interface similar to Gobuster, with smart options for scanning, output and extensions while still keeping core functionality.
</div>

---

## Important notices!

> [!IMPORTANT]
> Please leave an issue if you have a feature suggestion or a bug appears!

> [!IMPORTANT]
> If you have a suggestion for a new feature, please contribute. There is more information about how to contribute in our [contributing guidelines](CONTRIBUTING.md)

> [!CAUTION]  
> Use only against targets you have explicit permission to test. Misuse may be illegal.

## Features

- Probes HTTP/HTTPS (auto-fallback when no scheme is provided)

- Try raw directories and optional file extensions

- Output formats: raw, JSON, CSV

- Resume mode (skip already-recorded URLs)

- Append mode (preserve previous results)

- Subs-only mode to only try directory paths like /admin, /login etc.

- Scan many different domains in one with `-mT`

- Scan specific ports with `-p`

---

## Install


1. Install the project
```bash
git clone github.com/Schousboe/PyBuster.git
```
<br/>

2. Install requirements
```bash
pip install -r requirements.txt
```
<br/>

3. Run a simple script and boom!
```bash
python3 PyBuster.py -f wordlists/common.txt example.com
```

---

## Usage

#### Basic scan

```bash
python3 PyBuster.py -f path/to/wordlist.txt website.com
```
> This returns the raw data in a file called ***directories.txt***
 
#### Searching for path's with the extensions .php, .html and outputting the answer as JSON data

```bash
python3 PyBuster.py -f path/to/wordlist.txt -x .php,.html 
-oF json -o results.json example.com
```
> This returns all php and html files in JSON format to a file called ***results.json***

#### Searching for directories, from multiple sub-domains, with the extension .log, outputting as CSV to a file already containing data.

```bash
python3 PyBuster.py -f path/to/wordlist.txt -x .log -oF csv -o /path/to/output.csv --resume -d -mT path/to/targets.txt
```

---

## Flags

- **-f, --file** - path to wordlist (required)

- **-o, --output** - output file (default: directories.txt)

- **-x, --ext** - comma separated extensions (e.g. php, html)

- **-d, --dirs-only**- only try directory paths (no extensions)

- **-r, --resume** - skip URLs already present in output

- **-a, --append** - append to output file instead of overwrite

- **-oF, --output-format** - raw / json / csv

- **-mT, --multiple-targets** - file with multiple domains (one per line)

- **-p, --ports** - comma-separated ports to scan (e.g. 80,443,8080)


## Contributing

Contributions are ***welcome*** but please see our [contributing guidelines](CONTRIBUTING.md) first, before opening a pull request

## License

This project is distributed under the CC0 1.0 Universal license.
This means you are free to copy, modify and use PyBuster for any purpose, without restriction

<br/>
<div align="center"> <sub>Built with ❤️ by <a target="_blank" href="https://github.com/Schousboe">Schousboe</a> — For ethical hacking & secure web testing</sub> </div>