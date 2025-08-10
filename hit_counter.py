from collections import deque

class HitCounter:
    def __init__(self):
        self.q = deque()
        self.count = 0
    
    def _evict(self, ts):
        cutoff = ts - 300
        while self.q and self.q[0] <= cutoff:
            self.q.popleft()
            self.count -= 1
    
    def hit(self, ts):
        self.q.append(ts)
        self.count += 1
        self._evict(ts)
        
    def getHits(self, ts):
        self._evict(ts)
        return self.count
