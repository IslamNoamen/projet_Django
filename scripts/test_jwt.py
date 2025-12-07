"""
Quick helper script to exercise the JWT endpoints and the protected Session API.

Usage:
    1. Ensure the Django dev server is running (default http://127.0.0.1:8000).
    2. Activate the virtualenv and run:
           venv\Scripts\python scripts\test_jwt.py
    3. Adjust BASE_URL, credentials, or endpoints as needed.
"""

import sys
from typing import Dict

import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN_URL = f"{BASE_URL}/api/token/"
REFRESH_URL = f"{BASE_URL}/api/token/refresh/"
SESSION_URL = f"{BASE_URL}/api/session/sessions/"

# Update these credentials to an existing Django user account
CREDENTIALS = {
    "username": "apitester",
    "password": "SuperSecret123!",
}


def fetch_tokens() -> Dict[str, str]:
    response = requests.post(TOKEN_URL, data=CREDENTIALS)
    response.raise_for_status()
    return response.json()


def refresh_access_token(refresh_token: str) -> Dict[str, str]:
    response = requests.post(REFRESH_URL, data={"refresh": refresh_token})
    response.raise_for_status()
    return response.json()


def fetch_sessions(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SESSION_URL, headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    try:
        tokens = fetch_tokens()
        print("Initial tokens:", tokens)

        refreshed = refresh_access_token(tokens["refresh"])
        print("Refreshed access token payload:", refreshed)

        sessions = fetch_sessions(tokens["access"])
        print("Session list response:", sessions)

    except requests.HTTPError as exc:
        print("HTTPError:", exc.response.status_code, exc.response.text)
        sys.exit(1)
    except Exception as exc:
        print("Unexpected error:", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()

