import json
import os
from pathlib import Path

_CONFIG_PATH = Path.home() / ".skate" / "config.json"

_KNOWN_KEYS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY")


def get_api_key(name: str) -> str | None:
    value = os.environ.get(name)
    if value:
        return value
    if _CONFIG_PATH.exists():
        data: dict[str, str] = json.loads(_CONFIG_PATH.read_text())
        return data.get(name)
    return None


def set_api_key(name: str, value: str) -> None:
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, str] = {}
    if _CONFIG_PATH.exists():
        data = json.loads(_CONFIG_PATH.read_text())
    data[name] = value
    _CONFIG_PATH.write_text(json.dumps(data, indent=2))


def show_config() -> dict[str, str | None]:
    return {key: get_api_key(key) for key in _KNOWN_KEYS}
