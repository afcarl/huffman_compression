#'a': '00'
#'c': '011'
#'b': '1010'
#'e': '11'
#'d': '1011'
#'g': '010'
#'f': '100'

tree = [['a', ['g', 'c']], [['f', ['b', 'd']], 'e']]

msg = "0110001011"

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

print(decode(msg, tree))
