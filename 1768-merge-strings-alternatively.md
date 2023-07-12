# 1768. Merge Strings Alternatively

[Link to the problem description](https://leetcode.com/problems/merge-strings-alternately/description/?envType=study-plan-v2&envId=leetcode-75)



Solution 1:

```python
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        output = ""
        for i in range(max(len(word1), len(word2))):
            if i < len(word1):
                output += word1[i]
            if i < len(word2):
                output += word2[i]
        return output
```

Runtime: 

- `O(m+n)` where m and n are length of `word1` and `word2` respectively. 

Space complexity: 

- `O(1)`: Without considering the space consumed by the input strings (`word1` and `word2`) and the output string (`result`), we do not use more than constant space.
