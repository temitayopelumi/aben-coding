def compress(chars):
    ans = []  # this holds the answer, a list is used because appending to a list is expensive it is O(n)^2
    length = len(chars)  # length of the string

    # edge case: if the length of the string is less than 2 return the string
    if length < 2:
        return chars

    # the beginning of the continuous collection of characters we are reading right now.
    start = 0

    # We continue through each character until we come to one where the next one is not on equal with it.
    # then we use the start and pos pointer to determine if it has appeared more than once.

    # 1. iterate till we find a different character
    # 2. record the no. of times the current char was repeated

    for i, char in enumerate(chars):

        # check if we have reached the end or a different char
        if (i + 1) == length or char != chars[i + 1]:
            # append the new char to ans
            ans.append(char)

            # check if char has been repeated
            if i > start:
                # check no. of times char has been repeated
                repeated_times = i - start + 1
                # append the no. of times to the ans
                ans.append(str(repeated_times))

            # move the start to the next char in the iteration
            start = i + 1
    return ''.join(ans)




assert compress("bbcceeee") == "b2c2e4" # returns true
assert compress("aaabbbcccaaa") == "a3b3c3a3" #returns true
assert compress("a") == "a" #return true


#time complexity. => 0(n)