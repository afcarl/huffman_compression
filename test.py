from huffman import build_min_heap as build
from huffman import pop_min

tups = [-1, (17,'a'),(5,'b'),(4,'e'),(3,'t'),(2,'y'),(5,'l'),(1,'r')]

build(tups)

for i in range(7):
    print(pop_min(tups))
