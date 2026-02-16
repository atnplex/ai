#!/usr/bin/env python3
import json
import subprocess
import os
from pathlib import Path
from uuid import uuid4
import time

# --- Configuration ---
NAMESPACE = os.environ.get("NAMESPACE", "C:\\atn")
BWS_BIN = os.path.join(
    os.environ.get("HOME", "C:\\Users\\Alex"), ".antigravity_tools", "bin", "bws.exe"
)
ACCOUNTS_ROOT = os.path.join(
    os.environ.get("HOME", "C:\\Users\\Alex"), ".antigravity_tools"
)
ACCOUNTS_INDEX = os.path.join(ACCOUNTS_ROOT, "accounts.json")
ACCOUNTS_DIR = os.path.join(ACCOUNTS_ROOT, "accounts")

# Key format for Bitwarden Secrets: "GOOGLE_<email>" or "JULES_API_KEY_XX"
SECRET_PREFIXES = ["GOOGLE_", "JULES_API_KEY"]


def log(msg):
    print(f"[sync-accounts] {msg}")


def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        log(f"Error running command: {e.stderr}")
        return None


def fetch_bws_secrets():
    token_file = os.path.join(ACCOUNTS_ROOT, "bws_token.xml")
    token = None
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            raw = f.read().strip()
            if "<S>" in raw and "</S>" in raw:
                token = raw.split("<S>")[1].split("</S>")[0]
            else:
                token = raw

    if not token:
        log("No BWS token found.")
        return []

    log("Fetching secrets from BWS...")
    output = run_command([BWS_BIN, "secret", "list", "--access-token", token])
    if output:
        try:
            secrets = json.loads(output)
            log(f"Fetched {len(secrets)} secrets.")
            return secrets
        except Exception as e:
            log(f"Failed to parse BWS output: {e}")
    return []


def sync_accounts():
    secrets = fetch_bws_secrets()
    if not secrets:
        log("No secrets found to sync.")
        return

    # Load current index
    index = {"version": "2.0", "accounts": [], "current_account_id": None}
    if os.path.exists(ACCOUNTS_INDEX):
        try:
            with open(ACCOUNTS_INDEX, "r") as f:
                index = json.load(f)
        except Exception as e:
            log(f"Failed to load accounts.json: {e}")

    updated = False
    for secret in secrets:
        key = secret.get("key", "")
        is_jules = key.startswith("JULES_API_KEY")
        is_google = key.startswith("GOOGLE_")

        if not (is_google or is_jules):
            continue

        email = ""
        if is_google:
            email = key.replace("GOOGLE_", "").lower()
        elif is_jules:
            email = secret.get("note", "").lower()
            if not email or "@" not in email:
                log(f"Skipping {key}: No valid email in note.")
                continue

        value = secret.get("value")

        # Check if account exists
        existing = next(
            (acc for acc in index["accounts"] if acc["email"] == email), None
        )

        account_id = None
        if existing:
            account_id = existing["id"]
            log(f"Merging secret for: {email} ({account_id})")
        else:
            account_id = str(uuid4())
            log(f"Adding new account from BWS: {email} ({account_id})")
            index["accounts"].append(
                {
                    "id": account_id,
                    "email": email,
                    "name": email.split("@")[0],
                    "disabled": False,
                    "proxy_disabled": False,
                    "created_at": int(time.time()),
                    "last_used": int(time.time()),
                }
            )
            updated = True

        # Write/Update account JSON
        account_file = os.path.join(ACCOUNTS_DIR, f"{account_id}.json")
        account_data = {}
        if os.path.exists(account_file):
            with open(account_file, "r") as f:
                account_data = json.load(f)

        account_data.update(
            {
                "id": account_id,
                "email": email,
            }
        )

        if "token" not in account_data:
            account_data["token"] = {}

        # If it looks like an API key (JULES), store it. If refresh token, store that.
        if value.startswith("AQ."):
            account_data["token"]["api_key"] = value
        else:
            account_data["token"]["refresh_token"] = value

        # Ensure directory exists
        os.makedirs(ACCOUNTS_DIR, exist_ok=True)
        with open(account_file, "w") as f:
            json.dump(account_data, f, indent=2)
            updated = True

    if updated:
        with open(ACCOUNTS_INDEX, "w") as f:
            json.dump(index, f, indent=2)
        log("Sync complete. Account index updated.")
        update_dashboard(index, secrets)
    else:
        log("No changes detected.")


def update_dashboard(index, secrets):
    dashboard_path = os.path.join(NAMESPACE, "ai", "ai", "config", "account_health.md")
    bws_emails = []
    for s in secrets:
        if s.get("key", "").startswith("GOOGLE_"):
            bws_emails.append(s["key"].replace("GOOGLE_", "").lower())
        elif s.get("key", "").startswith("JULES_API_KEY"):
            bws_emails.append(s.get("note", "").lower())

    lines = [
        "# Account Health Dashboard",
        f"\nLast Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "\n| Account | Status | Proxy | Source |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for acc in index["accounts"]:
        email = acc["email"]
        source = "BWS" if email in bws_emails else "Local"
        status = "✅ Active" if not acc.get("disabled") else "❌ Disabled"
        proxy = "✅ Enabled" if not acc.get("proxy_disabled") else "❌ Disabled"
        lines.append(f"| {email} | {status} | {proxy} | {source} |")

    # Add known missing accounts
    if "charlydang6@gmail.com" not in [acc["email"] for acc in index["accounts"]]:
        lines.append(f"| charlydang6@gmail.com | ❌ Missing | ❌ N/A | None |")

    with open(dashboard_path, "w") as f:
        f.write("\n".join(lines))
    log(f"Dashboard updated at {dashboard_path}")


if __name__ == "__main__":
    sync_accounts()
