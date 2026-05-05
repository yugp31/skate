from dataclasses import dataclass


@dataclass
class ModelResult:
    model: str
    output: str
    tokens_input: int
    tokens_output: int
    latency_seconds: float
    cost_usd: float
    error: str | None = None
