class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res=[]
        for i,num in enumerate(nums):
            if i > 0 and num == nums[i - 1]:
                continue
            l=i+1
            r=len(nums)-1
            while l < r:
                curr_sum = num + nums[l] + nums[r]
                if curr_sum == 0:
                    res.append([num, nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1
                elif curr_sum < 0:
                    l += 1
                else:
                    r -= 1

        return res
