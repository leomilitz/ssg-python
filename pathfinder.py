from edge import Edge
import heapq
import utils
from vertex import Vertex

"""
Classe responsável pelo pathfinding. Ela faz tanto o SSG quanto o A* puro.
"""
class Pathfinder():
    def __init__(self, grid, metrics):
        self.grid = grid
        self.metrics = metrics
        self.goal_position = (0,0)
    
    def update_h(self, vertex):
        """
        Atualiza a heuristica h, que seria a distância do vértice até o objetivo.
        """
        vertex.h = utils.distance_between(vertex.position, self.goal_position)

    def calculate_g(self, vertex, parent):
        """
        Calcula o g, que seria a distancia acumulada do caminho.
        """
        return utils.distance_between(vertex.position, parent.position) + parent.g

    def ssg(self, start, goal):
        """
        Aqui é realizado clearance para buscar os subgoals H-reachable do inicio e
        do objetivo, assim, criando uma aresta entre esses valores e adicionando aos
        subgoals. Depois disso, é feito o A* no grafo de visibilidade.
        """
        start_vertex = self.grid.vertexes[start[0]][start[1]] 
        start_vertex_copy = Vertex(start_vertex.value, start_vertex.position, start_vertex.walkable)
        start_vertex_copy.reset()
        goal_vertex = self.grid.vertexes[goal[0]][goal[1]] 
        goal_vertex_copy = Vertex(goal_vertex.value, goal_vertex.position, goal_vertex.walkable)
        goal_vertex_copy.reset()
        
        h_reachable = utils.clearance(self.grid, start)
        for h in h_reachable:
            h.edges.append(Edge(h, start_vertex_copy))
            start_vertex_copy.edges.append(Edge(start_vertex_copy, h))
        
        h_reachable = utils.clearance(self.grid, goal)
        for h in h_reachable:
            h.edges.append(Edge(h, goal_vertex_copy))
            goal_vertex_copy.edges.append(Edge(goal_vertex_copy, h))

        self.grid.subgoals[start] = start_vertex_copy
        self.grid.subgoals[goal]  = goal_vertex_copy

        result = self.a_star(self.grid.subgoals[start], self.grid.subgoals[goal])
        
        del self.grid.subgoals[start]
        del self.grid.subgoals[goal]

        return result

    def a_star(self, start, goal):
        """
        Implementação do A*. Cada vértice possui arestas para seus vizinhos válidos,
        e A* percorre essas arestas.
        """
        start.is_start = True
        self.goal_position = goal.position
        num_open = 0

        if start.value != 1 or goal.value != 1:
            print("[error] Invalid coordinates.")
            return

        closed_nodes = set()
        open_nodes = [start]
        heapq.heapify(open_nodes)

        while True:
            if (len(open_nodes) == 0):
                return None
            
            current = heapq.heappop(open_nodes)
            current.is_closed = True
            closed_nodes.add(current)
            
            if current.position == goal.position:
                current.is_goal = True
                self.metrics.info["open_nodes"] = num_open
                self.metrics.info["distance"]   = current.g
                return current
            
            edges = current.edges  
            for edge in edges:
                connected = edge.target
                if connected.position in closed_nodes:
                    continue
                
                connected_g_cost = self.calculate_g(connected, current)
                is_not_open = not connected.is_open

                if is_not_open or connected_g_cost < connected.g:
                    connected.h = utils.distance_between(connected.position, self.goal_position)
                    connected.g = connected_g_cost
                    connected.f = connected.get_f()
                    connected.parent = current
                    
                    if is_not_open:
                        connected.is_open = True
                        num_open += 1
                        heapq.heappush(open_nodes, connected)

                



