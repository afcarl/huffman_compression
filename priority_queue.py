import copy
# definition of min heap priority queue

class PriorityQueue:
    # constructor, sets our list and gives it dummy value
    def __init__(self):
        heap = [-1]

    # function that will min-heapify starting at a given index down to given end
    def min_heapify(self , current_index , last_index):
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
        if not index_of_min == current_index:
            self.swap_tuples(current_index, index_of_min)
            self.min_heapify(index_of_min, last_index)

    # helper function, simply swaps tuples contained in two indecies
    def swap_tuples(self , i , j):
        tmp = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = tmp

    # will remove the minimum value from the priority queue and return it
    # this function will call min_heapify to ensure that min-heap integrity is retained
    def pop_min(self):
        # if there are not at least two items in the min_heap, it doesn't follow my specification
        if len(self.heap) < 2:
            return None
        if len(self.heap) == 2:
            return self.heap.pop(1)
        # get the frequency tuple to return
        return_tuple = self.heap.pop(1)

        # replace the removed tuple with the last item in the heap
        last_index = len(self.heap) - 1
        last_item = self.heap.pop(last_index)
        self.heap.insert(1, last_item)
        self.min_heapify(1, last_index)

        return return_tuple

    # function that inserts a tuple (freq, child) into a min_heap and bubbles it up until the integrity of the min 
    # heap is maintained
    def min_insert(self, insert_tuple):
        # insert the tuple on the end
        self.heap.append(insert_tuple)
        current_index = len(self.heap) - 1
        parent_index = current_index // 2
        in_place = False
        while not in_place and not parent_index < 1:
            (current_freq, current_child) = self.heap[current_index]
            (parent_freq, parent_child) = self.heap[parent_index]
            if current_freq < parent_freq:
                self.swap_tuples(current_index , parent_index)
                current_index = parent_index
                parent_index = current_index // 2
            else:
                in_place = True

    # given a tuple list build a min_heap 
    def build_queue(self, tuple_list):
        # set heap to local copy and add dummy -1 value to 0th index
        self.heap = copy.deepcopy(tuple_list)
        self.heap.insert(0, -1)

        # given a list of tuples, turn that into a heap by applying min_heapify from bottom up
        # get get the index of the last element in our list
        last_index = len(self.heap) - 1
        # all elements after last_index / 2 are leaf nodes, due to the properties of a binary tree
        # and we don't need to look at these, as they are trivially min-heaps
        # starting with all parent nodes, we heapify them and move upwards
        last_parent_index = last_index // 2
        while last_parent_index >= 1:
            self.min_heapify(last_parent_index , last_index)
            last_parent_index -= 1

    # function primarily for testing, will display the queue
    def display(self):
        print(self.heap)

        
    

