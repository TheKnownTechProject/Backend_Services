import re


def sanitize_html(value: str | None) -> str:
    if not value:
        return ""
    without_script = re.sub(r"<script.*?>.*?</script>", "", value, flags=re.IGNORECASE | re.DOTALL)
    return re.sub(r'on\w+=".*?"', "", without_script, flags=re.IGNORECASE)
