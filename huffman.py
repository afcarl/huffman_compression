import os
import sys
import marshal
import array
import copy

try:
    import cPickle as pickle
except:
    import pickle


#############################################################################
# class definition for Priority Queue for use in huffman compression
# this priority queue uses a min-heap to continually return the minimum
# value
class PriorityQueue:
    # constructor, sets our heap list and gives it dummy value (for ease of indexing)
    def __init__(self):
        heap = [-1]

    # function that will min-heapify starting at a given index down to given end (end of heap)
    def min_heapify(self , current_index , last_index):
        # INVARIANT - Initialization: The value at the current index represents a binary tree with 0-2 children, unsorted
        l_child_index = current_index * 2
        r_child_index = (current_index * 2) + 1
        index_of_min = current_index
        (freq , _) = self.heap[current_index]
        
        # look at the left child, if it exists
        if l_child_index <= last_index:
            (l_freq , _) = self.heap[l_child_index]
            if l_freq < freq:
                index_of_min = l_child_index
                (freq, _) = self.heap[index_of_min]
        
        # look at the right child, if it exists
        if r_child_index <= last_index:
            (r_freq , _) = self.heap[r_child_index]
            if r_freq < freq:
                index_of_min = r_child_index

        # if the index of min is not the current index, we swap the tuples therein contained, and 
        # recursively call on the index where our min val is being swapped out of
        # INVARIANT- Maintenance: the minimum value in our binary tree is swapped into the root spot,
        #                       satisfying the conditions and making it a min-heap, min_heapify is recursively
        #                       called to ensure that all subtrees of the newly swapped node also are consistent
        #                       with our min-heap rules
        if not index_of_min == current_index:
            self.swap_tuples(current_index, index_of_min)
            self.min_heapify(index_of_min, last_index)

        # INVARIANT - Termination: the element at current_index represents a subtree that is itself also a min-heap

    # helper function, simply swaps tuples contained in two indecies
    def swap_tuples(self , i , j):
        tmp = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = tmp

    # will remove the minimum value from the priority queue and return it
    # this function will call min_heapify to ensure that min-heap integrity is retained
    def dequeue(self):
        # INVARIANT - Initialization: The root element of the min-heap is smaller than any of its children, and
        #                           thus is the smallest element in the queue
        # if there are not at least two items in the min_heap, it doesn't follow my specification
        if len(self.heap) < 2:
            return None
        # there is one item in the heap (not including dummy value), so return it
        if len(self.heap) == 2:
            return self.heap.pop(1)

        # get the frequency tuple to return
        return_tuple = self.heap.pop(1)

        # replace the removed tuple with the last item in the heap and heapify it downwards
        last_index = len(self.heap) - 1
        last_item = self.heap.pop(last_index)
        self.heap.insert(1, last_item)
        self.min_heapify(1, last_index)
        # INVARIANT - Termination - the smallest element in the heap once again sits in the root position

        return return_tuple

    # function that inserts a tuple (freq, child) into a min_heap and bubbles it up until the integrity of the min 
    # heap is maintained
    def enqueue(self, insert_tuple):
        # insert the tuple on the end
        self.heap.append(insert_tuple)
        current_index = len(self.heap) - 1
        parent_index = current_index // 2
        in_place = False
        # INVARIANT - Initialization: The value just inserted is the last value in our min-heap,
        #                           and may or may not currently satisfy the conditions of our min-heap
        # INVARIANT - Maintenance: At each iteration of the while loop, the inserted value will propogate
        #                       upwards if it is determined to be less than its parent (it will swap with its parent)
        #                       This is guaranteed to maintain the integrity of the min-heap, as if it is smaller than
        #                       it's parent, it is by definition also smaller than any sibling it may have (as that sibling
        #                       must necessarily have been larger than the parent by definition)
        while not in_place and not parent_index < 1:
            (current_freq, current_child) = self.heap[current_index]
            (parent_freq, parent_child) = self.heap[parent_index]
            if current_freq < parent_freq:
                self.swap_tuples(current_index , parent_index)
                current_index = parent_index
                parent_index = current_index // 2
            else:
                in_place = True
        # INVARIANT - Termination: The node sits as the root of a subtree wherein it is smaller than any of its children

    # given a tuple list build a min_heap 
    def build_queue(self, tuple_list):
        # set heap to local copy and add dummy -1 value to 0th index
        self.heap = copy.deepcopy(tuple_list)
        self.heap.insert(0, -1)

        # given a list of tuples, turn that into a heap by applying min_heapify from bottom up
        # get the index of the last element in our list
        last_index = len(self.heap) - 1
        # INVARIANT - Initialization- all elements after (last_index / 2) are leaf nodes, due to the properties of a binary tree
        # and we don't need to look at these, as they are trivially min-heaps
        # starting with all parent nodes, we heapify them and move upwards
        last_parent_index = last_index // 2
        # INVARIANT - Maintenance: after each iteration, the element at last_parent_index will represent a subtree that is guaranteed
        #                       to be a min-heap
        while last_parent_index >= 1:
            self.min_heapify(last_parent_index , last_index)
            last_parent_index -= 1

        # INVARIANT - Termination: self.heap represents a min-heap

    # function that returns the length of the priority queue (ignoring, of course
    # our dummy value -1 at 0th index
    def length(self):
        return len(self.heap) - 1

