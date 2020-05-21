def ASCIIConvert(message):
    result = 0
    for i in range(len(message)):
        result += ord(message[i])
    return result