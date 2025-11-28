import re
from .patterns import INTENT_KEYWORDS, SERVICE_KEYWORDS
from .intent_schema import IntentResult
from .model_loader import MLModelLoader

class IntentClassifier:
    
    def __init__(self, use_ml=False, ml_model_path=None):
        self.use_ml = use_ml
        self.ml = MLModelLoader(ml_model_path) if use_ml else None

    def classify(self, text: str) -> IntentResult:
        text_low = text.lower()

        if self.use_ml and self.ml:
            ml_result = self.ml.predict(text)
            if ml_result:
                return IntentResult(
                    intent=ml_result["intent"],
                    service=self.detect_service(text_low),
                    confidence=ml_result["confidence"],
                    raw_text=text
                )

        # fallback: rule-based
        intent, confidence = self.rule_based_intent(text_low)
        service = self.detect_service(text_low)

        return IntentResult(
            intent=intent,
            service=service,
            confidence=confidence,
            raw_text=text
        )

    def rule_based_intent(self, text: str):
        best_match = None
        highest_score = 0

        for intent, keywords in INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > highest_score:
                best_match = intent
                highest_score = score

        confidence = min(1.0, highest_score / 3)  # simple heuristic
        return best_match, confidence

    def detect_service(self, text: str):
        for service, keywords in SERVICE_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return service
        return "generic"
