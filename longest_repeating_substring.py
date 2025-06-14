from collections import defaultdict
# 1st solution
'''class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = defaultdict(int)
        l = 0
        max_freq = 0
        res = 0
        
        for r in range(len(s)):
            count[s[r]] += 1
            max_freq = max(max_freq, count[s[r]])
            
            # If we need more than k replacements, shrink window
            while (r - l + 1) - max_freq > k:
                count[s[l]] -= 1
                l += 1
            
            res = max(res, r - l + 1)
        
        return res'''

#optimize solution

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = defaultdict(int)
        l = 0
        max_freq = 0
        res = 0
        
        for r in range(len(s)):
            count[s[r]] += 1
            max_freq = max(max_freq, count[s[r]])
            
            # If we need more than k replacements, shrink window
            while (r - l + 1) - max_freq > k:
                count[s[l]] -= 1
                l += 1
            
            res = max(res, r - l + 1)
        
        return res
