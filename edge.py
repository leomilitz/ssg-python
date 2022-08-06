from utils import distance_between

class Edge():
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.value = distance_between(source.position, target.position)
    
    # Averiguar se essa função está certa
    def __lt__(self, other):
        if (self.value == other.value):
            return self 
        
        return self.value < other.value

    def __eq__(self, other):
        return (self.source.position == other.source.position and 
                self.target.position == other.target.position)