import time

"""
Classe para guardar as métricas dos testes realizados.
"""
class Metrics():
    def __init__(self):
        self.info = ""
        self.time_start = 0.0
        self.time_end = 0.0
        self.time_elapsed = 0.0
        
        self.map_creation_info = {
            "map_time": 0.0,
            "width:": 0.0,
            "height:": 0.0,
            "vis_graph_time": 0.0,
            "vis_graph_size": 0
        }
        
        self.reset_info()
        self.log = {}

    def reset_info(self):
        self.info = {
            "elapsed_time": 0.0,
            "open_nodes": 0,
            "closed_nodes": 0,
            "distance": 0
        }

    def start_counting_time(self):
        self.time_start= time.time()

    def end_counting_time(self):
        self.time_end = time.time()
        self.time_elapsed = self.time_end - self.time_start

    def show_metrics_alg(self, test_name):
        test = self.log[test_name]
        print(f"\n----------------- Metrics: {test_name} -----------------\n")
        print(f"Elapsed Time:          {test['elapsed_time']}")
        print(f"Opened Nodes:          {test['open_nodes']}")
        print(f"Distance Traveled (g): {test['distance']}")
        print(f"\n---------------------------------------------" + len(test_name)*"-" + "\n")

    def show_metrics_map(self):
        print(f"\n----------------- Map Metrics -----------------------\n")
        print(f"Map Creation Time: {self.map_creation_info['map_time']}")
        print(f"Map Width:         {self.map_creation_info['width']}")
        print(f"Map Height:        {self.map_creation_info['height']}")
        print(f"\n-----------------------------------------------------\n")
    
    def show_metrics_vis_graph(self):
        print(f"\n------------ Visibility Graph Metrics ------------\n")
        print(f"Vis. Graph Creation Time: {self.map_creation_info['vis_graph_time']}")
        print(f"Vis. Graph Size:          {self.map_creation_info['vis_graph_size']}")
        print(f"\n--------------------------------------------------\n")
