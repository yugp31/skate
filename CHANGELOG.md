# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Open-source community standard files (LICENSE, CONTRIBUTING, CODE_OF_CONDUCT).
- GitHub Actions CI for automated testing and linting.
- Issue and Pull Request templates.

## [0.1.0] - 2026-05-13

Initial release of **skate**.

### Added
- **Multi-LLM Parallel Runner**: Simultaneously query multiple models using `litellm` and `httpx`.
- **Supported Providers**: Out-of-the-box integration for OpenAI, Anthropic, Google Gemini, and Ollama (local).
- **CLI Commands**:
    - `run`: Execute prompts across models with support for system messages and template variables.
    - `models`: List and check status of configured models and API keys.
    - `config`: Manage API keys locally via `~/.skate/config.json`.
- **Evaluation Tools**:
    - Pairwise cosine similarity matrix via `sentence-transformers` (`--score`).
    - LLM-as-judge system with customizable criteria (`--judge`).
- **Rich Terminal Output**: Visual side-by-side comparison panels using `rich`.
- **Export Options**: Save results directly to `JSON` or `CSV` formats.
