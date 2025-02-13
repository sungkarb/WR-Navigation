import numpy as np
from utilities import euclidean

class KDNode:
    def __init__(self, v, alignment=0):
        self.v = v 
        self.alignment = alignment
        self.left = None 
        self.right = None 
        self.parent = None 


class KDTree:
    def __init__(self):
        self.root = None 


    def insert(self, v):
        if self.root is None:
            self.root = KDNode(v)
            self.d = len(v)
            return 


        if len(v) != self.d:
            raise Exception(f"Length of new vector is {len(v)} when length of node is {self.d}")


        node = self.root 
        while True:
            i = node.alignment
            if v[i] >= node.v[i]:
                if node.right is None:
                    node.right = KDNode(v, ((i + 1) % self.d))
                    return 
                else:
                    node = node.right 
            else:
                if node.left is None:
                    node.left = KDNode(v, ((i + 1) % self.d))
                    return 
                else:
                    node = node.left 
    

    def find_neighbour(self, v):
        if self.root is None:
            raise Exception("Empty tree!")

        node = self.root 
        node_best = None  
        distance_best = None
        while node:
            if node_best is None:
                node_best = node 
                distance_best = euclidean(node_best.v, v)
            
            else:
                if euclidean(node.v, v) < distance_best:
                    node_best = node
                    distance_best = euclidean(node_best.v, v) 
                
            
            i = node.alignment
            if v[i] >= node.v[i]:
                node = node.right 
            else:
                node = node.left 

        return node_best.v
