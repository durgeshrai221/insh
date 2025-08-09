# utils.py
import base64

def encode_uid(uid: str) -> str:
    """Encode chat id to URL-safe base64 (no padding)."""
    b = base64.urlsafe_b64encode(uid.encode()).decode().rstrip("=")
    return b

def decode_uid(encoded: str) -> str:
    """Decode URL-safe base64 uid back to original string."""
    padded = encoded + "=" * ((4 - len(encoded) % 4) % 4)
    return base64.urlsafe_b64decode(padded.encode()).decode()
