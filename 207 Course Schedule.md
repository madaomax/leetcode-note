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

#### Approach 2: Kahn's algorithm

Intuition: If there is a cycle in the graph, there will be at least one node that cannot be visited since it will always have a nonzero indegree. On the other hand, if there are no cycles, all the nodes can be visited by starting from the nodes with no incoming edges and removing their outgoing edges one by one. If all nodes are finished in the end, it means that it is possible to finish all the courses. 

Kahn's algorithm:

1. Initialization & build the adjacency list
   1. Create an adjacency list to represent the directed graph. Each node in the graph represents a course, and the edges represent the prerequisites.
   2. `indegree` array of size `n`. It keeps track of the number of incoming edges to each course.
   3. `ans` array to store the topological order of the courses.
2. Perform topological sort using Kahn's algorithm
   1. 
3. Check result

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        ans = []

        for pair in prerequisites:
            course = pair[0]
            prerequisite = pair[1]
            adj[prerequisite].append(course)
            indegree[course] += 1
        
        queue = []
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)
        
        while queue:
            current = queue.pop(0)
            ans.append(current)

            for next_course in adj[current]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    queue.append(next_course)
            
        return len(ans) == numCourses
```

