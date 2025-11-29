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

        # Default mapping for all tools
        mapping = {
            "date": context.get("date", "N/A"),
            "time": context.get("time", "N/A"),
            "duration": context.get("duration", "N/A"),
            "participants": ", ".join(context.get("participants", [])) if context.get("participants") else "None",
            "title": user_text.upper() if user_text else "NEW EVENT",
            "content": user_text,
            "original_text": user_text,
            "recipients": ", ".join(context.get("participants", [])) if context.get("participants") else "None",
            "subject": context.get("subject", user_text.split("\n")[0] if user_text else "NO SUBJECT"),
            "attachments": context.get("attachments", ""),
            "channel": context.get("channel", ""),
            "mentions": context.get("mentions", ""),
            "database": context.get("database", ""),
            "properties": context.get("properties", ""),
            "repo": context.get("repo", ""),
            "labels": context.get("labels", ""),
            "assignees": context.get("assignees", ""),
            "chat_id": context.get("chat_id", ""),
            "parse_mode": context.get("parse_mode", "Markdown"),
            "current_date": structured_data.get("current_date", datetime.now().strftime("%A %d %B %Y"))
        }

        # Compute end_date for calendar events if intent is create_calendar_event
        if intent == "create_calendar_event" and context.get("date") and context.get("time") and context.get("duration"):
            try:
                start_dt = datetime.strptime(f"{context['date']} {context['time']}", "%Y-%m-%d %H:%M")
                dur = context["duration"]
                hours = int(dur.split()[0]) if "hour" in dur else 0
                minutes = int(dur.split()[0]) if "min" in dur else 0
                end_dt = start_dt + timedelta(hours=hours, minutes=minutes)
                mapping["end_date"] = end_dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                mapping["end_date"] = "N/A"
        else:
            mapping["end_date"] = mapping.get("end_date", "N/A")

        # Fill template safely
        try:
            message = template.format(**mapping)
        except Exception as e:
            print("ERROR formatting template:", e)
            print("DEBUG - mapping:", mapping)
            message = template

        return message
