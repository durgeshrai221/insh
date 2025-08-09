import base64

def encode_uid(user_id: int) -> str:
    return base64.urlsafe_b64encode(str(user_id).encode()).decode()

def decode_uid(encoded: str) -> int:
    return int(base64.urlsafe_b64decode(encoded.encode()).decode())
