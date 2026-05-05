import asyncio

import pytest

from skate.runner import ModelResult, _make_provider, run_all
from skate.providers.anthropic import AnthropicProvider
from skate.providers.gemini import GeminiProvider
from skate.providers.ollama import OllamaProvider
from skate.providers.openai import OpenAIProvider


def test_make_provider_routing():
    assert isinstance(_make_provider("gpt-4o"), OpenAIProvider)
    assert isinstance(_make_provider("gpt-4o-mini"), OpenAIProvider)
    assert isinstance(_make_provider("claude-sonnet-4-5"), AnthropicProvider)
    assert isinstance(_make_provider("gemini-1.5-pro"), GeminiProvider)
    assert isinstance(_make_provider("ollama/llama3"), OllamaProvider)


def test_run_all_returns_one_result_per_model(monkeypatch):
    async def _fake_run(self, prompt, **kwargs):
        return ModelResult(
            model=self.model,
            output="hello",
            tokens_input=5,
            tokens_output=3,
            latency_seconds=0.1,
            cost_usd=0.0,
        )

    monkeypatch.setattr(OpenAIProvider, "run", _fake_run)
    monkeypatch.setattr(AnthropicProvider, "run", _fake_run)

    results = asyncio.run(run_all("test prompt", ["gpt-4o-mini", "claude-haiku-4-5-20251001"]))

    assert len(results) == 2
    assert all(r.output == "hello" for r in results)
    assert all(r.error is None for r in results)


def test_run_all_timeout(monkeypatch):
    async def _slow_run(self, prompt, **kwargs):
        await asyncio.sleep(60)
        return ModelResult(model=self.model, output="", tokens_input=0,
                           tokens_output=0, latency_seconds=60.0, cost_usd=0.0)

    monkeypatch.setattr(OpenAIProvider, "run", _slow_run)
    monkeypatch.setattr("skate.runner._run_one.__wrapped__", None, raising=False)

    async def _patched_run_one(model, prompt, system, temperature, max_tokens):
        provider = _make_provider(model)
        try:
            return await asyncio.wait_for(
                provider.run(prompt),
                timeout=0.05,
            )
        except asyncio.TimeoutError:
            return ModelResult(
                model=model,
                output="",
                tokens_input=0,
                tokens_output=0,
                latency_seconds=0.05,
                cost_usd=0.0,
                error="Request timed out after 30 seconds",
            )

    monkeypatch.setattr("skate.runner._run_one", _patched_run_one)

    results = asyncio.run(run_all("test", ["gpt-4o-mini"]))

    assert len(results) == 1
    assert results[0].error is not None
    assert "timed out" in results[0].error
