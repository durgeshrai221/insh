import base64

def encode_uid(user_id: int) -> str:
    """Encode Telegram user ID to safe string."""
    return base64.urlsafe_b64encode(str(user_id).encode()).decode()

def decode_uid(uid_str: str) -> int:
    """Decode safe string back to Telegram user ID."""
    return int(base64.urlsafe_b64decode(uid_str.encode()).decode())