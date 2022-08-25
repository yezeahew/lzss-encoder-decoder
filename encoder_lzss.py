"""
Name: Hew Ye Zea
Student ID: 29035546
Date Created : 16/6/2020
Date Last Edited : 26/6/2020
""" 
import sys
from huffman import *
from elias import *
from z_algo import *
from bitarray import bitarray


def encode(filename,w,l):

    # read file
    string = readfile(filename)

    # encode the string using huffman
    encoded , uniq_char = encodeHuffman(string)

    # encode header and data
    header = encode_header(uniq_char,encoded)
    data = encode_data(string,w,l,encoded)

    # concat header and data
    result = header + data

    # output result to file
    output = open('output_encoder_lzss.bin', 'wb')
    result.tofile(output)
    output.close()


def encode_header(uniq_char, encoded):
    """
    Encode the header
    :param uniq_char: number of unique characters
    :param encoded: the huffman code of each unique character
    :return: an encoded header
    """
    # header consists of
    # 1. unique char - elias coded
    # 2. ascii code of each char - elias coded
    # 3. length of huffman code - elias coded
    # 4. huffman code
    result = bitarray()
    result += eliasEncode(uniq_char)  # add elias encoded # of unique char to header [1]

    for ascii,huffman_code in enumerate(encoded):
        if huffman_code is not None :
            ascii_in_binary = fromDecToBinary(ascii)
            ascii_encoded = bitarray('0' * (7 - len(ascii_in_binary))) + ascii_in_binary  # elias coded ascii code [2]
            huffman_code_length = eliasEncode(len(huffman_code))  # elias coded - length of huffman code [3]
            result = result + ascii_encoded + huffman_code_length + huffman_code  # concat huffman code

    return result


def encode_data(string,w,l,encoded):
    """
    Encode the data part
    :param string: string to be encoded
    :param w: window size
    :param l: lookahead buffer size
    :param encoded: the huffman code of each unique character
    :return: a bitstring that contains the encoded data
    """
    result = bitarray()
    number_of_formats = 0
    index = 0

    while index < len(string):
        # increment the number of formats
        number_of_formats += 1

        # run z algorithm on string to calculate the matched length
        z_arr = z_algo(string,w,l,index)

        maximum_length = -1
        maximum_offset = -1

        # obtain the maximum match length
        for i in range(len(z_arr)):
            if z_arr[i] >= maximum_length:
                maximum_offset = i
                maximum_length = z_arr[i]

        # matched length > 3 , encode data in the format of :
        # 0 +  offset [1]  + matched length [2]
        if maximum_length >= 3 :
            zero = bitarray('0')
            offset = eliasEncode(len(z_arr) - maximum_offset)  # [1]
            length = eliasEncode(maximum_length)  # [2]
            result = result + zero + offset + length
            index += maximum_length  # increment index

        # matched length < 3 , encode data in the format of :
        # 1 + ascii huffman code [1]
        else:
            one = bitarray('1')
            char = string[index]
            ascii_huffman = encoded[ord(char)]  # [1]

            result = result + one + ascii_huffman
            index += 1  # increment index

    elias_format = eliasEncode(number_of_formats)  # elias encode the total number of format
    result = elias_format + result  # prepend the elias encoded format to result

    return result


def readfile(filename):
    file = open(filename,"r")
    lines = []
    for line in file:
        lines.append(line)
    file.close()
    return ''.join(lines)


if __name__ == '__main__':
    _, filename, w, l = sys.argv
    encode(filename, int(w), int(l))


