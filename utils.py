def distance_between(v1, v2):
    """
    Octile distance entre dois vértices.
    """
    dist_x = abs(v2[0] - v1[0])
    dist_y = abs(v2[1] - v1[1])
    
    return (14 * min(dist_x, dist_y) + 10 * (abs(dist_x - dist_y)))

def cast_line_y_clearance(self, vertex, direction, max_reach):
    """
    Uma linha que percorre o eixo Y em busca de um subgoal, parede, ou o fim do mapa.
    """
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
    """
    Uma linha que percorre o eixo X em busca de um subgoal, parede, ou o fim do mapa.
    """
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
    """
    Uma linha que percorre a diagonal, e a cada passo, cria linhas verticais
    e horizontais em busca de subgoals, paredes ou fim do mapa.
    """
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
                    return h_reachable

                vertex, dist = cast_line_x_clearance(self, (x, y), inc_x, max_val_x)
                if vertex != None and dist <= max_val_x:
                    h_reachable.append(vertex)
                    max_val_x = dist - 1

                vertex, dist = cast_line_y_clearance(self, (x, y), inc_y, max_val_y)      
                if vertex != None and dist <= max_val_y:
                    h_reachable.append(vertex)
                    max_val_y = dist - 1 
                
    return h_reachable

def cardinal_clearance(self, v_idx):
    """
    Busca subgoals, paredes ou fim do mapa nos sentidos cardinais.
    """
    x, y = v_idx[0], v_idx[1]
    h_reachable = []
    
    for inc in [-1, 1]:
        vertex, dist = cast_line_x_clearance(self, (x, y), inc, int(self.info["width"]))
        if vertex != None: h_reachable.append(vertex)

        vertex, dist = cast_line_y_clearance(self, (x, y), inc, int(self.info["height"]))
        if vertex != None: h_reachable.append(vertex)         

    return h_reachable

def clearance(self, v_idx):
    """
    Realiza o clearance geral e retorna os vértices H-reachable.
    """
    c = cardinal_clearance(self, v_idx)
    d = diagonal_clearance(self, v_idx)
    return c + d

def is_valid_neighbor(self, idx):
    """
    Verifica se é um vizinho válido. Ou seja, verifica se ele é um vértice válido,
    não é uma parede, e não existem paredes que ele possa atravessar na diagonal.
    """
    x, y = idx
    inside_grid = not ((x < 0 or y < 0) or (x > int(self.info["width"])-1 or y > int(self.info["height"])-1))        
    is_walkable = False
    
    if inside_grid: is_walkable = self.vertexes[x][y].walkable
    return inside_grid and is_walkable 

def check_walls_around(self, idx, i, j):
    """
    Verifica se existem paredes na diagonal.
    """
    x, y = idx
    return (self.vertexes[x + i][y].walkable == False) or (self.vertexes[x][y + j].walkable == False)

def get_neighbors(self, vertex):
    """
    Busca uma lista de vizinhos válidos de um vértice.
    """
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
