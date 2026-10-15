"""Environment configuration.

Loaded once per test session by a session-scoped fixture in conftest.py.
`Config.load()` is a @classmethod: it sets *class* variables, so every test
and page object reads the same values without creating a Config object.
"""
import json
import os
from pathlib import Path

ENV_DIR = Path(__file__).parent / "environments"


class Config:
    env: str | None = None
    ui_base_url: str | None = None
    api_base_url: str | None = None
    api_username: str | None = None
    api_password: str | None = None
    timeout_ms: int = 10_000

    @classmethod
    def load(cls, env: str) -> type["Config"]:
        path = ENV_DIR / f"{env}.json"
        if not path.exists():
            available = ", ".join(p.stem for p in ENV_DIR.glob("*.json"))
            raise FileNotFoundError(f"Unknown env '{env}'. Available: {available}")

        data = json.loads(path.read_text())
        cls.env = env
        cls.ui_base_url = data["ui_base_url"]
        cls.api_base_url = data["api_base_url"]
        # Secrets: environment variables (e.g. CI secrets) win over the JSON file.
        cls.api_username = os.getenv("API_USERNAME", data["api_username"])
        cls.api_password = os.getenv("API_PASSWORD", data["api_password"])
        cls.timeout_ms = data.get("timeout_ms", cls.timeout_ms)
        return cls
