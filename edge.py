from utils import distance_between

class Edge():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.value = distance_between(v1.position, v2.position)
    