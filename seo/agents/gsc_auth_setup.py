#!/usr/bin/env python3
"""
One-time setup: generates a GSC OAuth2 refresh token from your Google account.
Run this once locally, then store the printed refresh token as an env var / secret.

Requirements:
    pip install google-auth-oauthlib google-api-python-client

Steps:
    1. Go to console.cloud.google.com -> APIs & Services -> Credentials
    2. Create OAuth 2.0 Client ID  (type: Desktop app, name: "SEO Report")
    3. Download the JSON -> save as seo/credentials/oauth_client.json
    4. Run: python seo/agents/gsc_auth_setup.py
    5. A browser window opens -> log in as benjamin@rosemedicalpavilion.com
    6. Copy the printed refresh_token into your env / GitHub secret GSC_REFRESH_TOKEN
"""
import json, os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), "../credentials/oauth-client.json")

def main():
    if not os.path.exists(CLIENT_SECRETS):
        print(f"ERROR: OAuth client file not found at {CLIENT_SECRETS}")
        print("Download it from Google Cloud Console -> Credentials -> your Desktop OAuth client -> Download JSON")
        return

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n" + "="*60)
    print("SUCCESS — save these values as secrets/env vars:")
    print("="*60)
    print(f"\nGSC_CLIENT_ID     = {creds.client_id}")
    print(f"GSC_CLIENT_SECRET = {creds.client_secret}")
    print(f"GSC_REFRESH_TOKEN = {creds.refresh_token}")
    print("\nAlso save to seo/credentials/gsc_token.json (do NOT commit this file):")

    token_path = os.path.join(os.path.dirname(__file__), "../credentials/gsc_token.json")
    with open(token_path, "w") as f:
        json.dump({
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "refresh_token": creds.refresh_token,
            "token_uri": "https://oauth2.googleapis.com/token",
        }, f, indent=2)
    print(f"Saved to {token_path}")

if __name__ == "__main__":
    main()
