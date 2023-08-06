import hashlib


def __hash_api_key(api_key: bytes, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", api_key, salt, 100000)


def hash_api_key(api_key: str, salt: str) -> str:
    salt = salt.encode("utf-8")
    api_key = api_key.encode("utf-8")

    hashed_api_key = __hash_api_key(api_key, salt)

    return hashed_api_key.hex()


def verify_api_key(received_api_key: str, hashed_api_key: str, salt: str) -> bool:
    received_api_key = received_api_key.encode("utf-8")
    salt = salt.encode("utf-8")

    received_hashed_api_key = __hash_api_key(received_api_key, salt).hex()

    return hashed_api_key == received_hashed_api_key
