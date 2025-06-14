class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapParantheses = {
            ')' : '(',
            '}' : '{',
            ']' : '['
        }
        for c in s:
            if c in mapParantheses:
                if stack and stack[-1] == mapParantheses[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        return True if not stack else False
