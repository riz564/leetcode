class Solution:
    def lengthOfLongestSubstring(self, s):
        seen = {}
        left = 0
        maxlen = 0 
        for i, c in enumerate(s):
            if c in seen and seen[c] >= left:
                left = seen[c] + 1
            seen[c] = i
            maxlen = max((i-left+1), maxlen)
        
        return maxlen
