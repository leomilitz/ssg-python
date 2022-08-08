from grid import Grid
from metrics import Metrics
from pathfinder import Pathfinder
from random import randrange

def create_valid_point(max_width, max_height, grid):
    x, y = randrange(0, max_width), randrange(0, max_height)
    while not grid.vertexes[x][y].walkable:
        x, y = randrange(0, max_width), randrange(0, max_height) 
    return x, y

def hundred_point_test(pathfinder, grid, metr, max_width, max_height):
    for i in range(0,100):
        start = create_valid_point(max_width, max_height, grid)
        goal  = create_valid_point(max_width, max_height, grid)
        do_ssg_only_test(start, goal, pathfinder, grid, metr)
        do_a_star_only_test(start, goal, pathfinder, grid, metr)
        

def do_ssg_only_test(start, goal, pathfinder, grid, metr):
    test_name = f"SSG {start} -> {goal}"
    metr.reset_info()
    metr.start_counting_time()
    print(f"[{test_name}] started counting time...")
    
    end_node = pathfinder.ssg(start, goal)

    metr.end_counting_time()
    metr.info["elapsed_time"] = str(metr.time_elapsed) + " s"
    print(f"[{test_name}] ended counting!")
    print(f"Added test \"{test_name}\" to the log.")
    metr.log[test_name] = metr.info
    metr.show_metrics_alg(test_name)

    if end_node == None:
        print(f"[{test_name}] Goal not found.")
        return None
    
    return end_node

def do_a_star_only_test(start, goal, pathfinder, grid, metr):
    test_name = f"A* {start} -> {goal}"
    metr.reset_info()
    metr.start_counting_time()
    print(f"[{test_name}] started counting time...")
    start_vertex = grid.vertexes[start[0]][start[1]]
    goal_vertex  = grid.vertexes[goal[0]][goal[1]]
    
    end_node = pathfinder.a_star(start_vertex, goal_vertex)

    metr.end_counting_time()
    metr.info["elapsed_time"] = str(metr.time_elapsed) + " s"
    print(f"[{test_name}] ended counting!")
    print(f"Added test \"{test_name}\" to the log.")
    metr.log[test_name] = metr.info
    metr.show_metrics_alg(test_name)

    if end_node == None:
        print(f"[{test_name}] Goal not found.")
        return None 

    return end_node

def main():
    metr = Metrics()
    grid = Grid("Denver_2_1024.map", metr)
    pathfinder = Pathfinder(grid, metr)
    
    grid.create_visibility_graph()
    metr.show_metrics_map()
    metr.show_metrics_vis_graph()

    #hundred_point_test(pathfinder, grid, metr, int(grid.info["width"]), int(grid.info["height"]))

    start = (0,0)
    goal  = (1020,1020)
    #end_node = do_a_star_only_test(start, goal, pathfinder, grid, metr)
    end_node = do_ssg_only_test(start, goal, pathfinder, grid, metr)
    grid.draw_map(end_node)

if __name__ == '__main__':
    main()