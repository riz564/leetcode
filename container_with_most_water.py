class Solution:
    def maxArea(self, heights: List[int]) -> int:
        l = 0
        r = len(heights)-1
        max_water = 0
        while l < r:
            water = (r-l) * min(heights[l], heights[r])
            max_water = max(water, max_water)
            if heights[l]<heights[r]:
                l+=1
            else:
                r-=1
        return max_water
