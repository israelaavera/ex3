import json
from typing import List
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
# from queue import PriorityQueue
import heapq
# from src import GraphInterface
import numpy as np
import matplotlib.pyplot as plt
import random


class GraphAlgo(GraphAlgoInterface):
    time = 0
    components = []  # list(list
    low_link = {}
    stack = []

    def __init__(self, graph=None):
        self.__g = graph
        self.__dijkstra_counter = 0

    def get_dijkstra_counter(self):
        return  self.__dijkstra_counter

    def get_graph(self):
        return self.__g

    def set_graph(self, ng: DiGraph):
        self.__g = ng

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        src_node = self.get_graph().get_all_v().get(id1)
        dst_node = self.get_graph().get_all_v().get(id2)
        if src_node is None and dst_node is None:
            ans = (None, [])
            return ans
        if id1 == id2:
            ans = (0, [id1])
            return ans
        ans = []
        self.dijkstra(src_node)
        tmp = dst_node
        while tmp is not src_node and tmp.get_tag() != -1:
            ans.append(tmp.get_key())
            if self.get_graph().get_all_v().get(tmp.get_tag()) is not None:
                tmp = self.get_graph().get_all_v().get(tmp.get_tag())
        if dst_node.get_tag() == -1:
            return float('inf'), []

        ans.append(tmp.get_key())
        ans.reverse()
        final_ans = (dst_node.get_weight(), ans)
        return final_ans

    def connected_component(self, id1: int) -> list:
        cc_list = self.connected_components()
        node = self.get_graph().get_all_v().get(id1)
        for i in cc_list:
            if node in i:
                return i

    def connected_components(self) -> List[list]:
        GraphAlgo.components.clear()
        GraphAlgo.time = 0
        GraphAlgo.low_link.clear()
        GraphAlgo.stack.clear()
        ans = self.tarjan()
        return ans

    def plot_graph(self) -> None:
        temp_list = []
        xy_list = []
        for node_i in self.get_graph().get_all_v().values():
            if node_i.get_pos() is not None:
                xy_list.append(node_i.get_pos())
            else:
                temp_list.append(node_i)
        if len(xy_list) == 0:
            node_tm = temp_list[0]
            node_tm.set_pos((0, 0, 0))
            xy_list.append((0, 0, 0))
            del temp_list[0]
        for node_i in temp_list:
            x1, y1 = random.randint(-10, 11), random.randint(-10, 11)
            # =======================================================
            if -2 <= x1 <= 2:
                if x1 < 0:
                    x1 = x1 - 3
                else:
                    x1 = x1 + 3
            if -2 <= y1 <= 2:
                if y1 < 0:
                    y1 = y1 - 3
                else:
                    y1 = y1 + 3
            # =======================================================
            ind = random.randint(0, len(xy_list)) - 1
            ans = (x1 + xy_list[ind][0], y1 + xy_list[ind][1], 0)
            while ans in xy_list:
                x1, y1 = random.randint(-10, 11), random.randint(-10, 11)
                # =======================================================
                if -2 <= x1 <= 2:
                    if x1 < 0:
                        x1 = x1 - 3
                    else:
                        x1 = x1 + 3
                if -2 <= y1 <= 2:
                    if y1 < 0:
                        y1 = y1 - 3
                    else:
                        y1 = y1 + 3
                # =======================================================
                ind = random.randint(0, len(xy_list)) - 1
                ans = (x1 + xy_list[ind][0], y1 + xy_list[ind][1],  0)
            xy_list.append(ans)
            node_i.set_pos(ans)
        for node_i in self.get_graph().get_all_v().keys():  # Iterate over node key
            x1, y1, z1 = self.get_graph().get_all_v().get(node_i).get_pos()
            if len(self.get_graph().all_out_edges_of_node(node_i)) > 0:
                for node_j in self.get_graph().all_out_edges_of_node(node_i).keys():  # Iterate over neighbors of node_i
                    x2, y2, z2 = self.get_graph().get_all_v().get(node_j).get_pos()
                    plt.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->"))
                    plt.annotate(f'{self.get_graph().all_out_edges_of_node(node_i).get(node_j)}', xy=(x2, y2),
                                 xytext=((x1 + x2) / 2, (y1 + y2) / 2), color='blue')
        for node in self.get_graph().get_all_v().values():
            x, y , z = node.get_pos()
            plt.scatter(x, y, color='c', s=50)  # Draw a vertex
            plt.text(x, y, f'{node.get_key()}', color='red', weight='bold', size=13)
        plt.show()

    def load_from_json(self, file_name: str) -> bool:
        new_graph = DiGraph()
        try:
            with open(file_name, "r") as f:
                s_tmp = f.read()
                new_dict = json.loads(s_tmp)
                nodes_arr = new_dict.get("Nodes")
                for a in nodes_arr:
                    chosen_xyz = None  # if there is no pos in the json file
                    if a.get('pos') is not None:  # if there is a position in the json file
                        if len(a.get('pos')) > 0:
                            x_s, y_s, z_s = a.get('pos').split(',')
                            x = float(x_s)
                            y = float(y_s)
                            z = float(z_s)
                            chosen_xyz = (x, y, z)
                            new_graph.add_node(a.get('id'), chosen_xyz)
                        else:
                            new_graph.add_node(a.get('id'), chosen_xyz)
                edges_arr = new_dict.get("Edges")
                for a in edges_arr:
                    new_graph.add_edge(a.get("src"), a.get("dest"), a.get("w"))
                self.set_graph(new_graph)
                return True
        except IOError as e:
            # print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        ans_temp = {"Nodes": [], "Edges": []}
        for tmp_id in self.get_graph().get_all_v().keys():
            if self.get_graph().get_all_v().get(tmp_id).get_pos() is None:
                ans_temp.get("Nodes").append({"id": tmp_id, "pos": ""})
            else:
                # ans_temp.get("Nodes").append({"id": tmp_id})
                x = self.get_graph().get_all_v().get(tmp_id).get_pos()[0]
                y = self.get_graph().get_all_v().get(tmp_id).get_pos()[1]
                z = self.get_graph().get_all_v().get(tmp_id).get_pos()[2]
                ans_temp.get("Nodes").append({"id": tmp_id, "pos":f'{x},{y},{z}'})
        for tmp_id in self.get_graph().get_all_v().keys():
            if self.get_graph().all_out_edges_of_node(tmp_id) is not None:
                for tmp2 in self.get_graph().all_out_edges_of_node(tmp_id).keys():
                    ans_temp.get("Edges").append(
                        {"src":tmp_id,"dest":tmp2,"w":self.get_graph().all_out_edges_of_node(tmp_id).get(tmp2)})

        ans = json.dumps(ans_temp)
        try:
            f = open(file_name, "w")
            f.write(ans)
            f.close()
            return True
        except FileExistsError as e:
            print(e)
            return False

    def dijkstra(self, start_node):
        self.__dijkstra_counter = 0
        start_node.set_weight(0)
        start_node.set_tag(-1)
        start_node.set_info('W')
        node_c = list(self.get_graph().get_all_v().values())
        for node1 in node_c:
            if node1.get_key() != start_node.get_key():
                node1.set_weight(float('inf'))
                node1.set_tag(-1)
                node1.set_info('W')
        node_c.clear()
        node_c.append(start_node)
        heapq.heapify(node_c)
        # print(list(node_c))
        while len(node_c) > 0:
            polled_node = heapq.heappop(node_c)
            a_id_list = list(self.get_graph().all_out_edges_of_node(polled_node.get_key()))
            print(a_id_list)
            a_node_list = self.get_graph().get_node_list(a_id_list)
            for i in a_node_list:
                adj = i
                if adj.get_info() == 'W':
                    total_weight = polled_node.get_weight() + self.get_graph().all_out_edges_of_node(
                        polled_node.get_key()).get(adj.get_key())
                    if total_weight < adj.get_weight():
                        if adj in node_c:
                            node_c.remove(adj)
                        adj.set_weight(total_weight)
                        adj.set_tag(polled_node.get_key())
                        if adj not in node_c:
                            heapq.heappush(node_c, adj)
            polled_node.set_info('B')
            print(polled_node)
            self.__dijkstra_counter = self.__dijkstra_counter + 1

    def tarjan(self):
        GraphAlgo.components.clear()
        GraphAlgo.time = 0
        GraphAlgo.low_link.clear()
        GraphAlgo.stack.clear()
        # GraphAlgo.low_link = [0] * (len(self.get_graph().get_all_v()) + 1)
        #   print(self.low_link)
        for node_i in self.get_graph().get_all_v().values():
            if node_i.get_info() != 'Visited':
                self.dfs(node_i)
        self.restore_nodes()
        return self.components

    def dfs(self, u):
        # print(len(GraphAlgo.low_link))
        # print(u.get_key())
        GraphAlgo.low_link[u.get_key()] = GraphAlgo.time
        GraphAlgo.time = GraphAlgo.time + 1
        u.set_info('Visited')
        GraphAlgo.stack.append(u)
        u_is_component_root = True
        arr_index_temp = self.get_graph().all_out_edges_of_node(u.get_key())
        arr_nodes_temp = self.get_graph().get_node_list(arr_index_temp)
        for v in arr_nodes_temp:
            if v.get_info() != 'Visited':
                self.dfs(v)
            if GraphAlgo.low_link[u.get_key()] > GraphAlgo.low_link[v.get_key()]:
                GraphAlgo.low_link[u.get_key()] = GraphAlgo.low_link[v.get_key()]
                u_is_component_root = False
        if u_is_component_root:
            component = []
            while True:
                x = GraphAlgo.stack.pop()
                component.append(x)
                GraphAlgo.low_link[x.get_key()] = 10000 * 100000
                if x.get_key() == u.get_key():
                    break
            GraphAlgo.components.append(component)

    def restore_nodes(self):
        if len(self.get_graph().get_all_v()) > 0:
            for node_a in self.get_graph().get_all_v().values():
                node_a.set_info('W')


if __name__ == '__main__':
                        # g = DiGraph()
                        # ga = GraphAlgo(g)
                        # g.add_node(0, (0, 2, 4))
                        # g.add_node(1, (2, 5, 6))
                        # g.add_node(2)
                        # g.add_node(3)
                        # g.add_node(4)
                        #
                        # ga.load_from_json('A5')
                        # ga.save_to_json('json_graph.json')
                        # # ga.save_to_json('json_graph.json')
                        # # ga.load_from_json('T0.json')
                        # print(ga.get_graph().get_all_v().keys())
                        # ga.plot_graph()
                g = DiGraph()
                g.add_node(0)
                g.add_node(1)
                g.add_node(2)
                ga = GraphAlgo(g)
                g.add_edge(0, 1, 1)
                g.add_edge(0, 2, 9)
                g.add_edge(1, 2, 3)
                g.add_edge(2, 1, 3)

                        # works
                        # ga.dijkstra(g.get_all_v().get(0))
                        # self.assertEqual(3, ga.get_dijkstra_counter())
                        # not works
                ga.dijkstra(g.get_all_v().get(2))
