"""
Name: Hew Ye Zea
Student ID: 29035546
Date Created : 11/6/2020
Date Last Edited : 13/6/2020
"""


class Heap:
    def __init__(self):
        self.nodes = None
        self.count = 0

    def __len__(self):
        return self.count

    def compare_larger(self, index1, index2):
        """
        Compare two nodes and return the index of the larger node

        Each node stores ( frequency , characters )
        compare their frequency &  length of characters ,
        return the index with higher frequency / has more characters

        """
        node1, node2 = self.nodes[index1], self.nodes[index2]
        if node1[0] == node2[0]:  # check if frequency of is the same
            if len(node1[1]) < len(node2[1]):  # check length of characters
                return index2
            else:
                return index1
        else:
            if node1[0] < node2[0]:  # compare the frequency
                return index2
            else:
                return index1

    def compare_smaller(self, index1, index2):
        """
        Compare two nodes and return the index of the smaller node


        Each node stores ( frequency , characters )
        compare their frequency &  length of characters ,
        return the index with higher frequency / has more characters

        """
        node1, node2 = self.nodes[index1], self.nodes[index2]
        if node1[0] == node2[0]:  # check if frequency of is the same
            if len(node1[1]) < len(node2[1]):  # check length of characters
                return index1
            else:
                return index2
        else:
            if node1[0] < node2[0]:  # compare the frequency
                return index1
            else:
                return index2

    def heapify(self,array):
        """
        Heapify an array
        :param array: an array to be heapified
        :return: a heapified array
        """
        self.nodes = array
        self.count = len(array)
        for i in reversed(range(self.count//2)):
            self.siftup(i)

    def siftup(self, index):
        """
        Sift nodes up from a given index
        :param index:
        :return:
        """
        start_index = index
        current_item = self.nodes[index]
        smaller_child_i = self.get_smaller_children(index)  # get the smaller children

        while smaller_child_i is not None:   # sift the smaller children up , repeat until no smaller children
            self.nodes[index] = self.nodes[smaller_child_i]  # Move the smaller child up.
            index = smaller_child_i
            smaller_child_i = self.get_smaller_children(index)

        # hit the leaf , place current item here
        self.nodes[index] = current_item

        # sift down parent , so that current item is at the correct index
        self.siftdown(start_index,index)

    def siftdown(self, start, index):
        """
        Sift nodes down from index, so that all nodes are >= the node @ start
        """
        current_item = self.nodes[index]
        while index > start:
            parent_i = (index - 1) >> 1
            parent = self.nodes[parent_i]
            larger_i = self.compare_larger(index, parent_i)
            if larger_i == parent_i:
                self.nodes[index] = parent
                index = parent_i
                continue
            break
        self.nodes[index] = current_item

    def add(self, node):
        """
        Add a new node to the heap
        :param node: node to be added
        """
        self.nodes.append(node)
        self.count += 1
        self.siftdown(0,self.count-1)

    def heappop(self):
        """
        Remove the smallest item from the heap
        """
        if self.count > 0 :
            lastItem = self.nodes.pop()
            self.count -= 1
            if self.count > 0 :
                retItem = self.nodes[0]
                self.nodes[0] = lastItem
                self.siftup(0)
                return retItem
            return lastItem

    def swap(self, a, b):
        """
        Swap two nodes
        """
        self.nodes[a], self.nodes[b] = self.nodes[b], self.nodes[a]

    def get_parent(self, index):
        """
        Get parent of the node
        :param index: index of node
        :return: parent of node
        """
        parent_index = (index - 1) // 2
        parent_node = self.nodes[parent_index]
        return parent_index,parent_node

    def get_children(self,index):
        """
        Get children of node
        :param index: index of node
        :return: the children of node
        """
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        if left_child_index > self.count-1:  # left child does not exist
            left_node = None
            left_child_index = None
        else:
            left_node = self.nodes[left_child_index]

        if right_child_index > self.count-1:  # right child does not exist
            right_node = None
            right_child_index = None

        else:
            right_node = self.nodes[right_child_index]

        return [(left_child_index,left_node),(right_child_index,right_node)]

    def get_larger_children(self,index):
        """
        Return the larger child
        :param index: index of parent node
        :return: index of larger child node
        """
        left, right = self.get_children(index)
        if right[0] is not None :  # if right is not None , left must also be present ( heap properties )
            return self.compare_larger(left[0], right[0])
        else:
            if left[0] is not None:
                return left[0]
            else:
                return None

    def get_smaller_children(self,index):
        """
        Return the smaller child
        :param index: index of parent node
        :return: index of smaller child node
        """
        left , right = self.get_children(index)
        if right[0] is not None :  # if right is not None , left must also be present ( heap properties )
            return self.compare_smaller(left[0], right[0])
        else:
            if left[0] is not None:
                return left[0]
            else:
                return None

