def distance_between(v1, v2):
    dist_x = abs(v2[0] - v1[0])
    dist_y = abs(v2[1] - v1[1])
    
    return (14 * min(dist_x, dist_y) + 10 * (abs(dist_x - dist_y)))

def cast_line_y_clearance(self, vertex, direction, max_reach):
    x, y = vertex[0], vertex[1]
    dist = 0
    while y >= 0 and y < max_reach:
        y += direction
        dist += 1
        if (not self.is_coord_valid(x, y)) or (not self.vertexes[x][y].walkable):
            return None, dist

        if self.vertexes[x][y].is_corner:
            return self.subgoals[(x,y)], dist
    
    return None, dist

def cast_line_x_clearance(self, vertex, direction, max_reach):
    x, y = vertex[0], vertex[1]
    dist = 0
    while x >= 0 and x < max_reach:
        x += direction
        dist += 1
        if (not self.is_coord_valid(x, y)) or (not self.vertexes[x][y].walkable):
            break

        if self.vertexes[x][y].is_corner:
            return self.subgoals[(x,y)], dist  
    return None, dist

def diagonal_clearance(self, v_idx):
    h_reachable = []
    for inc_x in [-1, 1]:
        for inc_y in [-1, 1]:
            x, y = v_idx[0], v_idx[1]
            max_val_x, max_val_y = int(self.info["width"]), int(self.info["height"])
            while True:
                x += inc_x
                y += inc_y
                
                if not self.is_coord_valid(x, y): 
                    break
                
                if self.coords[x][y] == 0: 
                    break

                if check_walls_around(self, (x,y), -inc_x, -inc_y):
                    break
                
                if self.vertexes[x][y].is_corner:
                    h_reachable.append(self.subgoals[(x,y)])
                    break
                
                vertex, dist = cast_line_x_clearance(self, (x, y), inc_x, max_val_x)
                if vertex != None and abs(vertex.position[0] - x) < max_val_x:
                    h_reachable.append(vertex)
                    max_val_x = abs(vertex.position[0] - x)

                vertex, dist = cast_line_y_clearance(self, (x, y), inc_y, max_val_y)
                if vertex != None and abs(vertex.position[1] - y) < max_val_y:
                    h_reachable.append(vertex)
                    max_val_y = abs(vertex.position[1] - y)
                
    return h_reachable

def cardinal_clearance(self, v_idx):
    x, y = v_idx[0], v_idx[1]
    h_reachable = []
    
    for inc in [-1, 1]:
        vertex, dist = cast_line_x_clearance(self, (x, y), inc, int(self.info["width"]))
        if vertex != None: h_reachable.append(vertex)

        vertex, dist = cast_line_y_clearance(self, (x, y), inc, int(self.info["height"]))
        if vertex != None: h_reachable.append(vertex)         

    return h_reachable

def clearance(self, v_idx):
    c = cardinal_clearance(self, v_idx)
    d = diagonal_clearance(self, v_idx)
    return c + d

def is_valid_neighbor(self, idx):
    x, y = idx
    inside_grid = not ((x < 0 or y < 0) or (x > int(self.info["width"])-1 or y > int(self.info["height"])-1))        
    is_walkable = False
    
    if inside_grid: is_walkable = self.vertexes[x][y].walkable
    return inside_grid and is_walkable 

def check_walls_around(self, idx, i, j):
    x, y = idx
    return (self.vertexes[x + i][y].walkable == False) or (self.vertexes[x][y + j].walkable == False)

def get_neighbors(self, vertex):
    neighbors = []
    x = vertex.position[0]
    y = vertex.position[1]
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_valid_neighbor(self, (x+i, y+j)) and not (i == j == 0):
                if i != 0 and j != 0 and check_walls_around(self, (x,y), i, j):
                    continue
                neighbors.append(self.vertexes[x+i][y+j])
                     

    return neighbors
