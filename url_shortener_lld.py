import string
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime, timezone

CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = len(CHARS)
CHAR_TO_VAL = {c: i for i, c in enumerate(CHARS)}

@dataclass
class UrlMap:
    short_code: str
    long_url: str
    created_at: datetime
    expiry_at: Optional[datetime] = None

class Base62Encoder:
    @staticmethod
    def encode(num: int) -> str:
        if num < 0:
            raise ValueError("Number to encode must be non-negative")
        if num == 0:
            return CHARS[0]
        result = []
        while num > 0:
            num, rem = divmod(num, BASE)
            result.append(CHARS[rem])
        return ''.join(reversed(result))

    @staticmethod
    def decode(code: str) -> int:
        if not code:
            raise ValueError("Code to decode must be non-empty")
        num = 0
        for ch in code:
            if ch not in CHAR_TO_VAL:
                raise ValueError(f"Invalid character for base62: {ch!r}")
            num = num * BASE + CHAR_TO_VAL[ch]
        return num

class IdGenerator:
    def __init__(self, mac_id: str):
        # mac_id is a shard/prefix string, e.g. "A1" or "1"
        self.mac_id = mac_id
        self.counter = 0

    def get_next_id(self) -> str:
        self.counter += 1
        # 6 digits zero-padded counter; adjust if you expect > 999999
        return self.mac_id + str(self.counter).zfill(6)

class UrlShortener:
    def __init__(self, db: Dict[str, UrlMap], id_generator: IdGenerator):
        self.db = db
        self.id_generator = id_generator

    def shorten_url(self, long_url: str, expiry_at: Optional[datetime] = None) -> str:
        uid = self.id_generator.get_next_id()
        # Strip the prefix length rather than assuming 1 char
        prefix_len = len(self.id_generator.mac_id)
        numeric_id = int(uid[prefix_len:])
        short_code = Base62Encoder.encode(numeric_id)
        short_url = f'http://short.ly/{short_code}'
        self.db[short_code] = UrlMap(
            short_code=short_code,
            long_url=long_url,
            created_at=datetime.now(timezone.utc),
            expiry_at=expiry_at
        )
        return short_url

    def get_long_url(self, short_code: str) -> Optional[str]:
        mapping = self.db.get(short_code)
        if not mapping:
            return None
        # Valid if no expiry or not yet expired
        if mapping.expiry_at is None or mapping.expiry_at > datetime.now(timezone.utc):
            return mapping.long_url
        return None



# tiny demo
store: Dict[str, UrlMap] = {}
gen = IdGenerator("A")  # prefix "A"
service = UrlShortener(store, gen)
short = service.shorten_url("https://example.com/some/very/long/path")
code = short.rsplit("/", 1)[-1]
print(short, "->", service.get_long_url(code))
