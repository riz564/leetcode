from collections import defaultdict
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Step 1: Create a list of empty lists (buckets), size = len(nums) + 1
        # Why? Because the max frequency of any element can be len(nums)
        freq = [[] for _ in range(len(nums) + 1)]

        # Step 2: Count the frequency of each number using a dictionary
        count = defaultdict(int)
        for n in nums:
            count[n] += 1

        # Step 3: Place each number into the correct frequency bucket
        for num, freq_count in count.items():
            freq[freq_count].append(num)

        # Step 4: Gather the top K frequent elements by going from high to low frequency
        res = []
        for i in range(len(freq) - 1, -1, -1):  # Start from highest freq
            for num in freq[i]:
                res.append(num)
                if len(res) == k:
                    return res  # Once we've collected K elements, return

        # Fallback return (in case k == 0)
        return res
