class Edge():
    def __init__(self, source, target):
        self.source = source
        self.target = target
    
    # Averiguar se essa função está certa
    def __lt__(self, other):
        if (self.value == other.value):
            return self 
        
        return self.value < other.value

    def __eq__(self, other):
        return (self.source.position == other.source.position and 
                self.target.position == other.target.position)