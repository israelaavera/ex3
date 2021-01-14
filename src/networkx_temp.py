import json
import time

import matplotlib.pyplot as plt
import networkx as nx


class NetworkxTemp:
    def __init__(self):
        self.__g = nx.DiGraph()

    def load_from_json(self, file_name: str) -> bool:
        new_graph = nx.DiGraph()
        try:
            with open(file_name, "r") as f:
                s_tmp = f.read()
                new_dict = json.loads(s_tmp)
                nodes_arr = new_dict.get("Nodes")
                for a in nodes_arr:
                    new_graph.add_node(a.get('id'))
                edges_arr = new_dict.get("Edges")
                for a in edges_arr:
                    new_graph.add_edge(a.get("src"), a.get("dest"), weight = a.get("w"))
                self.__g = new_graph
                return True
        except IOError as e:
            # print(e)
            return False
    def get_graph(self):
        return self.__g
if __name__ == '__main__':
    g = NetworkxTemp()
    g.load_from_json('G_30000_240000_2.json')
    a = g.get_graph()
    start_time = time.time()
    nx.strongly_connected_components(a)
    diff = time.time() - start_time
    print(f'connected components time is: {diff}')
    start_time = time.time()
    nx.dijkstra_path(a, 0, 9)
    diff = time.time() - start_time
    print(f'Shortest path time is: {diff}')
