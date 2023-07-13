# 133 Clone Graph

Problem description [here](https://leetcode.com/problems/clone-graph/description/).

#### Approach 1: BFS + Dict for cloned nodes

To ensure 100% coverage for a graph, we use BFS. 

We use a dictionary where key is value for the node and value is the node to keep track of nodes we already cloned. 

In addition, when we visit a node, if its neighbors have not been cloned yet, we also clone its neighbors and add them to the queue. And we append these neighbors to `neighbors` field of current node. 

```Python
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return node
        ret_root = Node(node.val)

        q = [node]
        # keep track of cloned stuff
        # Hashmap is the go-to
        cloned = {node.val: ret_root}
        
        while q:
            cur = q.pop(0)
            cur_clone = cloned[cur.val]
            
            for neighbor in cur.neighbors:
                # Also clone neighbors
                if neighbor.val not in cloned:
                    cloned[neighbor.val] = Node(neighbor.val)
                    q.append(neighbor)
                # Finish this clone's neighbor field
                cur_clone.neighbors.append(cloned[neighbor.val])

        return ret_root
```

