# utils.py
import base64

def encode_uid(uid_str: str) -> str:
    """Encode numeric user id to url-safe base64 without padding."""
    b = uid_str.encode('utf-8')
    s = base64.urlsafe_b64encode(b).decode('ascii')
    return s.rstrip('=')

def decode_uid(encoded: str) -> str:
    padded = encoded + '=' * ((4 - len(encoded) % 4) % 4)
    b = base64.urlsafe_b64decode(padded)
    return b.decode('utf-8')