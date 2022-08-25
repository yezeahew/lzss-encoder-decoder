"""
Name: Hew Ye Zea
Student ID: 29035546
Date Created : 12/6/2020
Date Last Edited : 24/6/2020
"""

from elias import eliasDecode, fromBinaryToDec
from bitarray import bitarray
from heap import Heap


class HuffmanNode:
    """
    Huffman Node Class
    """
    def __init__(self):
        self.left = None   # 0
        self.right = None  # 1
        self.ascii = None  # if leaf , store the ascii code for the char


class HuffmanTree:

    def __init__(self):
        self.root = None

    def buildTree(self,code):
        """
        Build a Huffman Tree to decode
        :param code: huffman encoded bitstring
        :return: the final index that it traversed to
        """

        self.root = HuffmanNode()

        # get the number of unique characters
        unique_char, start_index = eliasDecode(code, 0)

        # decode each character , build huffman tree for decode purpose
        for i in range(unique_char):
            char_ascii = fromBinaryToDec(code,start_index,start_index+7)  # get the ascii code
            start_index += 7
            char_length,start_index = eliasDecode(code,start_index)  # get the length of the huffman code
            self.insert(code,start_index,start_index + char_length,char_ascii)   # insert the huffman code into HF tree
            start_index += char_length

        return start_index

    def insert(self, bitcode, start, end, ascii):
        """
        Insert the huffman coded.
        Huffman code to be inserted = bitcode[start:end]
        :param bitcode: the whole bitcode
        :param start: the starting index of a huffman code
        :param end: ending index of a huffman code [ end is exclusive ]
        :param ascii: ascii code of the character
        """
        current = self.root
        for i in range(start,end):

            # if bitcode[i] = "0"
            if not bitcode[i]:
                if current.left is None:  # if current.left does not exist , create a new node
                    current.left = HuffmanNode()
                current = current.left

            # bitcode[i] = "1"
            else:
                if current.right is None:  # if current.right does not exist , create a new node
                    current.right = HuffmanNode()
                current = current.right

        current.ascii = ascii  # reach the leaf, add ascii code of char

    def decodeHuffman(self,code,start_index):
        """
        Traverse the tree to decode a portion of code
        :param code: a bitstring that contains huffman encoded ascii codes
        :param start_index: starting index of a huffman code in code
        :return: the decoded ascii code , the final index traversed
        """
        current = self.root
        k = 0
        while current.ascii is None:  # keep traversing until hitting a leaf
            if not code[start_index+k]:
                current = current.left
            else:
                current = current.right
            k += 1

        return current.ascii, start_index + k  # return the ascii code & final index


def encodeHuffman(string):
    """
    Encode a string with Huffman encoding method
    :param string: the string to be encoded
    :return:
    encoded - an array that contains huffman codes of each unique character
    uniq_char - total number of unique characters
    """

    uniq_char = 0
    char_frequency = [0] * 128
    encoded_char = [None] * 128

    heap_array = []

    # calculate the frequency of each character
    for c in string :
        char_frequency[ord(c)] += 1

    # fill in the heap array
    for ascii in range(len(char_frequency)):
        if char_frequency[ascii] > 0:  # if character exists
            # add (frequency, [ascii code]) to heap array
            heap_array.append((char_frequency[ascii],[ascii]))  # store ascii codes as array in the tuple
            uniq_char += 1  # increment the number of unique characters
            encoded_char[ascii] = bitarray()

    myHeap = Heap()
    myHeap.heapify(heap_array)  # heapify the array , parent nodes are smaller than their children

    # while heap is not empty
    while len(myHeap) > 0 :
        a_freq , a_node = myHeap.heappop()  # remove the smallest node
        b_freq , b_node = myHeap.heappop()  # remove the second smallest node

        # ie :
        # node a = ( 3 , a )
        # node b = ( 2 , c )
        # new node = ( 5 , ac )
        new_node = (a_freq + b_freq, a_node + b_node)  # create a new node with the two nodes
        for ascii in a_node :
            encoded_char[ascii] = bitarray('0') + encoded_char[ascii]   # assign the huffman codes
        for ascii in b_node :
            encoded_char[ascii] = bitarray('1') + encoded_char[ascii]

        if len(myHeap) > 0:
            myHeap.add(new_node)  # push the new node into the heap

    return encoded_char,uniq_char


