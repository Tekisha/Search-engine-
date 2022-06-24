class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}

        # dictionary kljuc-file, value-broj ponavljanja
        self.file_ponavljanje={}


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")
    
    def insert(self, word,filename):
        """Insert a word into the trie"""
        node = self.root


        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        
        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we see this word once more
        node.counter += 1
        if filename in node.file_ponavljanje.keys():
            node.file_ponavljanje[filename]+=1
        else:
            node.file_ponavljanje[filename]=1
        
    def dfs(self, node, prefix,osnovni_oblik):
        if node.is_end:
            self.output.append((prefix + node.char, node.file_ponavljanje, node.counter))
            if osnovni_oblik:
                return
        
        for child in node.children.values():
            self.dfs(child, prefix + node.char,osnovni_oblik)
        
    def query(self, x, osnovni_oblik):
        self.output = []
        node = self.root

        if len(x)<5:
            osnovni_oblik = True
        
        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return [(x,{},0)]
        
        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1],osnovni_oblik)

        return self.output




