# 102 Binary Tree Level Order Traversal

Problem description is [here](https://leetcode.com/problems/binary-tree-level-order-traversal/description/).

#### Approach 1: BFS with distance dict

Use a queue to traverse the binary tree. Use a dictionary to keep track of level of node.

```Python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """BFS"""
        if not root:
            return []
        result = []
        q = []
        q.append(root)
        level = {}
        level[root] = 0
        
        while q:
            cur_node = q.pop(0)
            if cur_node:
                # Add current node to corresponding level
                if level[cur_node] >= len(result):
                    result.append([cur_node.val])
                else:
                    result[level[cur_node]].append(cur_node.val)

                if cur_node.left:
                    q.append(cur_node.left)
                    level[cur_node.left] = level[cur_node] + 1
                if cur_node.right:
                    q.append(cur_node.right)
                    level[cur_node.right] = level[cur_node] + 1          
        return result

```

#### Approach 2: BFS without dict

Idea: do not add next level nodes directly to the queue. But keep them in a separate queue. Therefore, we know which level we are on. 

```Python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """BFS"""
        if not root:
            return []
        result = [[root.val]]
        q = [root]
        temp = []
        
        while q:
            node = q.pop(0)
            if node.left: temp.append(node.left)
            if node.right: temp.append(node.right)
            if not q:
                if temp:
                    result.append([n.val for n in temp])
                q = temp
                temp = []
        return result
```

