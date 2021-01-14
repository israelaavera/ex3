import json
import sys
import time
from typing import List
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from NodeData import NodeData
# from queue import PriorityQueue
import heapq
# from src import GraphInterface
import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx


class GraphAlgo(GraphAlgoInterface):
    components = [[]]  # list(list

    def __init__(self, graph=None):
        self.__g = graph
        self.__dijkstra_counter = 0

    def get_dijkstra_counter(self):
        return self.__dijkstra_counter

    def get_graph(self) -> DiGraph:
        return self.__g

    def set_graph(self, ng: DiGraph):
        self.__g = ng

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        start_time = time.time()
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
        diff = time.time() - start_time
        print(f'Shortest path time is: {diff}')
        return final_ans

    def connected_component(self, id1: int) -> list:
        start_time = time.time()
        cc_list = self.connected_components()
        node = self.get_graph().get_all_v().get(id1)
        for i in cc_list:
            if node in i:
                diff = time.time() - start_time
                print(f'connected component time is: {diff}')
                return i

    def connected_components(self) -> List[list]:
        start_time = time.time()
        GraphAlgo.components.clear()
        ans = self.scc_check()
        diff = time.time() - start_time
        print(f'connected components time is: {diff}')
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
                ans = (x1 + xy_list[ind][0], y1 + xy_list[ind][1], 0)
            xy_list.append(ans)
            node_i.set_pos(ans)
        for node_i in self.get_graph().get_all_v().keys():  # Iterate over node key
            x1, y1, z1 = self.get_graph().get_all_v().get(node_i).get_pos()
            if len(self.get_graph().all_out_edges_of_node(node_i)) > 0:
                for node_j in self.get_graph().all_out_edges_of_node(node_i).keys():  # Iterate over neighbors of node_i
                    x2, y2, z2 = self.get_graph().get_all_v().get(node_j).get_pos()
                    plt.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->"))
                    # plt.annotate(f'{self.get_graph().all_out_edges_of_node(node_i).get(node_j)}', xy=(x2, y2),
                    #              xytext=((x1 + x2) / 2, (y1 + y2) / 2), color='blue')
        for node in self.get_graph().get_all_v().values():
            x, y, z = node.get_pos()
            plt.scatter(x, y, color='r', s=50)  # Draw a vertex
            plt.text(x, y, f'{node.get_key()}', color='g', weight='bold', size=13)
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
                ans_temp.get("Nodes").append({"id": tmp_id, "pos": f'{x},{y},{z}'})
        for tmp_id in self.get_graph().get_all_v().keys():
            if self.get_graph().all_out_edges_of_node(tmp_id) is not None:
                for tmp2 in self.get_graph().all_out_edges_of_node(tmp_id).keys():
                    ans_temp.get("Edges").append(
                        {"src": tmp_id, "dest": tmp2, "w": self.get_graph().all_out_edges_of_node(tmp_id).get(tmp2)})

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
            # print(a_id_list)
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
            self.__dijkstra_counter = self.__dijkstra_counter + 1

    def scc_check(self):
        list1 = []
        list2 = []
        visited_for_scc = []
        for node in self.get_graph().get_all_v().values():
            if node.get_key() not in visited_for_scc:
                list1.clear()
                self.bfs(node, list1, True)
                list2.clear()
                self.restore_nodes()
                self.bfs(node, list2, False)
                component = []
                for item in list1:
                    if item in list2:
                        component.append(item)
                self.components.append(component)
                self.restore_nodes()
                for item in component:
                    visited_for_scc.append(item.get_key())
        return self.components

    def bfs(self, src: NodeData, list_i: [NodeData], in_or_out: bool):
        if src in self.get_graph().get_all_v().values():
            q = []
            src.set_info('Visited')
            q.append(src)
            list_i.append(src)
            while len(q) > 0:
                temp = q.pop()
                if in_or_out:
                    nodes_ni_list = self.get_graph().get_node_list(self.get_graph().all_out_edges_of_node(temp.get_key()).keys())
                else:
                    nodes_ni_list = self.get_graph().get_node_list(self.get_graph().all_in_edges_of_node(temp.get_key()).keys())
                for neighbor in nodes_ni_list:
                    if neighbor.get_info() != 'Visited':
                        neighbor.set_info('Visited')
                        q.append(neighbor)
                        list_i.append(neighbor)

    def restore_nodes(self):
        if len(self.get_graph().get_all_v()) > 0:
            for node_a in self.get_graph().get_all_v().values():
                node_a.set_info('W')


if __name__ == '__main__':
    g = DiGraph()
    ga = GraphAlgo(g)
    print(ga.load_from_json('G_30000_240000_2.json'))
    ga.connected_components()
    ga.connected_component(0)
    # print(ga.get_graph())
    ga.shortest_path(0, 9)