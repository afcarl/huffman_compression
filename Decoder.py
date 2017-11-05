#'a': '00'
#'c': '011'
#'b': '1010'
#'e': '11'
#'d': '1011'
#'g': '010'
#'f': '100'
import array

decoderRing = [['a', ['g', 'c']], [['f', ['b', 'd']], 'e']]
#cageaaa
msg = "0110001011000000"

#the function that decodes the string into its letter form using
#the huffman tree in array form
def decode(msg, decoderRing):
    newMsg = ""
    i = 0
    #traversing the huffman tree according to the values on the
    #string acting as array indexes
    while(i < len(msg)):
        theTree = decoderRing
        #as long as the node selected isn't a leaf node, i.e not
        #an array, then this loop continues. The index of the array,
        #or the child of the node, is taken until a leaf node is reached
        while(isinstance(theTree, list)):
            theTree = theTree[int(msg[i])]
            i = i + 1
        newMsg += theTree
    msg = newMsg
    return msg

def compress(msg):
    bitstream = array.array('B')
    buf = 0
    count = 0
    for bit in msg:
        if(bit == "0"):
            buf = (buf<<1)
        else:
            buf = (buf<<1)|1
        count += 1
        if(count > len(msg)):
            bitstream.append(buf)
            buf = (buf>>1)&1
    return buf

#the function that takes the binary form of the encoded message
#and the huffman tree in array form, and returns the fully decoded
#message
def decompress(msg, decoderRing):
    bits = ""
    #reading the raw binary values and adding a 1 or 0 to the string
    #according to the respective binary value
    for i in range(msg.bit_length()+1):
        if(msg & 1):
            bits += "1"
        else:
            bits += "0"
        msg = msg >> 1
    #reversing the order of the string, since its in reverse order
    #of the encoded message
    result = bits[::-1]
    #returning the return value of the decode function with result
    #as the parameter
    return decode(result,decoderRing)

print(compress(msg))
print(decompress(compress(msg), decoderRing))

