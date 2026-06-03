# 3 Longest Substring Without Repeating Characters

Problem description is [here](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/).

#### Approach 1:

Iterate through all substrings. If a character is a duplicate, we move to the next substring. We also keep track of the maximum length of the substrings.

```Python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) <= 1:
            return len(s)
        max_len = 0
        cur_substr = ""
        for i in range(len(s)):
            for j in range(i, len(s)):
                if s[j] not in cur_substr:
                    cur_substr = cur_substr + s[j]
                else:
                    max_len = max(max_len, len(cur_substr))
                    cur_substr = ""
                    break
        return max_len
```

#### Approach 2: Slide window + Python string

We want to improve the nested loop. Slide window is a technique to avoid nested loops. We keep track of a `left` pointer and a `right` pointer to represent the boundaries of current substring. 

Runtime 64ms beats 93.35%

Memory 16.3MB beats 83.12%

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Base case
        if len(s) <= 1:
            return len(s)
        max_len = 0
        cur_substr = ""
        left = 0

        for right in range(len(s)):
            if s[right] not in cur_substr:
                cur_substr = cur_substr + s[right]
                max_len = max(max_len, len(cur_substr))
            else:
                while s[right] in cur_substr:
                    cur_substr = cur_substr[1:]
                    left += 1
                cur_substr = cur_substr + s[right]
        return max_len
```

