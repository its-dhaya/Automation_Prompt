from dataclasses import dataclass

@dataclass
class IntentResult:
    intent: str
    service: str
    confidence: float
    raw_text: str
