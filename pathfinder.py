from turtle import clear
from edge import Edge
from queue import PriorityQueue
import heapq
import utils
from vertex import Vertex

class Pathfinder():
    def __init__(self, grid, metrics):
        self.grid = grid
        self.metrics = metrics
        self.goal_position = (0,0)
    
    def update_h(self, vertex):
        vertex.h = utils.distance_between(vertex.position, self.goal_position)

    def calculate_g(self, vertex, parent):
        return utils.distance_between(vertex.position, parent.position) + parent.g

    def ssg(self, start, goal):
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

        return self.a_star(self.grid.subgoals[start], self.grid.subgoals[goal])

    def a_star(self, start, goal):
        start.is_start = True
        self.goal_position = goal.position
        
        if start.value != 1 or goal.value != 1:
            print("[error] Invalid coordinates.")
            return

        closed_nodes = set()
        open_nodes = [start]
        heapq.heapify(open_nodes)

        while True:
            if (len(open_nodes) == 0):
                print("Goal not found")
                return None
            
            current = heapq.heappop(open_nodes)
            current.is_closed = True
            closed_nodes.add(current)
            
            if current.position == goal.position:
                current.is_goal = True
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
                        heapq.heappush(open_nodes, connected)

                



