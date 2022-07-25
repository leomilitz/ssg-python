from utils import distance_between
from queue import PriorityQueue

class Pathfinder():
    def __init__(self, grid, metrics):
        self.grid = grid
        self.metrics = metrics
        self.goal = (0,0)

    def is_valid_neighbor(self, idx):
        inside_grid = not ((idx[0] < 0 or idx[1] < 0) or (idx[0] > int(self.grid.info["width"])-1 or idx[1] > int(self.grid.info["height"])-1))        
        is_walkable = False
        
        if inside_grid: is_walkable = self.grid.vertexes[idx[0]][idx[1]].walkable
        return inside_grid and is_walkable 
    
    def update_h(self, vertex):
        vertex.h = distance_between(vertex.position, self.goal)

    def calculate_g(self, vertex, parent):
        return distance_between(vertex.position, parent.position) + parent.g

    def get_neighbors(self, vertex):
        neighbors = []
        x = vertex.position[0]
        y = vertex.position[1]
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_valid_neighbor((x+i, y+j)) and not (i == j == 0):
                    self.update_h(self.grid.vertexes[x+i][y+j])
                    neighbors.append(self.grid.vertexes[x+i][y+j])  
    
        return neighbors

    def walk_A_star(self, start, goal):
        self.metrics.reset_info()
        self.goal = goal
        start_vertex = self.grid.vertexes[start[0]][start[1]]
        goal_vertex = self.grid.vertexes[goal[0]][goal[1]]
        
        if start_vertex.value != 1 or goal_vertex.value != 1:
            print("[error] Invalid coordinates.")
            return

        test_name = f"A* {start} -> {goal}"
        self.metrics.start_counting_time()
        print(f"[{test_name}] started counting time...")

        closed_nodes = set()
        open_nodes = PriorityQueue(int(self.grid.info["width"]) * int(self.grid.info["height"]))
        open_nodes.put(start_vertex)
        self.metrics.info["open_nodes"] += 1

        while True:
            current = open_nodes.get()
            closed_nodes.add(current)
            
            if current.position == goal:
                dist = 0
                while current.position != start:
                    """
                    Adiciona o caminho e seus nodos vizinhos como path (dependendo do tamanho da imagem). 
                    Usado só para desenhar na tela o caminho do mapa.
                    """
                    current.is_path = True
                    if current.position == start:
                        current.is_start = True
                    if current.position == goal:
                        current.is_goal = True

                    if int(self.grid.info["width"]) > 256 or int(self.grid.info["height"]) > 256:
                        neighbors = self.get_neighbors(current)
                        for n in neighbors: 
                            n.is_path = True
                            if current.is_start:
                                n.is_start = True
                            if current.is_goal == goal:
                                n.is_goal = True

                    current = current.parent
                    dist += 1
                self.metrics.info["distance"] = dist 
                break 
            
            neighbor_list = self.get_neighbors(current)       
            for neighbor in neighbor_list:
                if neighbor.position in closed_nodes:
                    continue
                
                neighbor_g_cost = self.calculate_g(neighbor, current)
            
                # is_not_open = neighbor not in open_nodes
                is_not_open = not neighbor.is_open

                if is_not_open or neighbor_g_cost < neighbor.g:
                    neighbor.g = neighbor_g_cost
                    neighbor.f = neighbor.get_f()
                    neighbor.parent = current
                    
                    if is_not_open:
                        neighbor.is_open = True
                        open_nodes.put(neighbor)
                        self.metrics.info["open_nodes"] += 1
        
        self.metrics.end_counting_time()
        self.metrics.info["elapsed_time"] = str(self.metrics.time_elapsed) + " s"
        print(f"[{test_name}] ended counting!")
        print(f"Added test \"{test_name}\" to the log.")
        self.metrics.log[test_name] = self.metrics.info

    def walk_ssg(self, start, goal):
        self.metrics.reset_info()
        self.goal = goal
        start_vertex = self.grid.vertexes[start[0]][start[1]]
        goal_vertex = self.grid.vertexes[goal[0]][goal[1]]
        
        if start_vertex.value != 1 or goal_vertex.value != 1:
            print("[error] Invalid coordinates.")
            return

        test_name = f"SSG {start} -> {goal}"
        self.metrics.start_counting_time()
        print(f"[{test_name}] started counting time...")

        closed_nodes = set()
        open_nodes = PriorityQueue(int(self.grid.info["width"]) * int(self.grid.info["height"]))
        open_nodes.put(start_vertex)
        self.metrics.info["open_nodes"] += 1
        pass

                



