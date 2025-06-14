class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        count = {}
        for i,num in enumerate(nums):
            cmplnt = target - num
            if cmplnt in count:
                return [count[cmplnt], i]
            count[num]=i
