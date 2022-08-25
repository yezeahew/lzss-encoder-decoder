"""
Name: Hew Ye Zea
Student ID: 29035546
Date Created : 13/6/2020
Date Last Edited : 26/6/2020
"""


def z_algo(string, w_size, l_size, buffer_start):
    """
    Z algorithm
    :param string: the string
    :param w_size: window size
    :param l_size: lookahead buffer size
    :param buffer_start: the starting index of buffer
    """

    def z_for_buffer(buffer_size):
        """
        run Z algorithm for characters in the buffer / lookahead section
        :param buffer_size: size of the buffer / lookahead section
        """

        # initialise z array
        z_buffer_arr = [0] * buffer_size
        # initialise first position of z array
        z_buffer_arr[0] = buffer_size

        left = -1
        right = -1
        for k in range(1, buffer_size):
            # case 1 - no z box
            if k > right:
                count = 0
                # character a index : buffer_start + k + count
                # character b index : buffer_start + count
                while (k + count) < buffer_size and string[buffer_start + k + count] == string[buffer_start + count]:
                    count += 1
                left = k
                right = k + count - 1
                z_buffer_arr[k] = count
            else:
                remain = right - k + 1
                K = k - left

                # case 2a
                if z_buffer_arr[K] < remain:
                    z_buffer_arr[k] = z_buffer_arr[K]

                # case 2b
                elif z_buffer_arr[K] > remain:
                    z_buffer_arr[k] = remain

                # case 2c
                else:
                    count = 0
                    while (k + remain + count) < buffer_size and string[buffer_start + right + 1 + count] == string[buffer_start + right - k + 1 + count]:
                        count += 1
                    left = k
                    right = k + count - 1
                    z_buffer_arr[k] = count

        return z_buffer_arr

    def z_for_window():
        """
        Z algorithm for lzss, to calculate matched length of window ( dictionary ) & lookahead
        :return:
        """

        # initialise buffer size , this is to make sure the buffer size is within len(string)
        buffer_size = min(l_size, len(string) - buffer_start)

        # initialise the size of the window , this is to prevent negative index
        window_start = max(0, buffer_start - w_size)
        window_size = buffer_start - window_start  # calculate the size of window / dictionary

        z_buffer_arr = z_for_buffer(buffer_size)  # run Z for characters within the lookahead section

        # initialise z array for characters within the window
        z_window_arr = [0] * window_size

        # total length ( buffer size + window size )
        total_length = buffer_size + window_size

        left = -1
        right = -1
        for k in range(window_size):
            # case 1 - no z box
            if k > right:
                # compare characters and compute matched length
                # z_window_arr[k] stores the macthed length
                z_window_arr[k] = lz_compare(total_length,buffer_start,window_size,buffer_size,k,z_window_arr[k])
                left = k
                right = z_window_arr[k] + k - 1

            else:
                remain = right - k + 1
                K = k - left

                # case 2a
                if z_buffer_arr[K] < remain:
                    z_window_arr[k] = z_buffer_arr[K]

                # case 2b - z box exists
                elif z_window_arr[K] > remain:
                    z_window_arr[k] = remain

                    # calculate matched length outside z box
                    z_window_arr[k] = lz_compare(total_length, buffer_start, window_size, buffer_size, k,
                                                  z_window_arr[k])
                    left = k
                    right = z_window_arr[k] + k - 1

                # case 2c
                else:
                    z_window_arr[k] = lz_compare(total_length, buffer_start, window_size, buffer_size, k,
                                                  z_window_arr[k])
                    left = k
                    right = z_window_arr[k] + k - 1

        return z_window_arr

    def lz_compare(total_length,buffer_start,window_size,buffer_size,k,count):
        """
        Compare the characters of two index & compute matched length
        - matched length cannot exceed buffer size
        :param total_length: size of dictionary/window & lookahead buffer
        :param buffer_start: starting index of buffer
        :param window_size: size of dictionary
        :param buffer_size: size of buffer/lookahead
        :param k: current iteration
        :param count: matched length
        :return:
        """
        index_a = k + count + buffer_start - window_size
        index_b = count + buffer_start
        within_string_length = index_a < len(string) and index_b < len(string)  # make sure index is within len(string)

        while (count + k ) < total_length and count < buffer_size \
                and within_string_length and string[index_a] == string[index_b]:
            count += 1
            index_a = k + count + buffer_start - window_size
            index_b = count + buffer_start
            within_string_length = index_a < len(string) and index_b < len(string)
        return count

    return z_for_window()
