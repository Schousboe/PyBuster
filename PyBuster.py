#!/usr/bin/env python3
import requests
import argparse
import sys
import json
import csv
import subprocess
from pathlib import Path
from typing import List, Set

def get_version():
    try:
        tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
        return f"PyBuster {tag}"
    except Exception:
        return "PyBuster (dev)"

VERSION = get_version()

def build_candidate_urls(domain: str, word: str, exts: List[str], dirs_only: bool = False) -> List[str]:
    candidates = []
    base_candidates = []
    domain = domain.rstrip('/')
    if domain.startswith(("http://", "https://")):
        base_candidates = [domain]
    else:
        base_candidates = [f"https://{domain}", f"http://{domain}"]
    for base in base_candidates:
        candidates.append(f"{base}/{word}")
    if not dirs_only:
        for ext in exts:
            e = ext if ext.startswith('.') else f".{ext}"
            for base in base_candidates:
                candidates.append(f"{base}/{word}{e}")
    return candidates

def load_existing_urls(path: Path) -> Set[str]:
    urls = set()
    if not path.exists():
        return urls
    try:
        text = path.read_text(encoding="utf-8").strip()
    except Exception:
        return urls
    if not text:
        return urls
    if text.startswith('['):
        try:
            arr = json.loads(text)
            if isinstance(arr, list):
                for item in arr:
                    if isinstance(item, dict) and 'url' in item:
                        urls.add(item['url'])
                    elif isinstance(item, str):
                        urls.add(item)
        except Exception:
            pass
    if not urls:
        try:
            with path.open(newline='', encoding="utf-8") as fh:
                reader = csv.reader(fh)
                rows = list(reader)
                if rows:
                    header = [h.strip().lower() for h in rows[0]]
                    if 'url' in header:
                        idx = header.index('url')
                        for r in rows[1:]:
                            if len(r) > idx:
                                urls.add(r[idx].strip())
                    else:
                        for r in rows:
                            if r:
                                urls.add(r[0].strip())
        except Exception:
            pass
    if not urls:
        for line in text.splitlines():
            line = line.strip()
            if line:
                urls.add(line)
    return urls

def save_results_raw(path: Path, results: List[dict], append: bool):
    mode = 'a' if append else 'w'
    with path.open(mode, encoding="utf-8") as fh:
        for r in results:
            fh.write(r['url'] + "\n")

def save_results_json(path: Path, results: List[dict], append: bool):
    if append and path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except Exception:
            existing = []
        existing.extend(results)
        path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    else:
        path.write_text(json.dumps(results, indent=2), encoding="utf-8")

def save_results_csv(path: Path, results: List[dict], append: bool):
    mode = 'a' if append else 'w'
    write_header = True
    if append and path.exists():
        try:
            if path.stat().st_size > 0:
                write_header = False
        except Exception:
            write_header = True
    with path.open(mode, newline='', encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if write_header:
            writer.writerow(['url', 'status'])
        for r in results:
            writer.writerow([r.get('url', ''), r.get('status', '')])

def scan_domain(domain: str, args):
    wordlist_path = Path(args.file)
    out_path = Path(args.output)
    domain = domain.rstrip('/')

    if not wordlist_path.is_file():
        print(f"[ERROR] Wordlist not found: {wordlist_path}", file=sys.stderr)
        return

    try:
        with wordlist_path.open('r', encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[ERROR] Failed to read wordlist: {e}", file=sys.stderr)
        return

    exts = []
    if args.ext:
        for e in args.ext.split(','):
            e = e.strip()
            if e:
                exts.append(e)

    if args.dirs_only:
        exts = []

    seen = set()
    if args.resume:
        seen = load_existing_urls(out_path)
        if seen:
            print(f"[RESUME] Loaded {len(seen)} entries from {out_path}")

    found_dirs = []
    print(f"\n[SCAN] Target: {domain} ({len(words)} words)\n")

    for word in words:
        candidates = build_candidate_urls(domain, word, exts, dirs_only=args.dirs_only)
        for url in candidates:
            if args.resume and url in seen:
                break
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code < 400:
                    print(f"[FOUND] {url} ({resp.status_code})")
                    entry = {'url': url, 'status': resp.status_code}
                    found_dirs.append(entry)
                    seen.add(url)
                    break
            except requests.RequestException:
                pass

    try:
        if args.output_format == 'raw':
            save_results_raw(out_path, found_dirs, append=args.append)
        elif args.output_format == 'json':
            save_results_json(out_path, found_dirs, append=args.append)
        elif args.output_format == 'csv':
            save_results_csv(out_path, found_dirs, append=args.append)
    except Exception as e:
        print(f"[ERROR] Failed to write output: {e}", file=sys.stderr)

    print(f"[DONE] {domain}: {len(found_dirs)} results written to {out_path}")

def read_targets_file(path: Path) -> List[str]:
    """Read a file with one domain per line. Ignore blank lines & comments (#)."""
    targets = []
    if not path.is_file():
        raise FileNotFoundError(f"Targets file not found: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        targets.append(line)
    return targets

def main():
    parser = argparse.ArgumentParser(description="PyBuster - Simple directory buster")
    parser.add_argument("-f", "--file", required=True, help="Path to wordlist")
    parser.add_argument("-o", "--output", default="directories.txt", help="Output file (default: directories.txt)")
    parser.add_argument("-mT", "--multiple-targets", dest="targets", help="File containing multiple domains (one per line)")
    parser.add_argument("-x", "--ext", default="", help="Comma-separated extensions (e.g. .php,.html,js)")
    parser.add_argument("-r", "--resume", action="store_true", help="Skip words already present in the output file")
    parser.add_argument("-a", "--append", action="store_true", help="Append instead of overwrite")
    parser.add_argument("-oF", "--output-format", choices=['raw', 'json', 'csv'], default='raw', help="Output format")
    parser.add_argument("-d", "--dirs-only", action="store_true", help="Only try directories (no extensions)")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("domain", nargs="?", help="Target domain (example.com or http(s)://example.com[:port])")

    args = parser.parse_args()

    if args.version:
        print(VERSION)
        sys.exit(0)

    if args.resume and not args.append:
        args.append = True

    if not args.domain and not args.targets:
        print("[ERROR] You must specify either a single domain or --multiple-targets file.", file=sys.stderr)
        sys.exit(1)

    if args.targets:
        targets_path = Path(args.targets)
        if not targets_path.exists():
            print(f"[ERROR] Targets file not found: {targets_path}", file=sys.stderr)
            sys.exit(1)
        try:
            domains = read_targets_file(targets_path)
        except Exception as e:
            print(f"[ERROR] Failed to read targets file: {e}", file=sys.stderr)
            sys.exit(1)
        if not domains:
            print(f"[ERROR] No valid domains in {targets_path}", file=sys.stderr)
            sys.exit(1)
        print(f"[+] Loaded {len(domains)} targets from {targets_path}")
        for i, domain in enumerate(domains, start=1):
            print(f"\n=== [{i}/{len(domains)}] {domain} ===")
            scan_domain(domain, args)
        print("\n[+] Multi-target scan complete!")
    else:
        scan_domain(args.domain, args)

if __name__ == "__main__":
    main()
