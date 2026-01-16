import hashlib

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def url_to_base62(url: str, hash_bytes: int = 7) -> str:
    """
    Преобразует URL в base62-строку.
    """

    digest = hashlib.sha256(url.encode("utf-8")).digest()
    num = int.from_bytes(digest[:hash_bytes], "big")

    if num == 0:
        return BASE62_ALPHABET[0]

    base = len(BASE62_ALPHABET)
    encoded = []

    while num > 0:
        num, rem = divmod(num, base)
        encoded.append(BASE62_ALPHABET[rem])

    return "".join(reversed(encoded))


def check_link_in_redis(short_code: str) -> str:
    return f"shortlink:{short_code}"
