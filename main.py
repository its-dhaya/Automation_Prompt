from intent_classifier.classifier import IntentClassifier
from context_extractor.extractor import ContextExtractor
import json

def main():
    # Initialize modules
    intent_clf = IntentClassifier()
    context_ext = ContextExtractor()

    # User input
    user_input = "schedule a meeting tomorrow at 3 PM for 1 hour with John and Jane"

    # Run Intent Classifier
    intent_result = intent_clf.classify(user_input)

    # Run Context Extractor
    context_result = context_ext.extract(user_input)

    # Combine both
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

    # Print output
    print("\n--- Full Structured Output ---")
    print(json.dumps(structured_output, indent=4))
    print("--------------------------------\n")

if __name__ == "__main__":
    main()
