# 146 LRU Cache

Problem link can be found [here](https://leetcode.com/problems/lru-cache/description/?source=submission-ac).

#### Approach 1: Naive. Use list to store LRU.

Data structure choice: 

To get a key and a value, we need a dictionary. 

To store information of the sequence of recently, I chose the easiest dummy python list. However, `list.remove` takes `O(n)` . `list.append` takes `O(1)`. 

```Python
class LRUCache:

    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with positive size `capacity`
        """
        self.capacity = capacity
        self.dict = {}
        self.LRUqueue = []

    def get(self, key: int) -> int:
        """
        Return the value of the `key` if the key exists, otherwise 
        return -1.
        """
        value = self.dict.get(key, -1)
        if value == -1:
            return -1
        if key in self.LRUqueue:
            self.LRUqueue.remove(key)
        self.LRUqueue.append(key)
        return value

    def put(self, key: int, value: int) -> None:
        """
        Update the value of the key if the key exists. Otherwise, 
        add the key-value pair to the cache. If the number of keys
        exceeds the capacity from this operation, evict the 
        least recently used key. 
        """
        if self.dict.get(key, -1) == -1:
            if len(self.dict) == self.capacity:
                # evict the most recently used cache.
                MRkey = self.LRUqueue.pop(0)
                del self.dict[MRkey]
        if key in self.LRUqueue:
            self.LRUqueue.remove(key)
        self.LRUqueue.append(key)
        self.dict[key] = value


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

#### Approach 2: Doubly-linked list

In order to make `remove` and `add` time to `O(1)`, we can choose from stack, queue, singly-linked list, or doubly-linked list. Stack and queue do not work because LRU does not fall into their patterns. It is hard to trace the tail of singly-linked list. So, we consider doubly-linked list. 

```Python
class LRUCache:

    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with positive size `capacity`
        """
        self.capacity = capacity
        self.dict = {}
        # sentinel nodes
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        # create doubly linked list
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        """
        Return the value of the `key` if the key exists, otherwise 
        return -1.
        """
        if key not in self.dict:
            return -1
        node = self.dict[key]
        self.deleteNode(node)
        self.addNode(node)
        self.dict[key] = self.head.next
        return self.dict[key].val

    def put(self, key: int, value: int) -> None:
        """
        Update the value of the key if the key exists. Otherwise, 
        add the key-value pair to the cache. If the number of keys
        exceeds the capacity from this operation, evict the 
        least recently used key. 
        """
        if key in self.dict:
            node = self.dict[key]
            self.deleteNode(node)
            node.val = value
            self.addNode(node)
        else:
            if len(self.dict) == self.capacity:
                # evict the least recently used 
                last_node = self.tail.prev
                self.deleteNode(last_node)
                del self.dict[last_node.key]
            # create new node
            new_node = Node(key, value)
            self.addNode(new_node)
        self.dict[key] = self.head.next

    def deleteNode(self, p) -> None:
        """Delete dedicated node. O(1)"""
        p.prev.next = p.next
        p.next.prev = p.prev
    
    def addNode(self, new) -> None:
        """Add node to the front. O(1)"""
        temp = self.head.next
        self.head.next = new
        new.prev = self.head
        new.next = temp
        temp.prev = new

"""
Maintain a doubly-linked list. Recently used element will be stored first, and 
least recently used element will be stored last. 
"""
class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None
# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

