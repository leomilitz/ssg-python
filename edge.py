"""
Classe que guarda uma aresta entre um vértice origem e alvo.
"""
class Edge():
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __eq__(self, other):
        return (self.source.position == other.source.position and 
                self.target.position == other.target.position)