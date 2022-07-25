from grid import Grid
from metrics import Metrics
from pathfinder import Pathfinder

def main():
    metr = Metrics()
    grid = Grid("Berlin_0_1024.map", metr)
    pathfinder = Pathfinder(grid, metr)
    pathfinder.walk_A_star((0,0), (900, 135))
    metr.show_metrics_alg(f"A* {(0,0)} -> {(900, 135)}")
    grid.draw_map()

if __name__ == '__main__':
    main()