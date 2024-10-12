# Leetcode Code template Notes

https://leetcode.com/explore/interview/card/cheatsheets/720/resources/4723/





### Sliding window

```python
def fn(arr):
    left = ans = curr = 0
    
    for right in range(len(arr)):
        # do logic here to add arr[right] to curr (?)
        
        while WINDOW_CONDITION_BROKEN:
            # remove arr[left] from curr
            left += 1
        # update ans
    return ans
```

Substrings? Subarrays.



### Build a prefix sum

```python
def fn(arr):
    prefix = [arr[0]]
    for i in range(1, len(arr)):
        prefix.append(prefix[-1] + arr[i])
    return prefix
```



### Efficient string building

```python
# arr is a list of characters
def fn(arr):
    ans = []
    for c in arr:
        ans.append(c)
    return "".join(ans)
```





### Linked list: fast and slow poitner

```python
def fn(head):
    slow = head
    fast = head
    ans = 0
    
    while fast and fast.next:
        # do logic
        slow = slow.next
        fast = fast.next.next
   	return ans
```



### Reversing a linked list

```python
def fn(head):
    curr = head
    prev = None
    while curr:
        # Need to retain information for next_node because we will 
        # change the curr.next pointer.
        next_node = curr.next
        # Change .next pointer to point to the previous node.
        curr.next = prev
        # Update prev pointer
        prev = curr
        # Update curr pointer. 
        curr = next_node
    return prev
```



### Find number of subarrays that fit an exact criteria

```python
def fn(arr, k):
	counts = defaultdict(int)
    counts[0] = 1
    ans = curr = 0
    
    for num in arr:
        # do logic to change curr
        ans += counts[curr - k]
        counts[curr] += 1
    return ans
```

(??????????????)



### Monotonically increasing stack

```python
def fn(arr):
	stack = []
    ans = 0
    
    for num in arr:
        # for monotonic decreasing, just flip the > to <
        while stack and stack[-1] > num:
            # do logic
            stack.pop()
        stack.append(num)
    return ans
```





### Binary tree: DFS (iterative)

```python
def dfs(root):
    stack = [root]
    ans = 0
    while stack:
        node = stack.pop()
        # do logic
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return ans
```



### Binary tree: BFS

```python
from collections import deque

def fn(root):
    queue = deque([root])
    ans = 0
    
    while queue:
        current_length = len(queue)
        # do logic for current level
        
        for _ in range(current_length):
            node = queue.popleft()
            # do logic
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return ans
```



### Graph: DFS (recursive)

```python
def fn(graph):
    def dfs(node):
        ans = 0
        # do some logic
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                ans += dfs(neighbor)
        return ans
    seen = {START_NODE}
    return dfs(START_NODE)
```



### Graph: DFS (iterative)

```python
def fn(graph):
    stack = [START_NODE]
    seen = {START_NODE}
    ans = 0
    
    while stack:
        node = stack.pop()
        # do some logic
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return ans
```



### Graph: BFS

```python
from collections import deque

def fn(graph):
    queue = deque([START_NODE])
    seen = {START_NODE}
    ans = 0
    
    while queue:
        node = queue.popleft()
        # do some logic
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return ans
```





### Find top k elements with heap

```python
import heapq

def fn(arr, k):
    heap = []
    for num in arr:
        # do some logic to push onto heap according to problem's criteria
        heapq.heappush(heap, (CRITERIA, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for num in heap]
```





### Binary search: duplicate elements, left-most insertion point

```python
def fn(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] >= target:
            right = mid
        else:
            left = mid + 1
    return left
```



### Binary search: duplicate elements, right-most insertion point

```python
def fn(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] > target:
            right = mid
        else:
            left = mid + 1
    return left
```





### Binary search: for greedy problems

If looking for a minimum

```python
def fn(arr):
    def check(x):
        # this function is implemented depending on the problem
        return BOOLEAN
    left = MINIMUM_POSSIBLE_ANSWER
    right = MAXIMUM_POSSIBLE_ANSWER
    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            right = mid - 1
        else:
            left = mid + 1
    return left
```

If looking for a maximum:

```python
def fn(arr):
    def check(x):
        # this function is implemented depending on the problem
        return BOOLEAN
    left = MINIMUM_POSSIBLE_ANSWER
    right = MAXIMUM_POSSIBLE_ANSWER
    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            left = mid + 1
        else:
            right = mid - 1
    return right
```



### Backtracking

```python
def backtrack(curr, OTHER_ARGUMENTS...):
	if (BASE_CASE):
        # modify the answer
        return
    ans = 0
    for (ITERATE_OVER_INPUT):
        # modify the current state
        ans += backtrack(curr, OTHER_ARGUMENTS...)
        # undo the modification of the current state
    return ans

```



### Here's the guide for problem constraints:

| N           | Complexity | Possible Algorithms & Techniques                             |
| ----------- | ---------- | ------------------------------------------------------------ |
| 1018        | O(log N)   | Binary & Ternary Search / Matrix Power / Cycle Tricks / Big Simulation Steps / Values ReRank |
| 100,000,000 | O(N)       | A Linear Solution - May be a greedy/adhock algorithm         |
| 40,000,000  | O(N log N) | linear # calls to Binary & Ternary Search / Pre-processing & Querying / D & C |
| 10,000      | O(N2)      | adhock / DP / Greedy / D & C / B & B                         |
| 500         | O(N3)      | adhock / DP / Greedy / ..                                    |
| 90          | O(N4)      | adhock / DP / Greedy / ...                                   |
| 30-50       | O(N5)      | Search with pruning - branch and bound                       |
| 40          | O(2N/2)    | Meet in Middle                                               |
| 20          | O(2N)      | Backtracking / Generating 2N Subsets                         |
| 11          | O(N!)      | Factorial / Permutations / Combination Algorithm             |

** The above table is an excerpt from the ACM ICPC World Finalist 2011. The original blog post can be found [here](https://sites.google.com/site/mostafasibrahim/programming-competitions/thinking-techniques?authuser=0)

**P.S:** Practicing all these problems doesn't guarantee you a job at **Amazon**. It all depends on your *thought-process*, *luck* and *hard-work*. Take these problems as a reference to build your problem solving skills.



