import asyncio
import os

import pytest

from skate.providers.anthropic import AnthropicProvider
from skate.providers.gemini import GeminiProvider
from skate.providers.ollama import OllamaProvider, is_running
from skate.providers.openai import OpenAIProvider


def test_openai_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("skate.config._CONFIG_PATH", __import__("pathlib").Path("/nonexistent"))

    result = asyncio.run(OpenAIProvider("gpt-4o-mini").run("hello"))

    assert result.error == "OPENAI_API_KEY is not set"
    assert result.output == ""


def test_anthropic_missing_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr("skate.config._CONFIG_PATH", __import__("pathlib").Path("/nonexistent"))

    result = asyncio.run(AnthropicProvider("claude-haiku-4-5-20251001").run("hello"))

    assert result.error == "ANTHROPIC_API_KEY is not set"
    assert result.output == ""


def test_gemini_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr("skate.config._CONFIG_PATH", __import__("pathlib").Path("/nonexistent"))

    result = asyncio.run(GeminiProvider("gemini-1.5-flash").run("hello"))

    assert result.error == "GEMINI_API_KEY is not set"
    assert result.output == ""


def test_ollama_not_running(monkeypatch):
    import httpx

    class _FailClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            raise httpx.ConnectError("refused")

        async def __aexit__(self, *args):
            pass

    monkeypatch.setattr("skate.providers.ollama.httpx.AsyncClient", _FailClient)

    result = asyncio.run(OllamaProvider("ollama/llama3").run("hello"))

    assert result.error is not None
    assert "11434" in result.error or "Ollama" in result.error
    assert result.cost_usd == 0.0


@pytest.mark.integration
def test_openai_integration():
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")

    result = asyncio.run(OpenAIProvider("gpt-4o-mini").run("Say hello in one word."))

    assert result.error is None
    assert len(result.output) > 0
    assert result.tokens_output > 0


@pytest.mark.integration
def test_anthropic_integration():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not set")

    result = asyncio.run(AnthropicProvider("claude-haiku-4-5-20251001").run("Say hello in one word."))

    assert result.error is None
    assert len(result.output) > 0
    assert result.tokens_output > 0


@pytest.mark.integration
def test_gemini_integration():
    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not set")

    result = asyncio.run(GeminiProvider("gemini-1.5-flash").run("Say hello in one word."))

    assert result.error is None
    assert len(result.output) > 0
    assert result.tokens_output > 0


@pytest.mark.integration
def test_ollama_integration():
    if not asyncio.run(is_running()):
        pytest.skip("Ollama is not running")

    result = asyncio.run(OllamaProvider("ollama/llama3").run("Say hello in one word."))

    assert result.error is None
    assert len(result.output) > 0
    assert result.cost_usd == 0.0