##############################################################################
# group of utility functions for huffman encoding
# takes our (freq, [list of children]) tuple and constructs both an encoding and 
# decoding dictionary. Our encoding dictionary is indexed by the char with its 
# value being the path to that value on the tree, whereas the decoding dictionary
# represents the inverse
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
    
# takes our huffman tree and turns it into a (freq, [list of children') tuple
def process_tree(tree):
    if isinstance(tree, list):
        return process_tree(tree[0]).append(process_tree(tree[1]))
    if isinstance(tree, tuple):
        if isinstance(tree[1] , list):
            return [process_tree(tree[1])]
        else:
            return tree[1]



##############################################################################
# code accepts a message (str) and returns a human readable huffman encoding
# along with a dictionary that can be used to decode the 'compressed' message
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
    return return_str, decoding_dict
############################################################################################

############################################################################################
def decode(msg, decode_dict):
    decodedMsg = ""
    path = ""
    for byte in msg:
        path += byte
        if path in decode_dict:
            decodedMsg += str(decode_dict[path])
            path = ""
    return decodedMsg 

############################################################################################

############################################################################################
# compress takes a message to compress (str) and returns a bitstring representation of
# the huffman encoding for the message, along side a dictionary that can be used to decompress
# the message
def compress(msg):
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
    # NOTE: here we insert our special 'EOF' character with a frequency of 1, this will
    # help decompresser to know when to stop
    freq_list = []
    for entry,freq in freqs.items():
           freq_list.append( (freq , entry) )
    freq_list.append( (1 , "EOF"))

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
    # NOTE: here we additionally append our special EOF encoding to the end
    # of the compressed message
    code =""
    for byte in msg:
        code += encoding_dict[byte]
    code += encoding_dict["EOF"]

    # now we need to turn our string encoding into a bitstring
    bitstream = array.array('B')
    buf = 0 # our current byte
    bit_count = 0 # keeps track of how far we are into writing unsigned byte
    msg_count = 0 # we need to know when we can stop writing to bitstream
    for bit in code:
        if(bit == "0"):
            buf = (buf<<1)
        else:
            buf = (buf<<1|1)
        bit_count += 1
        msg_count += 1
        if bit_count >= 8 or msg_count >= len(code):
            if msg_count >= len(code):
                # here we have a special case where we want to bump
                # up our bit values so there are no empty spaces in the bitstream
                # that could be misinterpreted by the decompresser
                buf = buf << (8 - bit_count)
                bitstream.append(buf)
            else:
                bitstream.append(buf)
                buf = 0
                bit_count = 0
        
    return bitstream, decoding_dict

#############################################################################################

#############################################################################################
# decompress takes a bitstream representation of a huffman encoded message as well as a
# dict that can be used to decompress it and returns the uncompressed message
def decompress(msg, decoderRing):
    # fix to re-wrap msg as a bitstream array
    msg = array.array('B' , msg)
    bits = ""
    #reading the raw binary values and adding a 1 or 0 to the string
    #according to the respective binary value
    # for every byte in our bitstring
    for byte in msg:
        word = ""
        # record the 'word' bit by bit, note this will record in reverse order
        for i in range(0,8):
            if(byte & 1):
                word += "1"
            else:
                word += "0"
            byte = byte >> 1
        # we now have the byte in string form, but reversed, so we need to reverse
        # it and append it to our overall bits string
        word = word[::-1]
        bits += word
    
    # we now have a literal string of 1's and 0's translated from our bitstring
    # we process this just as we did in the decode function, save for the
    # added functionality of halting when we see the EOF terminator
    path = ""
    decodedMsg = ""
    for bit in bits:
        path += bit
        if path in decoderRing:
            character = decoderRing[path]
            if character == "EOF":
                # we can stop
                break
            else:
                decodedMsg += str(character)
            path = ""
    return decodedMsg 

    return decode(bits,decoderRing)

#############################################################################################

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
