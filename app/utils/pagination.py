import base64


def encode_cursor(offset: int) -> str | None:
    if offset < 0:
        return None
    return base64.urlsafe_b64encode(str(offset).encode("utf-8")).decode("utf-8")


def decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    try:
        return int(base64.urlsafe_b64decode(cursor.encode("utf-8")).decode("utf-8"))
    except Exception:
        return 0
