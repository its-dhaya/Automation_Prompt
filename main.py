# from intent_classifier.classifier import IntentClassifier

# def main():
#     clf = IntentClassifier()

#     # Example natural-language input
#     user_input = "schedule a meeting tomorrow at 3 PM for 1 hour"

#     result = clf.classify(user_input)

#     print("\n--- Intent Classification Result ---")
#     print(f"Intent: {result.intent}")
#     print(f"Service: {result.service}")
#     print(f"Confidence: {result.confidence}")
#     print(f"Raw Text: {result.raw_text}")
#     print("------------------------------------\n")

# if __name__ == "__main__":
#     main()
from  content_extractor.extractor import ContextExtractor

ce = ContextExtractor()

user_input = "schedule a meeting tomorrow at 3 PM for 1 hour with John and Jane"

ctx = ce.extract(user_input)

print(ctx)
