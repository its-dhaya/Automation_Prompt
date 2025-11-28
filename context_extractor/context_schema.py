from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ExtractedContext:
    date: Optional[str] = None       # e.g., "2025-11-29"
    time: Optional[str] = None       # e.g., "15:00"
    duration: Optional[str] = None   # e.g., "1 hour"
    participants: List[str] = None  # e.g., ["John", "Jane"]
    content: Optional[str] = None    # e.g., email body, message text
