import re
from .context_schema import ExtractedContext
from dateparser import parse
from dateparser.search import search_dates

class ContextExtractor:
    def __init__(self):
        pass

    def extract(self, text: str) -> ExtractedContext:
        ctx = ExtractedContext()

        # --- Extract date & time ---
        search_result = search_dates(text, languages=['en'])
        if search_result:
            dt_text, dt_obj = search_result[0]
            ctx.date = dt_obj.date().isoformat()
            ctx.time = dt_obj.time().strftime("%H:%M")

        # --- Extract duration ---
        duration_match = re.search(r'(\d+\s*(?:hour|hr|minute|min)s?)', text)
        if duration_match:
            ctx.duration = duration_match.group(1)

        # --- Extract participants ---
        participants_match = re.search(r'with\s+([A-Za-z, ]+)', text)
        if participants_match:
            participants = participants_match.group(1)
            participants = re.split(r',| and ', participants)
            ctx.participants = [p.strip() for p in participants if p.strip()]

        # --- Remaining text as content ---
        ctx.content = text

        return ctx
