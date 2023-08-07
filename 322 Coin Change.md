# 322 Coin Change

Problem link is [here](https://leetcode.com/problems/coin-change/description/)

### Approach 1: Recursion -> Dynamic programming

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        Args:
            coins: coins of different denominations
            amount: total amount of money
        
        Returns:
            fewest number of coins to make up AMOUNT. -1 if not possible.
        """
        # DP.
        # Initialize DP array
        dp = [float('inf') for _ in range(amount + 1)]
        # dp(x), where x is AMOUNT. Each element is the result of coinChange with 
        # given amount as the index. 
        # Base cases
        dp[0] = 0
        for coin in coins:
            if coin <= amount:
                dp[coin] = 1
        for i in range(1, min(min(coins), amount + 1)):
            dp[i] = -1
        
        for i in range(min(coins), amount + 1):
            # recurrence relations
            for coin in coins:
                if i - coin >= 0 and dp[i - coin] != -1:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
            if dp[i] == float('inf'):
                dp[i] = -1
            
        return dp[amount]

```

### 