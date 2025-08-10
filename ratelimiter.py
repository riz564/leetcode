from time import time
class RateLimiter:
    def __init__(self, rate_per_sec, capacity):
        self.bucket_fill_rate = rate_per_sec
        self.bucket_capacity = capacity
        self.total_tokens = capacity
        self.last_req_time = time()
        
    def allow(self, now=None):
        now = now if now else time()
        elapsed = max(0.0, now - self.last_req_time)
        self.total_tokens = min(self.bucket_capacity, self.total_tokens + elapsed * self.bucket_fill_rate)
        self.last_req_time = now

        # Step 2: Check & consume
        if self.total_tokens >= 1:
            self.total_tokens -= 1
            return True
        return False
