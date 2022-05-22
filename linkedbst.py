"""
File: linkedbst.py
Author: Ken Lambert
"""

from copy import copy
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
from math import log
import random
import time
import sys
sys.setrecursionlimit(1000)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()
        stack = LinkedStack()
        node = self._root
        while not stack.isEmpty() or node is None:
            if node.left is not None:
                stack.push(node)
                node = node.left
            else:
                ele = stack.pop()
                lyst.append(ele.data)
                node = node.right
        return copy(lyst)

        # def recurse(node):
        #     if node is not None:
        #         recurse(node.left)
        #         lyst.append(node.data)
        #         recurse(node.right)

        # recurse(self._root)
        # return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)
        # return recurse(self._root)
        node = self._root
        if node == None:
            return None
        while True:
            if node == None:
                return None
            elif item == node.data:
                return node
            elif item < node.data:
                node = node.left
            else:
                node = node.right
            

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTN
                    ode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            if node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            # recurse(self._root)
            node = self._root
            while True:
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        break
                    node = node.left
                # New item is greater or equal,
                # go right until spot is found
                else:
                    if node.right == None:
                        node.right = BSTNode(item)
                        break
                    node = node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top): # pylint: disable=invalid-name
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top: BSTNode):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.right is None and top.left is None:
                return 0
            else:
                all_pos = [top.right, top.left]
                return 1 + max(height1(x) for x in all_pos if x is not None)
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        # print(list(self.inorder()))
        return self.height() < 2 * log((len(list(self.inorder())) + 1), 2) - 1

    def rangeFind(self, low, high): # pylint: disable=invalid-name
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [i for i in self.inorder() if low <= i <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def func(elem):
            if len(elem) == 0:
                return None
            mid = len(elem) // 2
            node = BSTNode(elem[mid])
            node.left = func(elem[:mid])
            node.right = func(elem[mid + 1:])
            return node

        self._root = func(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for num in self.inorder():
            if num > item:
                return num
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # allow = 0
        for num in list(self.inorder())[::-1]:
            if num < item:
                return num
            # elif allow == 1:
            #     return num
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            all_words = [word[:-1] for word in file]
            ten_thou = random.sample(all_words, k=10000)

        def list_find(words):
            """ find in list """
            cur_time = time.time()
            for word in ten_thou:
                word in words
            return time.time() - cur_time

        def bin_tree_find(words):
            """ find in bin tree """
            new_tree = LinkedBST()
            # print(len(words))
            for word in words:
                new_tree.add(word)
            cur_time = time.time()
            for word in ten_thou[5000:]:
                new_tree.find(word)
            return time.time() - cur_time
        
        def bin_tree_shuffled(words):
            """ find in shuffled bin tree """
            words1 = copy(words)
            random.shuffle(words1)
            new_tree = LinkedBST()

            for word in words1:
                new_tree.add(word)
            # print(new_tree.height())
            cur_time = time.time()
            for word in ten_thou:
                new_tree.find(word)
            return time.time() - cur_time

        def balanced_tree(words):
            """ find in balanced tree """
            words1 = copy(words)
            random.shuffle(words1)
            new_tree = LinkedBST()

            for word in words1:
                new_tree.add(word)
            cur_time = time.time()
            new_tree.rebalance()
            print(time.time() - cur_time)
            cur_time = time.time()
            for word in ten_thou:
                new_tree.find(word)
            return time.time() - cur_time

        return f"""find in list: {list_find(all_words)}\nfind in ordered tree: {bin_tree_find(all_words)}
find in shuffled tree: {bin_tree_shuffled(all_words)}\nfind in balanced tree: {balanced_tree(all_words)}"""
    

if __name__ == "__main__":
    LBST = LinkedBST()
    # print(LBST.demo_bst('words.txt'))
    # LBST.add(4)
    # LBST.add(2)
    # LBST.add(6)
    # LBST.add(1)
    # LBST.add(3)
    # LBST.add(55)
    # LBST.add(7)
    # LBST.add(9)
    # # lbst.add()
    # print(LBST)
    # print(LBST.height())
    # print(LBST.is_balanced())
    # LBST.rebalance()
    # print(LBST)
    # print(LBST.predecessor(10))
    # print(LBST.rangeFind(1, 50))
