from intent_classifier.classifier import IntentClassifier
from context_extractor.extractor import ContextExtractor
from system_message_builder.builder import SystemMessageBuilder
from datetime import datetime
import pytz
import json

def main():
    # Initialize modules
    intent_clf = IntentClassifier()
    context_ext = ContextExtractor()
    builder = SystemMessageBuilder()

    # You can change this input to test different tools
    test_inputs = [
        # "schedule a meeting tomorrow at 3 PM for 1 hour with John and Jane",  # Google Calendar
        # "send an email to alice@example.com with subject Project Update and body Please review the attached report",  # Gmail
        # "post a message in #general channel on Slack saying Hello team",  # Slack
        "create a Notion page titled Weekly Report in database Reports with content Weekly metrics",  # Notion
        # "create a GitHub issue in repo my-repo titled Bug Found with body Steps to reproduce",  # GitHub
        # "send a Telegram message to @john_bot saying Meeting starts in 10 minutes"  # Telegram
    ]

    # Get current date in Asia/Kolkata
    ist = pytz.timezone("Asia/Kolkata")
    current_date = datetime.now(ist).strftime("%A %d %B %Y")

    for user_input in test_inputs:
        print(f"\n--- Testing Input ---\n{user_input}\n")

        # Run Intent Classifier
        intent_result = intent_clf.classify(user_input)
        print("DEBUG - intent:", intent_result.intent)

        # Run Context Extractor
        context_result = context_ext.extract(user_input)
        print("DEBUG - extracted context:", context_result.__dict__)

        # Combine both into structured output
        structured_output = {
            "current_date": current_date,
            "intent": intent_result.intent,
            "service": intent_result.service,
            "confidence": intent_result.confidence,
            "context": {
                "date": context_result.date or "",
                "time": context_result.time or "",
                "duration": context_result.duration or "",
                "participants": context_result.participants or [],
                "content": context_result.content or "",
                "subject": getattr(context_result, "subject", ""),
                "channel": getattr(context_result, "channel", ""),
                "database": getattr(context_result, "database", ""),
                "repo": getattr(context_result, "repo", ""),
                "labels": getattr(context_result, "labels", ""),
                "assignees": getattr(context_result, "assignees", ""),
                "chat_id": getattr(context_result, "chat_id", ""),
            }
        }

        # Convert participants list to comma-separated string
        if isinstance(structured_output["context"]["participants"], list):
            structured_output["context"]["participants"] = ", ".join(structured_output["context"]["participants"])

        # Build full system message
        system_msg = builder.build(structured_output)

        print("\n--- GENERATED FULL SYSTEM MESSAGE ---")
        print(system_msg)
        print("--------------------------------------------------")

if __name__ == "__main__":
    main()
