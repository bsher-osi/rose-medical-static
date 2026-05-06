#!/usr/bin/env python3
"""Submit all city pages and new blog posts to GSC for indexing via URL Inspection API."""
import os, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CREDS_PATH = Path(__file__).resolve().parents[1] / "credentials" / "gsc_token.json"
SITE = "sc-domain:rosemedicalpavilion.com"
BASE_URL = "https://rosemedicalpavilion.com"

def _creds():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    client_id     = os.environ.get("GSC_CLIENT_ID", "")
    client_secret = os.environ.get("GSC_CLIENT_SECRET", "")
    refresh_token = os.environ.get("GSC_REFRESH_TOKEN", "")
    if not (client_id and client_secret and refresh_token):
        if CREDS_PATH.exists() and CREDS_PATH.stat().st_size > 10:
            tok = json.loads(CREDS_PATH.read_text())
            client_id     = tok.get("client_id", "")
            client_secret = tok.get("client_secret", "")
            refresh_token = tok.get("refresh_token", "")
    creds = Credentials(
        token=None, refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id, client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/webmasters"],
    )
    creds.refresh(Request())
    return creds

def get_urls():
    urls = []
    # All top-level page dirs (city pages, blog posts)
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        if name.startswith(".") or name in {"seo", "wp-content", "wp-includes", "contact_form"}:
            continue
        idx = d / "index.html"
        if idx.exists():
            urls.append(f"{BASE_URL}/{name}/")
    return urls

def main():
    from googleapiclient.discovery import build
    creds = _creds()
    service = build("searchconsole", "v1", credentials=creds)

    urls = get_urls()
    print(f"Submitting {len(urls)} URLs to GSC...")

    submitted = 0
    errors = 0
    for i, url in enumerate(urls):
        try:
            result = service.urlInspection().index().inspect(
                body={"inspectionUrl": url, "siteUrl": SITE}
            ).execute()
            verdict = result.get("inspectionResult", {}).get("indexStatusResult", {}).get("verdict", "?")
            if i % 50 == 0:
                print(f"  [{i}/{len(urls)}] {url} -> {verdict}")
            submitted += 1
            time.sleep(0.5)  # respect rate limits
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  [ERROR] {url}: {e}")

    print(f"\nDone. Submitted {submitted} URLs, {errors} errors.")

if __name__ == "__main__":
    main()
