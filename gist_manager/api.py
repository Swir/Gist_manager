import os

import requests
from PyQt5 import QtCore

from .config import (
    API_BASE,
    REQUEST_TIMEOUT,
    SETTINGS_APPLICATION,
    SETTINGS_ORGANIZATION,
)


class ApiError(RuntimeError):
    pass


class TokenStore:
    @staticmethod
    def settings():
        return QtCore.QSettings(SETTINGS_ORGANIZATION, SETTINGS_APPLICATION)

    @classmethod
    def token(cls):
        value = cls.settings().value("github_token", "", type=str).strip()
        return value or os.getenv("GITHUB_TOKEN", "").strip()

    @classmethod
    def save(cls, token):
        cls.settings().setValue("github_token", token.strip())

    @classmethod
    def clear(cls):
        cls.settings().remove("github_token")


class GitHubGistApi:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "Swir-Gist-Manager/2.0",
            }
        )

    def _request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        try:
            response = self.session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise ApiError(f"Błąd połączenia z GitHub: {exc}") from exc

        if response.status_code >= 400:
            try:
                message = response.json().get("message", response.text)
            except ValueError:
                message = response.text or f"HTTP {response.status_code}"
            raise ApiError(f"GitHub API: {message}")
        return response

    def list_gists(self):
        gists = []
        for page in range(1, 11):
            response = self._request(
                "GET",
                f"{API_BASE}/gists",
                params={"per_page": 100, "page": page},
            )
            batch = response.json()
            gists.extend(batch)
            if len(batch) < 100:
                break
        return gists

    def create_gist(self, filename, content, description, public):
        payload = {
            "description": description,
            "public": public,
            "files": {filename: {"content": content}},
        }
        return self._request("POST", f"{API_BASE}/gists", json=payload).json()

    def delete_gist(self, gist_id):
        self._request("DELETE", f"{API_BASE}/gists/{gist_id}")
