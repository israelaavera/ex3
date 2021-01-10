import json
from typing import List
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
# from queue import PriorityQueue
import heapq
# from src import GraphInterface


class GraphAlgo(GraphAlgoInterface):
    time = 0
    components = []  # list(list
    low_link = {}
    stack = []

    def __init__(self, graph=None):
        self.__g = graph
        self.__dijkstra_counter = 0

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
        while tmp is not src_node:
            ans.append(tmp.get_key())
            if self.get_graph().get_all_v().get(tmp.get_tag()) is not None:
                tmp = self.get_graph().get_all_v().get(tmp.get_tag())
        ans.append(tmp.get_key())
        ans.reverse()
        final_ans = (dst_node.get_weight(), ans)
        return final_ans

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        ans = self.tarjan()
        return ans

    def plot_graph(self) -> None:
        pass

    def load_from_json(self, file_name: str) -> bool:
        new_graph = DiGraph()
        try:
            with open(file_name, "r") as f:
                s_tmp = f.read()
                # print(s_tmp)
                new_dict = json.loads(s_tmp)
                # print(type(new_dict))
                nodes_arr = new_dict.get("Nodes")
                # print(nodes_arr)
                for a in nodes_arr:
                    new_graph.add_node(a.get('id'))
                edges_arr = new_dict.get("Edges")
                for a in edges_arr:
                    new_graph.add_edge(a.get("src"), a.get("dest"), a.get("w"))
                self.set_graph(new_graph)
                return True
        except IOError as e:
            print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        ans_temp = {"Nodes": [], "Edges": []}
        for tmp_id in self.get_graph().get_all_v().keys():
            ans_temp.get("Nodes").append({"id": tmp_id})
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
        heapq.heapify(node_c)
        # print(list(node_c))
        while len(node_c) > 0:
            polled_node = heapq.heappop(node_c)
            a_id_list = list(self.get_graph().all_out_edges_of_node(polled_node.get_key()))
            a_node_list = self.get_graph().get_node_list(a_id_list)
            for i in a_node_list:
                adj = i
                if adj.get_info() == 'W':
                    total_weight = polled_node.get_weight() + self.get_graph().all_out_edges_of_node(
                        polled_node.get_key()).get(adj.get_key())
                    if total_weight < adj.get_weight():
                        node_c.remove(adj)
                        adj.set_weight(total_weight)
                        adj.set_tag(polled_node.get_key())
                        heapq.heappush(node_c, adj)
            polled_node.set_info('B')
            self.__dijkstra_counter = self.__dijkstra_counter + 1

    def tarjan(self):
        GraphAlgo.time = 0
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
    g = DiGraph()
    ga = GraphAlgo(g)

    # g.add_node(1)
    # g.add_node(2)
    # g.add_node(3)
    # g.add_node(4)
    # g.add_edge(1, 4, 8)
    # g.add_edge(1, 2, 3)
    # g.add_edge(2, 3, 5)
    # g.add_edge(4, 3, 2)
    # ga.dijkstra(g.get_all_v().get(1))
    # for node in g.get_all_v().values():
    #     print(node)
    #     print(node.get_weight())
    #     print('---------------')
    # tmp2 = ga.shortest_path(1, 3)
    # print(tmp2)
    # ga.tarjan()
    # g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    # g.add_node(5)
    # g.add_node(6)
    # g.add_node(7)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 1, 1)
    g.add_edge(3, 4, 1)
    # g.add_edge(0, 7, 4)
    # g.add_edge(6, 4, 3)
    # //ga.save_to_json('json_graph.json')
    # //ga.load_from_json('json_graph.json')
    print(ga.tarjan())
    # print(ga.get_graph())