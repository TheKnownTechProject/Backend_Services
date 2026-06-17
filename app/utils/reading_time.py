import math
import re
from typing import Any


def calculate_reading_time(content_html: str | None, content_blocks: list[dict[str, Any]] | None) -> int:
    html_text = re.sub(r"<[^>]+>", " ", content_html or "")
    block_text = " ".join(str(block.get("text", "")) for block in (content_blocks or []))
    words = len([word for word in f"{html_text} {block_text}".split() if word.strip()])
    if words == 0:
        return 0
    return max(1, math.ceil(words / 200))
