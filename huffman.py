import os
import sys
import marshal
import array

try:
    import cPickle as pickle
except:
    import pickle


# function that will min-heapify a list of tuples (freq, word) starting at a given index with a given end
# this function assumes we are working with 1 indexed lists i.e. there is a placeholder
# value in the 0th element spot
def min_heapify(heap , current_index , last_index):
    l_child_index = current_index * 2
    r_child_index = (current_index * 2) + 1
    index_of_min = current_index
    (freq , _) = heap[current_index]
    
    # look at the left child, if it exists
    if l_child_index <= last_index:
        (l_freq , _) = heap[l_child_index]
        if l_freq < freq:
            index_of_min = l_child_index
            (freq, _) = heap[index_of_min]
    
    # look at the right child, if it exists
    if r_child_index <= last_index:
        (r_freq , _) = heap[r_child_index]
        if r_freq < freq:
            index_of_min = r_child_index

    # if the index of min is not the current index, we swap the tuples therein contained, and 
    # recursively call on the index where our min val is being swapped out of
    if not index_of_min == current_index:
        swap_tuples(heap, current_index, index_of_min)
        min_heapify(heap , index_of_min, last_index)
    else:
        # we are done
        return

# helper function, simply swaps tuples contained in two indecies
# NOTE, this function operates on the heap provided it
def swap_tuples(heap , i , j):
    tmp = heap[i]
    heap[i] = heap[j]
    heap[j] = tmp

# function given a min heap (with a placeholder value in 0th index)
# will pop off and return the minimum value. This function modifies its parameter
# and in fact ensures the integrity of the new min heap
def pop_min(min_heap):
    # if there are not at least two items in the min_heap, it doesn't follow my specification
    if len(min_heap) < 2:
        return None
    if len(min_heap) == 2:
        return min_heap.pop(1)
    # get the frequency tuple to return
    return_tuple = min_heap.pop(1)

    # replace the removed tuple with the last item in the heap
    last_index = len(min_heap) - 1
    last_item = min_heap.pop(last_index)
    min_heap.insert(1, last_item)
    min_heapify(min_heap, 1, last_index)

    return return_tuple

'''
# function that takes a list of tuples of type (int,_) and returns a min_heap version
# of that list
def build_min_heap(tuple_list):
    # we can use this list to create our min heap
    min_heap = [-1] # we use a nonsene value to hold our 0th index, as we want to play with more comprehensible 1-indexed list

    for entry in tuple_list:
        (freq , word) = entry
        # we put this new entry in the last 'available' position
        min_heap.append( (freq,word) )
        # bubble this tuple up until its frequency value is greater than that of its parents
        current_index = len(min_heap) - 1 # the index of the value we just added
        parent_index = current_index // 2 
        in_place = False
        while(not in_place and not parent_index < 1):
            (parent_freq, parent_word) = min_heap[parent_index]
            if freq < parent_freq:
                # swap with parent
                min_heap[parent_index] = (freq,word)
                min_heap[current_index] = (parent_freq,parent_word)
            else:
                in_place = True

    return min_heap
'''

# given a tuple list (using a placeholder value in its 0th index), build a min_heap in-place
# note, this function works on and alters its parameter
def build_min_heap(tuple_list):
    # given a list of tuples, turn that into a heap by applying min_heapify from bottom up
    # get get the index of the last element in our list
    last_index = len(tuple_list) - 1
    # all elements after last_index / 2 are leaf nodes, due to the properties of a binary tree
    # and we don't need to look at these, as they are trivially min-heaps
    # starting with all parent nodes, we heapify them and move upwards
    last_parent_index = last_index // 2
    while last_parent_index >= 1:
        min_heapify(tuple_list , last_parent_index , last_index)
        last_parent_index -= 1
    
'''
# function that accepts a min_heap and pops off the minimum element from the root
# This fucntion alters the given min_heap, and ensures the new root is the smallest
# element
def pop_min(min_heap):
    # our root is the value to return
    return_tuple = min_heap.pop(1)  #we have 1-indexed heaps

    # we put the last element in the heap in the root spot, unless it was already
    # moved there via our pop()
    if len(min_heap) > 2:
        # pop the last element out
        new_root = min_heap.pop(len(min_heap) - 1)
        current_index = 1
        min_heap.insert(current_index, new_root)
        (freq , word) = min_heap[current_index]
        in_place = False
        l_child_index = current_index * 2
        r_child_index = (current_index * 2) + 1 
        while not in_place:
            # if there is a left child
            max_index = len(min_heap) - 1
            l_child_exists = l_child_index <= max_index
            r_child_exists = r_child_index <= max_index
            if l_child_exists and r_child_exists:
                pass
            elif r_child_exists:
                pass
            else:
                # only left child exists
                pass





    return return_tuple
'''



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

    # we can use this list to create our min heap
    min_heap = build_min_heap(freq_list)

    # apply huffman algo to get our encoding tree


    # use tree to encode message

    # return message and tree for decoding

    raise NotImplementedError

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
