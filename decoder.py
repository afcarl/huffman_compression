#'a': '00'
#'c': '011'
#'b': '1010'
#'e': '11'
#'d': '1011'
#'g': '010'
#'f': '100'

#tree = [['a', ['g', 'c']], [['f', ['b', 'd']], 'e']]
tree = ['l' , ['e',['h','o']]]

msg = "1101000111"

def decode(msg, tree):
    newMsg = ""
    i = 0
    while(i < len(msg)):
        theTree = tree
        while(isinstance(theTree, list)):
            theTree = theTree[int(msg[i])]
            i = i + 1
        newMsg += theTree
    msg = newMsg
    return msg

#print(decode(msg, tree))


def decode_alt(msg, decode_dict):
    decodedMsg = ""
    path = ""
    for byte in msg:
        path += byte
        if path in decode_dict:
            decodedMsg += str(decode_dict[path])
            path = ""
    return decodedMsg 
        
