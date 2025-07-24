

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []

        def dfs(i, cur, total):
            if total == target:
                res.append(cur.copy())
                return  # stop further processing
            if i >= len(candidates) or total > target:
                return

            # include current candidate
            cur.append(candidates[i])
            dfs(i, cur, total + candidates[i])  # not i+1 because we can reuse same element
            cur.pop()

            # skip current candidate
            dfs(i + 1, cur, total)

        dfs(0, [], 0)
        return res
