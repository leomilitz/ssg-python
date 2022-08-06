import matplotlib.pyplot as plt
import numpy as np
import utils
from edge import Edge

from vertex import Vertex

class Grid():
    def __init__(self, map_path, metrics):
        self.info = {}
        self.coords = []
        self.metrics = metrics
        self.vertexes = []
        self.visibility_graph = []
        self.map_path = map_path
        print("[info] Creating map...")
        self.read_map()
        self.create_map_vertexes()
        self.create_edges()
        print("[info] Map created.")
        self.metrics.show_metrics_map()

    def is_coord_valid(self, x, y):
        return (x >= 0 and y >= 0 and x < int(self.info["width"]) and y < int(self.info["height"])) 

    def create_edges(self):
        for row in self.vertexes:
            for v in row:
                for neighbor in utils.get_neighbors(self, v):
                    v.edges.append(Edge(v, neighbor))

    def create_visibility_graph(self, subgoals):
        print("[info] Creating visibility graph...")
        self.metrics.start_counting_time()

        for sg in subgoals:
            h_reachable = utils.clearance(self, sg.position)
            for h in h_reachable:
                self.visibility_graph.append(Edge(sg, h))

        self.metrics.end_counting_time()
        self.metrics.map_creation_info["vis_graph_time"] = str(self.metrics.time_elapsed) + " s"
        print(f"[info] Visibility graph created. Size: {len(self.visibility_graph)}")

    def is_convex_corner(self, v):
        x, y = v[0], v[1]

        for i in [-1, 1]:
            for j in [-1, 1]:
                if self.is_coord_valid(x+i, y+j) and self.coords[x+i][y+j] == 0:
                    if self.coords[x+i][y] == self.coords[x][y+j] == 1:
                        return True
        return False

    def reset_vertexes(self):
        for row in self.vertexes:
            for v in row:
                v.reset()

    def create_map_vertexes(self):
        self.vertexes = []
        corners = []
        for i in range(0, len(self.coords)):
            aux = []
            for j in range(0, len(self.coords[i])):
                walkable = True if self.coords[i][j] == 1 else False
                v = Vertex(self.coords[i][j], (i,j), walkable)
                
                if walkable and self.is_convex_corner((i,j)):
                    v.is_corner = True
                    corners.append(v)
                
                aux.append(v)    
            self.vertexes.append(aux)
            
    def read_map(self):
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

    def draw_map(self):
        print("[info] Drawing map...")
        plot_grid = []
        for vertex_line in self.vertexes:
            aux = []
            for v in vertex_line:
                color = [0, 0, 0]
                if v.walkable:  color = [255, 255, 255]
                if v.is_closed: color = [255,   0,   0]
                if v.is_path:   color = [  0, 255,   0]
                if v.is_start:  color = [255,   0,   0]
                if v.is_goal:   color = [255, 255,   0]
                if v.is_corner: color = [255,   0, 255] 
                
                aux.append(color)

            plot_grid.append(aux)

        plt.imshow(plot_grid)
        plt.show()



