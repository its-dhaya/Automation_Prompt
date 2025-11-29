# system_message_builder/builder.py

from .templates import FULL_SYSTEM_TEMPLATES
from datetime import datetime, timedelta

class SystemMessageBuilder:
    def __init__(self):
        pass

    def build(self, structured_data: dict) -> str:

        intent = structured_data.get("intent")
        context = structured_data.get("context", {})
        user_text = context.get("content", "")

        template = FULL_SYSTEM_TEMPLATES.get(intent)
        if not template:
            return f"No system prompt template found for intent: {intent}"

        # Participants formatting
        participants_list = context.get("participants", [])
        participants = ", ".join(participants_list) if participants_list else "None"

        # Calculate end date
        end_date = "N/A"
        if context.get("date") and context.get("time") and context.get("duration"):
            try:
                start_dt = datetime.strptime(
                    f"{context['date']} {context['time']}", "%Y-%m-%d %H:%M"
                )

                dur = context["duration"]
                hours = 0

                if "hour" in dur:
                    hours = int(dur.split()[0])

                end_dt = start_dt + timedelta(hours=hours)
                end_date = end_dt.strftime("%Y-%m-%d %H:%M:%S")

            except:
                pass

        # Auto-title (uppercase)
        title = user_text.upper() if user_text else "NEW EVENT"

        # Fill template
        message = template.format(
            date=context.get("date", "N/A"),
            time=context.get("time", "N/A"),
            end_date=end_date,
            title=title,
            content=user_text,
            participants=participants,
            original_text=user_text,
        )

        return message
