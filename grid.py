import matplotlib.pyplot as plt
import numpy as np
import utils
from edge import Edge

from vertex import Vertex

"""
Classe que representa o mapa. Guarda o grafo de visibilidade e
a lista de vértices.
"""
class Grid():
    def __init__(self, map_path, metrics):
        self.info = {}
        self.coords = []
        self.metrics = metrics
        self.vertexes = []
        self.subgoals = {}
        self.map_path = map_path
        print("[info] Creating map...")
        self.metrics.start_counting_time()
        self.read_map()
        self.metrics.map_creation_info = self.info
        print("[info] Creating vertexes...")
        self.create_map_vertexes()
        print("[info] Creating edges...")
        self.create_edges()
        print("[info] Map created.")
        self.metrics.end_counting_time()
        self.metrics.map_creation_info["map_time"] = str(self.metrics.time_elapsed) + " s"

    def is_coord_valid(self, x, y):
        """
        Verifica se a coordenada está dentro do mapa.
        """
        return (x >= 0 and y >= 0 and x < int(self.info["width"]) and y < int(self.info["height"])) 

    def create_edges(self):
        """
        Cria as arestas do mapa. Cada vértice possui uma aresta que o conecta
        com seus vizinhos válidos.
        """
        for row in self.vertexes:
            for v in row:
                for neighbor in utils.get_neighbors(self, v):
                    v.edges.append(Edge(v, neighbor))
    def create_visibility_graph(self):
        """
        Cria o grafo de visibilidade. É realizado o clearance
        para obter os h_reachable em todos subgoals, e depois disso
        cria uma aresta entre eles.
        """
        print("[info] Creating visibility graph...")
        self.metrics.start_counting_time()

        for sg in self.subgoals.values():
            h_reachable = utils.clearance(self, sg.position)
            for h in h_reachable:
                sg.edges.append(Edge(sg, h))

        self.metrics.end_counting_time()
        self.metrics.map_creation_info["vis_graph_time"] = str(self.metrics.time_elapsed) + " s"
        self.metrics.map_creation_info["vis_graph_size"] = len(self.subgoals)

    def is_convex_corner(self, v):
        """
        Verifica se o vértice é um canto convexo. É usado para criar
        os subgoals.
        """
        x, y = v[0], v[1]

        for i in [-1, 1]:
            for j in [-1, 1]:
                if self.is_coord_valid(x+i, y+j) and self.coords[x+i][y+j] == 0:
                    if self.coords[x+i][y] == self.coords[x][y+j] == 1:
                        return True
        return False

    def reset_vertexes(self):
        """
        Reseta todos os vértices do mapa.
        """
        for row in self.vertexes:
            for v in row:
                v.reset()

    def create_map_vertexes(self):
        """
        Cria os vértices do mapa. Se o vértice for um canto convexo,
        será adicionado na lista de subgoals.
        """
        self.vertexes = []
        for i in range(0, len(self.coords)):
            aux = []
            for j in range(0, len(self.coords[i])):
                walkable = True if self.coords[i][j] == 1 else False
                v = Vertex(self.coords[i][j], (i,j), walkable)
                
                if walkable and self.is_convex_corner((i,j)):
                    v.is_corner = True
                    sg = Vertex(v.value, v.position, v.walkable)
                    sg.is_corner = True
                    self.subgoals[sg.position] = sg
                
                aux.append(v)    
            self.vertexes.append(aux)
            
    def read_map(self):
        """
        Lê o arquivo .map do mapa informado. No resultado final, os caracteres
        são convertidos para 0 e 1, sendo:

        1 = andável
        0 = não andável
        """
        lines = []        
        with open(self.map_path) as f:
            print("[info] Loaded \"" + self.map_path + "\"")
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if (line[0][0] != "." and line[0][0] != "@"):
                split = line.split(" ")
                if (len(split) == 2):
                    self.info[split[0]] = split[1]
                else:
                    self.info["misc"] = split[0]
            else:
                new_line = line.replace("@", "0").replace(".", "1")
                self.coords.append(np.asarray(list(new_line), dtype=np.uint8))

    def draw_map(self, node):
        """
        Desenha o mapa usando matplotlib. Se o algoritmo usado for
        A* sem auxilio do grafo de visibilidade, irá pintar os 
        closed nodes de vermelho.
        """
        print("[info] Drawing map...")
        plot_grid = []
        for vertex_line in self.vertexes:
            aux = []
            for v in vertex_line:
                color = [0, 0, 0]
                if v.walkable:  color = [255, 255, 255]
                if v.is_closed: color = [255,   0,   0]
                if v.is_corner: color = [255,   0, 255] 
                
                aux.append(color)

            plot_grid.append(aux)
        
        while not node.is_start:
            x_org, y_org   = node.position
            x_dest, y_dest = node.parent.position
            plt.plot([y_org, y_dest], [x_org, x_dest], "-", color="lime")
            node = node.parent

        plt.imshow(plot_grid)
        plt.show()



