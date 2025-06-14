class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups=defaultdict(list)
        for st in strs:
            count=[0]*26
            for c in st:
                count[ord(c)-ord('a')]+=1
            groups[tuple(count)].append(st)

        return [v for k,v in groups.items()]
