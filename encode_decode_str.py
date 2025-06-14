from typing import List

class Solution:
    delim = ":"

    def encode(self, strs: List[str]) -> str:
        res = ''
        for s in strs:
            res += str(len(s)) + self.delim + s
        return res

    def decode(self, s: str) -> List[str]:
        i = 0
        op = []
        while i < len(s):
            j = i
            while s[j] != self.delim:
                j += 1
            length = int(s[i:j])               
            j += 1                             
            ss = s[j: j + length]              
            op.append(ss)
            i = j + length                   
        return op
