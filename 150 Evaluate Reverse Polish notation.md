# 150 Evaluate Reverse Polish notation

Problem description is [here](https://leetcode.com/problems/evaluate-reverse-polish-notation/description/).

#### Approach 1: Naive with minor improvements

```Python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        l = 0
        while len(tokens) >= 3:
            for i in range(l, len(tokens)):
                if tokens[i] in ["+", "-", "*", "/"]:
                    expr = self.eval_basic(tokens[i-2], tokens[i-1], tokens[i])
                    tokens = tokens[:i-2] + [str(expr)] + tokens[i+1:]
                    l = i - 1
                    break
        return int(tokens[0])
        
    def eval_basic(self, op1, op2, operator):
        op1 = int(op1)
        op2 = int(op2)
        if operator == "+":
            return op1 + op2
        elif operator == "-":
            return op1 - op2
        elif operator == "*":
            return op1 * op2
        elif operator == "/":
            return int(op1 / op2)
```

