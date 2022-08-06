from turtle import clear
from edge import Edge
from utils import distance_between, clearance
from queue import PriorityQueue
import heapq

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

        closed_nodes = set()
        open_nodes = [start_vertex]
        heapq.heapify(open_nodes)
        self.metrics.info["open_nodes"] += 1

        while True:
            current = heapq.heappop(open_nodes)
            current.is_closed = True
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
                is_not_open = not neighbor.is_open

                if is_not_open or neighbor_g_cost < neighbor.g:
                    neighbor.g = neighbor_g_cost
                    neighbor.f = neighbor.get_f()
                    neighbor.parent = current
                    
                    if is_not_open:
                        neighbor.is_open = True
                        heapq.heappush(open_nodes, neighbor)
                        self.metrics.info["open_nodes"] += 1

    def get_nearest_reachable_vertex(self, vertex):
        h_reachable = clearance(self.grid, vertex.position)
        min = distance_between(vertex, h_reachable[0])
        ans = None
        for h in h_reachable:
            dist = distance_between(vertex, h)
            if dist < min:
                ans = h
                min = dist
        
        return ans

    def walk_ssg(self, start, goal):
        self.metrics.reset_info()
        self.goal = goal
        start_vertex = self.grid.vertexes[start[0]][start[1]]
        goal_vertex = self.grid.vertexes[goal[0]][goal[1]]
        vis_graph = self.grid.visibility_graph
        
        srt_edge = Edge(start_vertex, self.get_nearest_reachable_vertex(start_vertex))
        end_edge = Edge(goal_vertex, self.get_nearest_reachable_vertex(goal_vertex))
        vis_graph.insert(0, srt_edge)
        vis_graph.append(end_edge)
        
        if start_vertex.value != 1 or goal_vertex.value != 1:
            print("[error] Invalid coordinates.")
            return

        open_edges = [start_vertex]
        heapq.heapify(open_edges)
        closed_edges = set()
        self.metrics.info["open_nodes"] += 1

        while True:
            current = heapq.heappop(open_edges)
            closed_edges.add(current)

            if current.target.position == goal:
                print("cum") 
            
            neighbor_list = self.get_neighbors(current)       
            for neighbor in neighbor_list:
                if neighbor in closed_edges:
                    continue
                
                neighbor_g_cost = self.calculate_g(neighbor, current)
                is_not_open = not neighbor.is_open

                if is_not_open or neighbor_g_cost < neighbor.g:
                    neighbor.g = neighbor_g_cost
                    neighbor.f = neighbor.get_f()
                    neighbor.parent = current
                    
                    if is_not_open:
                        neighbor.is_open = True
                        heapq.heappush(open_edges, neighbor)
                        self.metrics.info["open_nodes"] += 1
                



