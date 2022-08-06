def distance_between(v1, v2):
    dist_x = abs(v2[0] - v1[0])
    dist_y = abs(v2[1] - v1[1])
    
    return (14 * min(dist_x, dist_y) + 10 * (abs(dist_x - dist_y)))

def cast_line_y_clearance(self, vertex, direction, max_reach):
    x, y = vertex[0], vertex[1]
    while y < max_reach:
        y += direction
        if not self.is_coord_valid(x, y) or self.coords[x][y] == 0:
            break

        if self.vertexes[x][y].is_corner:
            return self.vertexes[x][y]
    return None

def cast_line_x_clearance(self, vertex, direction, max_reach):
    x, y = vertex[0], vertex[1]
    while x < max_reach:
        x += direction
        if not self.is_coord_valid(x, y) or self.coords[x][y] == 0:
            break

        if self.vertexes[x][y].is_corner:
            return self.vertexes[x][y]
    
    return None

def diagonal_clearance(self, v_idx):
    h_reachable = []
    x, y = v_idx[0], v_idx[1]
    for inc_x in [-1, 1]:
        for inc_y in [-1, 1]:
            max_val_x, max_val_y = int(self.info["width"]), int(self.info["height"])
            while True:
                x += inc_x
                y += inc_y
                if not self.is_coord_valid(x, y) or self.coords[x][y] == 0:
                    break
                
                if self.vertexes[x][y].is_corner:
                    h_reachable.append(self.vertexes[x][y])
                    break
                
                vertex = cast_line_x_clearance(self, (x, y), inc_x, max_val_x)
                if vertex != None and abs(vertex.position[0] - x) < max_val_x:
                    h_reachable.append(vertex)
                    max_val_x = abs(vertex.position[0] - x)
                
                vertex = cast_line_y_clearance(self, (x, y), inc_y, max_val_y)
                if vertex != None and abs(vertex.position[1] - y) < max_val_y:
                    h_reachable.append(vertex)
                    max_val_y = abs(vertex.position[1] - y)
    return h_reachable

def cardinal_clearance(self, v_idx):
    x, y = v_idx[0], v_idx[1]
    h_reachable = []
    
    for inc in [-1, +1]:
        vertex = cast_line_x_clearance(self, (x, y), inc, int(self.info["width"]))
        if vertex != None: h_reachable.append(vertex)

        vertex = cast_line_y_clearance(self, (x, y), inc, int(self.info["height"]))
        if vertex != None: h_reachable.append(vertex)         

    return h_reachable

def clearance(self, v_idx):
    return cardinal_clearance(self, v_idx) + diagonal_clearance(self, v_idx)

def is_valid_neighbor(self, idx):
    inside_grid = not ((idx[0] < 0 or idx[1] < 0) or (idx[0] > int(self.info["width"])-1 or idx[1] > int(self.info["height"])-1))        
    is_walkable = False
    
    if inside_grid: is_walkable = self.vertexes[idx[0]][idx[1]].walkable
    return inside_grid and is_walkable 

def get_neighbors(self, vertex):
    neighbors = []
    x = vertex.position[0]
    y = vertex.position[1]
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_valid_neighbor(self, (x+i, y+j)) and not (i == j == 0):
                neighbors.append(self.vertexes[x+i][y+j])  

    return neighbors
