from grid import Grid
from metrics import Metrics
from pathfinder import Pathfinder

def main():
    metr = Metrics()
    #grid = Grid("Berlin_0_1024.map", metr)
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
    #pathfinder.walk_A_star(start_idx, goal_idx)
    pathfinder.walk_ssg(start_idx, goal_idx)

    metr.end_counting_time()
    metr.info["elapsed_time"] = str(metr.time_elapsed) + " s"
    print(f"[{test_name}] ended counting!")
    print(f"Added test \"{test_name}\" to the log.")
    metr.log[test_name] = metr.info
    metr.show_metrics_alg(f"A* {start_idx} -> {goal_idx}")
    
    grid.draw_map()

if __name__ == '__main__':
    main()