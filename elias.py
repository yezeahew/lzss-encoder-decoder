"""
Name: Hew Ye Zea
Student ID: 29035546
Date Created : 11/6/2020
Date Last Edited : 26/6/2020
"""

from bitarray import bitarray


def fromDecToBinary(num):
    """
    Generate binary representation of num
    :param num: the number
    :return: a bitarray that represents num
    """
    temp = []
    while num > 0:
        temp.append(num & 1)
        num = num >> 1
    temp = temp[::-1]  # reverse the array to get the correct binary representation
    return bitarray(temp)


def fromBinaryToDec(binary, start, end, flipBit=False):
    """
    Convert a portion of the bitarray to its respective decimal value
    :param binary: bitarray
    :param start: staring index
    :param end: ending index
    :param flipBit : boolean, true = flip starting bit
    :return: binary[start:end] as decimal value
    """
    bin = ""
    if flipBit :
        binary[start] = "1"
    for bit_index in range(start,end):
        if binary[bit_index]:
            bin += "1"
        else:
            bin += "0"

    return int(bin,2)


def eliasEncode(num):
    """
    Encode an integer using Elias Encoding method
    :param num: the integer to be elias encoded
    :return: the elias encoded integer
    """
    binary_num = fromDecToBinary(num)
    encoded = []
    encoded.append(binary_num)
    length_bin = len(binary_num)

    while length_bin > 1 :
        # encode all length code
        new_length = fromDecToBinary(length_bin-1)
        new_length[0] = 0  # flip the first bit to 0 , to denote that this is a length code
        encoded.append(new_length)
        length_bin = len(new_length)

    result = bitarray('')
    for i in range(len(encoded)-1,-1,-1):
        result += encoded[i]  # reverse the whole thing

    return result


def eliasDecode(code,current_i = 0):
    """
    Decode an elias encoded integer
    :param code: a bitstring that is elias encoded
    :param current_i: current index of i
    :return:
    """

    # if the current bit == "1" , that denotes the smallest possible integer , return 1 straight away
    if code[current_i]:
        return 1,current_i + 1

    else:
        index = 1
        length = 2
        # "0" denotes the length
        # while the next bit is "0" , keep finding the new length
        while not code[current_i+index]:
            new_length = fromBinaryToDec(code, current_i+index, current_i+index+length,True)
            index += length # increment index
            length = new_length + 1

        decoded_num = fromBinaryToDec(code,current_i+index, current_i+index+length)  # decode the number

        return decoded_num, index + current_i + length
