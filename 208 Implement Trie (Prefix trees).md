# 208 Implement Trie (Prefix trees)

Problem link is [here](https://leetcode.com/problems/implement-trie-prefix-tree/description/)

#### Approach 1: 61B style. Trees & Nodes. 

Use an empty node to be the head of the tree, and an empty node at the end of each word inserted. 

```Python
class Trie:

    def __init__(self):
        """
        A tree data structure used to efficiently store and retrieve keys 
        in a dataset of strings
        """
        self.head = Node()


    def insert(self, word: str) -> None:
        # Insert only when it is not inserted yet. 
        cur_node = self.head
        while word:
            cur_char = word[0]
            found = False
            for child in cur_node.children:
                if child.char == cur_char:
                    found = True
                    cur_node = child
                    break
            if not found:
                new_node = Node(cur_char)
                cur_node.children.append(new_node)
                cur_node = new_node
            word = word[1:]

        # Insert an empty node at the end to indicate the end of a word
        for child in cur_node.children:
            if child.char == "":
                return
        end_node = Node()
        cur_node.children.append(end_node)

        

    def search(self, word: str) -> bool:
        cur_node = self.head
        while word:
            cur_char = word[0]
            found = False
            for child in cur_node.children:
                if child.char == cur_char:
                    cur_node = child
                    found = True
                    word = word[1:]
                    break
            if not found:
                return False
        for child in cur_node.children:
            if child.char == "":
                return True
        return False
  

    def startsWith(self, prefix: str) -> bool:
        cur_node = self.head
        while prefix:
            cur_char = prefix[0]
            found = False
            for child in cur_node.children:
                if child.char == cur_char:
                    cur_node = child
                    found = True
                    prefix = prefix[1:]
                    break
            if not found:
                return False
        return True

        


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

class Node:
    def __init__(self, char=""):
        self.char = char
        # A list of child nodes. 
        self.children = []
   
```



#### Approach 2: Optimize for Python

To optimize runtime, maybe we need to get rid of another class. Dictionaries are our best friend due to its exceptional runtime, so we replace Nodes with dictionaries. Essentially, we have a bunch of nested dictionaries. Additionally, instead of an empty node to indicate the end of a word, we'll use a char not in the alphabet because keys cannot be empty. 

```python
class Trie:

    def __init__(self):
        """
        A tree data structure used to efficiently store and retrieve keys 
        in a dataset of strings
        """
        self.head = {}


    def insert(self, word: str) -> None:
        # Insert only when it is not inserted yet. 
        cur = self.head
        for letter in word:
            if letter not in cur:
                cur[letter] = {}
            cur = cur[letter]
        cur['*'] = ''


    def search(self, word: str) -> bool:
        cur = self.head
        for letter in word:
            if letter not in cur:
                return False
            cur = cur[letter]
        return '*' in cur
  

    def startsWith(self, prefix: str) -> bool:
        cur = self.head
        for letter in prefix:
            if letter not in cur:
                return False
            cur = cur[letter]
        return True

        
# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

```

