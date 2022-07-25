def distance_between(v1, v2):
    dist_x = abs(v2[0] - v1[0])
    dist_y = abs(v2[1] - v1[1])
    
    return (14 * min(dist_x, dist_y) + 10 * (abs(dist_x - dist_y)))