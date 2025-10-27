#!/usr/bin/env python3
import requests
import argparse
import sys
import json
import csv
from pathlib import Path
from typing import List, Set

VERSION = "PyBuster 1.1"

def build_candidate_urls(domain: str, word: str, exts: List[str], subs_only: bool = False) -> List[str]:
    candidates = []
    base_candidates = []
    domain = domain.rstrip('/')
    if domain.startswith(("http://", "https://")):
        base_candidates = [domain]
    else:
        base_candidates = [f"https://{domain}", f"http://{domain}"]
    # add raw word (directory)
    for base in base_candidates:
        candidates.append(f"{base}/{word}")
    # add word with extensions unless subs_only is requested
    if not subs_only:
        for ext in exts:
            # normalize extension (user may pass ".php" or "php")
            e = ext if ext.startswith('.') else f".{ext}"
            for base in base_candidates:
                candidates.append(f"{base}/{word}{e}")
    return candidates

def load_existing_urls(path: Path) -> Set[str]:
    """Load existing URLs from a file, trying raw/json/csv heuristics."""
    urls = set()
    if not path.exists():
        return urls
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return urls
    text = text.strip()
    if not text:
        return urls
    # Try JSON array
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
    # Try CSV: look for lines with comma and "url" header
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
                        # fallback: every line first column is URL
                        for r in rows:
                            if r:
                                urls.add(r[0].strip())
        except Exception:
            pass
    # Fallback: plain lines
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
        # try to load existing array, extend it
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
        # if file has content, don't write header
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

def main():
    parser = argparse.ArgumentParser(description="Simple directory buster")
    parser.add_argument("-f", "--file", required=True, help="Path to wordlist")
    parser.add_argument("-o", "--output", required=False, default="directories.txt",
                        help="Output file (default: directories.txt)")
    parser.add_argument("domain", help="Target domain (example.com or http(s)://example.com[:port])")
    # New flags requested:
    parser.add_argument("--ext", required=False, default="", help="Comma-separated extensions to try (e.g. .php,.html,js)")
    parser.add_argument("--resume", action="store_true", help="Skip words already present in the output file")
    parser.add_argument("--append", action="store_true", help="Append to output file instead of overwriting")
    parser.add_argument("--output-format", choices=['raw', 'json', 'csv'], default='raw',
                        help="Output format: raw (one url per line), json (array of objects), csv (url,status). Default: raw")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    # New subs-only flag (-s / --subs-only)
    parser.add_argument("-s", "--subs-only", action="store_true", help="Only try raw directory paths (no extensions) like /admin, /api, /etc")
    args = parser.parse_args()

    if args.resume and not args.append:
        args.append = True


    if args.version:
        print(VERSION)
        sys.exit(0)

    wordlist_path = Path(args.file)
    out_path = Path(args.output)
    domain = args.domain.rstrip('/')

    if not wordlist_path.is_file():
        print(f"Wordlist file not found: {wordlist_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with wordlist_path.open('r', encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Failed to read wordlist: {e}", file=sys.stderr)
        sys.exit(1)

    # parse extensions
    exts = []
    if args.ext:
        for e in args.ext.split(','):
            e = e.strip()
            if e:
                # store without duplicate dots; later normalized
                exts.append(e)

    # if subs-only was requested, ignore any extensions the user passed
    if args.subs_only:
        exts = []

    # load existing urls if resume requested
    seen = set()
    if args.resume:
        seen = load_existing_urls(out_path)
        if seen:
            print(f"[RESUME] Loaded {len(seen)} existing entries from {out_path}")

    found_dirs = []
    print(f"Starting scan on {domain} with {len(words)} entries...")

    for word in words:
        # build candidates (includes extensions unless subs-only is set)
        candidates = build_candidate_urls(domain, word, exts, subs_only=args.subs_only)

        # For each candidate URL try once; break on first successful response (<400)
        for url in candidates:
            if args.resume and url in seen:
                # skip URLs we've already recorded
                # don't print error messages for skipped/resumed items
                break
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code < 400:
                    print(f"[FOUND] {url} ({resp.status_code})")
                    entry = {'url': url, 'status': resp.status_code}
                    found_dirs.append(entry)
                    seen.add(url)
                    break  # stop trying other schemes/extensions for this word
            except requests.RequestException:
                # Ignore failed requests (timeouts, DNS failures, etc.)
                pass

    # Save results according to chosen format and append/overwrite behavior
    try:
        if args.output_format == 'raw':
            # raw requires writing only URLs per line
            save_results_raw(out_path, found_dirs, append=args.append)
        elif args.output_format == 'json':
            save_results_json(out_path, found_dirs, append=args.append)
        elif args.output_format == 'csv':
            save_results_csv(out_path, found_dirs, append=args.append)
    except Exception as e:
        print(f"Failed to write output file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Scan complete. Found {len(found_dirs)} directories. Saved to {out_path}")

if __name__ == "__main__":
    main()
