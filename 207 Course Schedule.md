# 207 Course Schedule

#### Approach 1: DFS topological sort in DPV style

We run DFS on `prerequisites` graph and mark each node's preorder and postorder numbers. Then we iterate through all the edges to see if there is a back edge. If there is a back edge, the graph is not a DAG, and therefore not possible to finish all the courses. 

```Python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        visited = []
        clock = 0
        preorder = [0 for _ in range(numCourses)]
        postorder = [0 for _ in range(numCourses)]

        def explore(i):
            nonlocal clock
            preorder[i] = clock
            clock += 1
            edges = [x for x in prerequisites if x[1] == i]
            for edge in edges:
                if edge[0] not in visited:
                    visited.append(edge[0])
                    explore(edge[0])
            postorder[i] = clock
            clock += 1

        for i in range(numCourses):
            if i not in visited:
                visited.append(i)
                explore(i)
        # Find backedge
        for edge in prerequisites:
            u = edge[1]
            v = edge[0]
            if preorder[v] <= preorder[u] <= postorder[u] <= postorder[v]:
                return False
        return True
```

