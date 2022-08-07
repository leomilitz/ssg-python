from grid import Grid
from metrics import Metrics
from pathfinder import Pathfinder

def main():
    metr = Metrics()
    grid = Grid("Denver_2_1024.map", metr)
    grid.create_visibility_graph()
    metr.show_metrics_map()
    pathfinder = Pathfinder(grid, metr)
    
    start_idx = (0,0)
    goal_idx = (1020,1020)
    test_name = f"A* {start_idx} -> {goal_idx}"
    metr.reset_info()
    metr.start_counting_time()
    print(f"[{test_name}] started counting time...")
    end_node = pathfinder.a_star(grid.vertexes[start_idx[0]][start_idx[1]], grid.vertexes[goal_idx[0]][goal_idx[1]])
    #end_node = pathfinder.ssg(start_idx, goal_idx)

    metr.end_counting_time()
    metr.info["elapsed_time"] = str(metr.time_elapsed) + " s"
    print(f"[{test_name}] ended counting!")
    print(f"Added test \"{test_name}\" to the log.")
    metr.log[test_name] = metr.info
    metr.show_metrics_alg(f"A* {start_idx} -> {goal_idx}")
    
    grid.draw_map(end_node)

if __name__ == '__main__':
    main()