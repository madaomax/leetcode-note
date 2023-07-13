# 150 Evaluate Reverse Polish notation

Problem description is [here](https://leetcode.com/problems/evaluate-reverse-polish-notation/description/).

Tag: Stack

#### Approach 1: Naive with minor improvements

Fact: To truncate a division towards zero, in Python 3, just wrap float division with `int()`. For example, `int(3 / 2)`.

Idea: find and start evaluate from the innermost expression. 

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

#### Approach 2: stack

It iterates through the tokens of the expression, performing the corresponding arithmetic operations when encountering operators. The solution pops operands from the stack, applies the operations, and pushes the results back to the stack. If a token is an operand, it is directly added to the stack. Finally, the one remaining value on the stack is retrieved as the evaluated result of the RPN expression. 

```Python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        op = ['+', '-', '*', '/']
        for t in tokens:
            if t in op:
                x, y = int(stack.pop()), int(stack.pop())
                stack.append(y + x if t == '+' else y - x if t == '-' \
                                else x * y if t == '*' else int(y / x))       
            else:
                stack.append(t)
        return int(stack[0])
```

Time complexity: `O(n)`, where n is length of `tokens`. 

Space complexity: `O(1)`