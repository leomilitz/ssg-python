from grid import Grid
from metrics import Metrics
from pathfinder import Pathfinder

def main():
    metr = Metrics()
    grid = Grid("Berlin_0_1024.map", metr)
    pathfinder = Pathfinder(grid, metr)
    
    start = (0,0)
    goal  = (1020, 1020)
    test_name = f"A* {start} -> {goal}"
    metr.reset_info()
    metr.start_counting_time()
    print(f"[{test_name}] started counting time...")
    
    pathfinder.walk_A_star(start, goal)

    metr.end_counting_time()
    metr.info["elapsed_time"] = str(metr.time_elapsed) + " s"
    print(f"[{test_name}] ended counting!")
    print(f"Added test \"{test_name}\" to the log.")
    metr.log[test_name] = metr.info
    metr.show_metrics_alg(f"A* {start} -> {goal}")
    
    #pathfinder.walk_ssg((0,0), (900, 135))
    grid.draw_map()

if __name__ == '__main__':
    main()