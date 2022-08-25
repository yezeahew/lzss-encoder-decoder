"""
Name: Hew Ye Zea
Student ID: 29035546
Date Created : 16/6/2020
Date Last Edited : 26/6/2020
"""
import sys
from huffman import *
from elias import *
from bitarray import bitarray


def decode(filename):
    """
    Decode a file
    :param filename: file to be decoded
    :return: a file that contains the decoded string
    """

    bitcode = bitarray()
    file = open(filename, 'rb')
    bitcode.fromfile(file)

    # build a huffman tree to decode characters
    huffman_decoder = HuffmanTree()
    start_index = huffman_decoder.buildTree(bitcode)

    # decode the number of formats
    num_of_format, start_index = eliasDecode(bitcode,start_index)

    retval = ''
    # decode all formats
    for i in range(num_of_format):
        start_index += 1

        # match length > 3 : format starts with "0"
        if not bitcode[start_index - 1]:
            offset, start_index = eliasDecode(bitcode,start_index)  # decode the offset
            matched_length, start_index = eliasDecode(bitcode,start_index)  # decode match length

            offset_start = len(retval) - offset

            for j in range(matched_length):
                retval += retval[j + offset_start]  # copy the characters

        # match length < 3 , format starts with "1"
        else:
            char_ascii,start_index = huffman_decoder.decodeHuffman(bitcode,start_index)
            retval += chr(char_ascii)       # decode the character

    output = open('output_decoder_lzss.txt', 'w')
    output.write(retval)
    output.close()
    file.close()


if __name__ == '__main__':
    _, filename = sys.argv
    decode(filename)

    #decode('output_encoder_lzss.bin')