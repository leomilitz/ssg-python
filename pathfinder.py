from turtle import clear
from edge import Edge
from queue import PriorityQueue
import heapq
import utils

class Pathfinder():
    def __init__(self, grid, metrics):
        self.grid = grid
        self.metrics = metrics
        self.goal = (0,0)
    
    def update_h(self, vertex):
        vertex.h = utils.distance_between(vertex.position, self.goal)

    def calculate_g(self, vertex, parent):
        return utils.distance_between(vertex.position, parent.position) + parent.g

    def walk_A_star(self, start, goal):
        self.goal = goal
        start_vertex = self.grid.vertexes[start[0]][start[1]]
        goal_vertex = self.grid.vertexes[goal[0]][goal[1]]
        
        if start_vertex.value != 1 or goal_vertex.value != 1:
            print("[error] Invalid coordinates.")
            return

        closed_nodes = set()
        open_nodes = [start_vertex]
        heapq.heapify(open_nodes)

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
                        neighbors = utils.get_neighbors(self.grid, current)
                        for n in neighbors: 
                            n.is_path = True
                            if current.is_start:
                                n.is_start = True
                            if current.is_goal == goal:
                                n.is_goal = True

                    current = current.parent
                    dist += 1
                break 
            
            edges = current.edges  
            for edge in edges:
                connected = edge.target
                if connected.position in closed_nodes:
                    continue
                
                connected_g_cost = self.calculate_g(connected, current)
                is_not_open = not connected.is_open

                if is_not_open or connected_g_cost < connected.g:
                    connected.h = utils.distance_between(connected.position, self.goal)
                    connected.g = connected_g_cost
                    connected.f = connected.get_f()
                    connected.parent = current
                    
                    if is_not_open:
                        connected.is_open = True
                        heapq.heappush(open_nodes, connected)

    def get_nearest_reachable_vertex(self, vertex):
        h_reachable = utils.clearance(self.grid, vertex.position)
        min = utils.distance_between(vertex, h_reachable[0])
        ans = None
        for h in h_reachable:
            dist = utils.distance_between(vertex, h)
            if dist < min:
                ans = h
                min = dist
        
        return ans
                



