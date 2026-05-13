# Security Policy

## Supported Versions

Currently, only the latest version of **skate** is supported for security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of **skate** seriously. If you find a security vulnerability, please do not open a public issue. Instead, please report it via [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidelines-for-reporting-vulnerabilities/reporting-a-vulnerability-to-a-repository).

Include a description of the issue, steps to reproduce, and the version affected. We aim to respond to all reports within 7 days.

## Scope

**skate** is a command-line tool, not a network service. The relevant security surface includes:

- **API Key Management**: `skate` stores API keys locally in `~/.skate/config.json`. Access to this file should be restricted to the local user.
- **Provider Integrations**: API keys are only transmitted to the respective LLM providers (OpenAI, Anthropic, Google) during request execution. We do not store or transmit keys to any other third-party servers.
- **Local Data Export**: When using `--output`, `skate` writes results to the local filesystem. Ensure you have the necessary permissions for the target directory.
- **Dependency Security**: `skate` relies on third-party libraries like `litellm` and `httpx`. If a vulnerability is found in these dependencies, please report it to the respective upstream maintainers and notify us so we can update our pins.

## API Key Security Best Practices

- **Environment Variables**: For enhanced security, you can use environment variables (e.g., `OPENAI_API_KEY`) instead of the local config file. Environment variables always take precedence.
- **Minimal Permissions**: Use API keys with the minimum necessary scopes required for your prompts.
- **Secure Storage**: Ensure your home directory and the `~/.skate/` folder have appropriate filesystem permissions (e.g., `chmod 700 ~/.skate`).
