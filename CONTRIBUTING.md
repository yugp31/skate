# Contributing to skate

Thank you for your interest in contributing to **skate**! This document covers how to set up your development environment, the project structure, and the pull request process.

## Development Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/PracticalMind/skate.git
   cd skate
   ```

2. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Verify** the installation:
   ```bash
   skate --help
   ```

## Project Structure

- `skate/cli/` — CLI entry point and command definitions (`main.py`).
- `skate/providers/` — Individual LLM provider implementations (OpenAI, Anthropic, Gemini, Ollama).
- `skate/runner.py` — Async orchestrator for running parallel prompts.
- `skate/scorer.py` — Similarity and readability scoring logic.
- `skate/judge.py` — LLM-as-judge evaluation logic.
- `skate/renderer.py` — Terminal UI rendering using `rich`.
- `tests/` — Unit and integration tests mirroring the `skate/` structure.

## How to Add a New Provider

1. Create a new file in `skate/providers/<name>.py`.
2. Inherit from `BaseProvider` and implement the `async def run(...)` method.
3. Ensure the provider handles API keys via `skate.config.get_api_key`.
4. Register the new provider in `skate/runner.py` inside the `_make_provider` function.
5. Add the supported model identifiers to `_KNOWN_MODELS` in `skate/cli/main.py`.
6. Create a corresponding test file in `tests/test_providers.py` or a new `tests/test_<name>.py`.

## Testing Requirements

- **Unit Tests**: Every logical path must be tested. We use `pytest` and `unittest.mock` to avoid real API calls.
- **Integration Tests**: Marked with `@pytest.mark.integration`. These are skipped by default unless the required environment variables (e.g., `OPENAI_API_KEY`) are set.
- **Verification**: Run all tests before submitting a PR:
  ```bash
  pytest
  ```

## Code Style

- **Type Hints**: Required for all function signatures and class members.
- **Linting**: We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Ensure your code is clean:
  ```bash
  ruff check .
  ruff check --fix .
  ```
- **Logging**: Use `rich.console` for CLI output and standard `logging` for internal library traces (if added). No raw `print()` calls in library code.
- **Clean Code**: Follow PEP 8. One class per file where possible, and ensure error messages are actionable.

## PR Process

1. Fork the repository and create a branch from `main`.
2. Implement your changes and add tests.
3. Ensure all tests pass and `ruff check .` is clean.
4. Open a Pull Request with a clear description of the change and its motivation.
5. If you're proposing a major architectural change, please open an issue for discussion first.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
