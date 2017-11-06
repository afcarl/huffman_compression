# group of utility functions for huffman encoding
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


