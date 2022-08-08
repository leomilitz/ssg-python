"""
Classe do vértice. Ele guarda alguns bools úteis para o A* e para
printar no matplotlib o caminho realizado
"""
class Vertex():
    def __init__(self, value, position, walkable):
        self.value = value
        self.position = position
        self.walkable = walkable
        self.is_path = False
        self.parent = None
        self.is_open = False
        self.is_closed = False
        self.is_goal = False
        self.is_start = False
        self.is_corner = False
        self.h = 0
        self.g = 0
        self.f = 0
        self.edges = []

    def reset(self):
        self.is_path = False
        self.parent = None
        self.is_open = False
        self.is_closed = False
        self.is_goal = False
        self.is_start = False
        self.h = 0
        self.g = 0
        self.f = 0

    def get_f(self):
        return self.g + self.h

    def __lt__(self, other):
        if (self.get_f() == other.get_f()):
            return self.g < other.g
        
        return self.get_f() < other.get_f()

    def __str__(self):
        return f"pos: {self.position} | is_corner: {self.is_corner} | walk: {self.walkable}"