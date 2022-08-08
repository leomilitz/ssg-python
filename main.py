from math import floor
from grid import Grid
from metrics import Metrics
from pathfinder import Pathfinder
from random import randrange

def create_valid_point(max_width, max_height, grid):
    x, y = randrange(0, max_width), randrange(0, max_height)
    while not grid.vertexes[x][y].walkable:
        x, y = randrange(0, max_width), randrange(0, max_height) 
    return x, y

def get_average_values_metrics(metr):
    print("[info] Calculating average values...")
    ssg_time = astar_time = 0.0
    ssg_nodes = astar_nodes = 0
    ssg_count = astar_count = 0
    for test in metr.log.values():
        if test["kind"] == "ssg":
            ssg_time += test["elapsed_time"]
            ssg_nodes += test["open_nodes"]
            ssg_count += 1

        if test["kind"] == "a*":
            astar_time += test["elapsed_time"]
            astar_nodes += test["open_nodes"]
            astar_count += 1

    avg_time_astar = astar_time / astar_count
    avg_time_ssg = ssg_time / ssg_count
    avg_nodes_astar = astar_nodes / astar_count
    avg_nodes_ssg = ssg_nodes / ssg_count

    print("==================================== SUMMARY ====================================")
    print(f"A* Average execution time:  {avg_time_astar} s")
    print(f"SSG Average execution time: {avg_time_ssg} s")
    print()
    print(f"A* Average open nodes:  {avg_nodes_astar}")
    print(f"SSG Average open nodes: {avg_nodes_ssg}")  
    print("---------------------------------------------------------------------------------")
    rel_time = avg_time_astar/avg_time_ssg
    rel_nodes = avg_nodes_astar/avg_nodes_ssg
    print(f"SGG is {rel_time*100}% on average faster than pure A*.")
    print(f"A* haves {floor(rel_nodes)} times more open nodes on avarege than SSG.")

def hundred_point_test(pathfinder, grid, metr, max_width, max_height):
    for i in range(0,100):
        print(f"\n======================== Test {str(i+1)} ========================\n")
        start = create_valid_point(max_width, max_height, grid)
        goal  = create_valid_point(max_width, max_height, grid)
        do_a_star_only_test(start, goal, pathfinder, grid, metr)
        do_ssg_only_test(start, goal, pathfinder, grid, metr)
        grid.reset_vis_graph_vertexes()
        grid.reset_vertexes()
    
    get_average_values_metrics(metr)

def do_ssg_only_test(start, goal, pathfinder, grid, metr):
    test_name = f"SSG {start} -> {goal}"
    metr.reset_info()
    metr.start_counting_time()
    print(f"[{test_name}] started counting time...")
    
    end_node = pathfinder.ssg(start, goal)

    metr.end_counting_time()
    metr.info["elapsed_time"] = metr.time_elapsed
    print(f"[{test_name}] ended counting!")
    print(f"Added test \"{test_name}\" to the log.")
    metr.log[test_name] = metr.info
    metr.log[test_name]["kind"] = "ssg"
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
    metr.info["elapsed_time"] = metr.time_elapsed
    print(f"[{test_name}] ended counting!")
    print(f"Added test \"{test_name}\" to the log.")
    metr.log[test_name] = metr.info
    metr.log[test_name]["kind"] = "a*"
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

    # hundred_point_test(pathfinder, grid, metr, int(grid.info["width"]), int(grid.info["height"]))

    start = (0,0)
    goal  = (1020,1020)
    end_node = do_a_star_only_test(start, goal, pathfinder, grid, metr)
    grid.draw_map(end_node)
    grid.reset_vertexes()
    end_node = do_ssg_only_test(start, goal, pathfinder, grid, metr)
    grid.draw_map(end_node)

if __name__ == '__main__':
    main()