# LLD for Redis-like KV
# GET, SET, DEL, FLUSHDB, EXPIRE, TTL
import time
import threading

class Miniredis(object):
    def __init__(self):
        self._db = {}                 # key -> (value, expire_at or None)
        self._lock = threading.Lock()

    def _now(self):
        return time.time()

    def _is_expired(self, exp):
        return (exp is not None) and (exp <= self._now())

    # SET key value [ex=seconds]
    def set(self, key, value, ex=None):
        with self._lock:
            expire_at = (self._now() + ex) if ex is not None else None
            self._db[key] = (value, expire_at)

    # GET key -> value or None
    def get(self, key):
        with self._lock:
            item = self._db.get(key)
            if not item:
                return None
            value, exp = item
            if self._is_expired(exp):
                self._db.pop(key, None)  # lazy delete
                return None
            return value

    # DEL key -> True/False
    def delete(self, key):
        with self._lock:
            return self._db.pop(key, None) is not None

    # EXPIRE key seconds -> True/False
    def expire(self, key, seconds):
        with self._lock:
            item = self._db.get(key)
            if not item:
                return False
            value, exp = item
            if self._is_expired(exp):
                self._db.pop(key, None)
                return False
            self._db[key] = (value, self._now() + max(0, int(seconds)))
            return True

    # TTL key -> -2 (no key), -1 (no expiry), or remaining seconds
    def ttl(self, key):
        with self._lock:
            item = self._db.get(key)
            if not item:
                return -2
            _, exp = item
            if exp is None:
                return -1
            rem = int(exp - self._now())
            if rem < 0:
                self._db.pop(key, None)  # clean up if accessed after expiry
                return -2
            return rem

    # FLUSHDB
    def flushdb(self):
        with self._lock:
            self._db.clear()
