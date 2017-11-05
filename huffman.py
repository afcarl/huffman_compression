import os
import sys
import marshal
import array
from priority_queue import PriorityQueue

try:
    import cPickle as pickle
except:
    import pickle

def code(msg):
    # generate a frequency table for all our bytes
    freqs = {}
    for byte in msg:
        if byte not in freqs:
            # this is a new entry, so we add it to dict
            freqs[byte] = 1
        else:
            # we need to update the value
            current_freq = freqs[byte]
            freqs[byte] = current_freq + 1

    # now we have a dict of our word frequencies, we want to use this to construct 
    # a min-heap, so we first dump the dict to a list of tuples, and as we are concerned
    # primarily with frequency in the next step, we switch the order of the key/value pairing
    freq_list = []
    for entry,freq in freqs.items():
           freq_list.append( (freq , entry) )

    # we can use this list to create our priority queue
    queue = PriorityQueue()
    queue.build_queue(freq_list)

    # apply huffman algo to get our encoding tree
    while queue.length() > 1:
        min1_tuple = (min1_freq , min1_child) = queue.dequeue()
        min2_tuple = (min2_freq , min2_child) = queue.dequeue()
        new_tuple = (min1_freq + min2_freq , [min1_tuple , min2_tuple])
        queue.enqueue(new_tuple)

    # our priority queue should now (mostly) represent a huffman tree
    huffman_tree = queue.dequeue()

    # build a dictionary out of tree for encoding, this dictionary will
    # be indexed on the char and the value stored will be its encoding path
    # through the tree
    encoding_dict = {}
    decoding_dict = {}
    build_encoding_dict("" , huffman_tree, encoding_dict, decoding_dict)

    # now we can walk through the file once again and build our message
    return_str =""
    for byte in msg:
        return_str += encoding_dict[byte]
        


    #print huffman_tree
    return (return_str, decoding_dict)


        

    # use tree to encode message

    # return message and tree for decoding

    raise NotImplementedError

def build_encoding_dict(path, child, encode_dict, decoding_dict):
    (left , right) = child
    if not isinstance(right, list) and not isinstance(right, tuple):
        # we are at a (freq, char) base case
        encode_dict[right] = path
        decoding_dict[path] = right
    else:
        # process left and process right
        build_encoding_dict(path + "0" , right[0] , encode_dict, decoding_dict)
        build_encoding_dict(path + "1" , right[1] , encode_dict, decoding_dict)
    

def process_tree(tree):
    if isinstance(tree, list):
        return process_tree(tree[0]).append(process_tree(tree[1]))
    if isinstance(tree, tuple):
        if isinstance(tree[1] , list):
            return [process_tree(tree[1])]
        else:
            return tree[1]

def decode(str, decoderRing):

    raise NotImplementedError

def compress(msg):

    raise NotImplementedError

def decompress(str, decoderRing):

    raise NotImplementedError

def usage():
    sys.stderr.write("Usage: {} [-c|-d|-v|-w] infile outfile\n".format(sys.argv[0]))
    exit(1)

if __name__=='__main__':
    if len(sys.argv) != 4:
        usage()
    opt = sys.argv[1]
    compressing = False
    decompressing = False
    encoding = False
    decoding = False
    if opt == "-c":
        compressing = True
    elif opt == "-d":
        decompressing = True
    elif opt == "-v":
        encoding = True
    elif opt == "-w":
        decoding = True
    else:
        usage()

    infile = sys.argv[2]
    outfile = sys.argv[3]
    assert os.path.exists(infile)

    if compressing or encoding:
        fp = open(infile, 'rb')
        str = fp.read()
        fp.close()
        if compressing:
            msg, tree = compress(str)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), msg), fcompressed)
            fcompressed.close()
        else:
            msg, tree = code(str)
            print(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), msg), fcompressed)
            fcompressed.close()
    else:
        fp = open(infile, 'rb')
        pickleRick, msg = marshal.load(fp)
        tree = pickle.loads(pickleRick)
        fp.close()
        if decompressing:
            str = decompress(msg, tree)
        else:
            str = decode(msg, tree)
            print(str)
        fp = open(outfile, 'wb')
        fp.write(str)
        fp.close()
