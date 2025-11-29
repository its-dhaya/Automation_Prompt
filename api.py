from intent_classifier.classifier import IntentClassifier
from context_extractor.extractor import ContextExtractor
from system_message_builder.builder import SystemMessageBuilder

class AutomationAPI:
    def __init__(self):
        self.intent_clf = IntentClassifier()
        self.context_ext = ContextExtractor()
        self.builder = SystemMessageBuilder()

    def generate_system_message(self, user_input: str) -> dict:
        """
        Main entry method: 
        → Classifies intent
        → Extracts context
        → Generates system message using unified builder
        → Returns dictionary for external tools (like n8n)
        """

        # 1. Intent Classification
        intent_result = self.intent_clf.classify(user_input)

        # 2. Context Extraction
        context_result = self.context_ext.extract(user_input)

        # 3. Build combined data object
        structured_output = {
            "intent": intent_result.intent,
            "service": intent_result.service,
            "confidence": intent_result.confidence,
            "context": {
                "date": context_result.date,
                "time": context_result.time,
                "duration": context_result.duration,
                "participants": context_result.participants,
                "content": context_result.content
            }
        }

        # 4. Final system message
        system_message = self.builder.build(structured_output)

        return {
            "intent": intent_result.intent,
            "confidence": intent_result.confidence,
            "service": intent_result.service,
            "context": structured_output["context"],
            "system_message": system_message
        }

# -------------------------------
# Example direct run
# -------------------------------
if __name__ == "__main__":
    api = AutomationAPI()
    result = api.generate_system_message(
        "schedule a meeting tomorrow at 3 PM for 1 hour with John and Jane"
    )

    print("\n====== API OUTPUT ======")
    for k, v in result.items():
        print(f"{k}: {v}")
