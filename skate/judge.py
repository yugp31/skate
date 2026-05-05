from dataclasses import dataclass, field


@dataclass
class JudgeResult:
    winner: str
    reasoning: str
    scores: dict[str, dict[str, float]] = field(default_factory=dict)
