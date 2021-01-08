from GraphInterface import GraphInterface
from NodeData import NodeData


class DiGraph(GraphInterface):

    #  default constructor
    def __init__(self):
        self.__nodes_in_graph = {}  # A dictionary that contains all the nodes on the graph
        self.__neighbors = {}
        self.__pointers = {}  # { '1' : [2,3,4,5],
        self.__edge_size = 0
        self.__mc_counter = 0

    def v_size(self):
        return len(self.__nodes_in_graph)

    def e_size(self):
        return self.__edge_size

    def get_all_v(self):
        return self.__nodes_in_graph

    def all_in_edges_of_node(self, id1: int):
        if id1 in self.__nodes_in_graph.keys():
            if self.__pointers.get(id1) is not None:
                return self.__pointers.get(id1)
        else:
            return None

    def all_out_edges_of_node(self, id1: int):
        if id1 in self.__nodes_in_graph:
            if self.__neighbors.get(id1) is not None:
                return self.__neighbors.get(id1)
        else:
            return None

    def get_mc(self):
        return self.__mc_counter

    def add_node(self, node_id: int, pos: tuple = None):
        if node_id not in self.__nodes_in_graph:
            tmp = NodeData(node_id, pos)
            #  string_id = f"{node_id}"
            #  tmp = super(NodeData(node_id, pos))
            self.__nodes_in_graph[node_id] = tmp
            # print(self.__nodes_in_graph[node_id])
            self.__neighbors[node_id] = {}
            self.__pointers[node_id] = {}
            self.__mc_counter = self.__mc_counter + 1
            return True
        else:
            # print('Already added')
            return False

    #  { "1" : {"2" : 1, "4" : 5},...}
    def add_edge(self, id1: int, id2: int, weight: float):
        if (id1 in self.__nodes_in_graph) and (id2 in self.__nodes_in_graph) and (id1 != id2):
            if self.__neighbors.get(id1) is not None:
                if id2 in self.__neighbors.get(id1):
                    return False
                else:
                    self.__neighbors.get(id1)[id2] = weight
                    self.__pointers.get(id2)[id1] = weight
                    self.__edge_size = self.__edge_size + 1
                    self.__mc_counter = self.__mc_counter + 1
                    return True
            else:
                return False
        else:
            return False

    def remove_edge(self, node_id1: int, node_id2: int):
        if node_id1 in self.__nodes_in_graph and node_id2 in self.__nodes_in_graph:
            if node_id2 in self.__neighbors.get(node_id1):
                del self.__neighbors.get(node_id1)[node_id2]
                del self.__pointers.get(node_id2)[node_id1]
                self.__edge_size = self.__edge_size - 1
                self.__mc_counter = self.__mc_counter + 1
                return True
        else:
            return False

    def remove_node(self, node_id: int):
        if node_id in self.__nodes_in_graph:
            if (self.__neighbors.get(node_id) is not None) and (len(self.__neighbors.get(node_id)) > 0):
                print(list(self.__neighbors.get(node_id)))
                for node in list(self.__neighbors.get(node_id)):
                    self.remove_edge(node_id, node)
            if self.__pointers.get(node_id).keys() is not None:
                for node in list(self.__pointers.get(node_id)):
                    self.remove_edge(node, node_id)
            del self.__nodes_in_graph[node_id]
            del self.__pointers[node_id]
            del self.__neighbors[node_id]
            self.__mc_counter = self.__mc_counter + 1
            return True
        else:
            return False

    def __str__(self):
        ans = ''
        for node_id in self.__nodes_in_graph:
            if (self.__neighbors.get(node_id) is not None) and (len(self.__neighbors.get(node_id)) > 0):
                for n in self.__neighbors.get(node_id).keys():
                    ans = ans + f'{node_id} {n} {self.__neighbors.get(node_id).get(n)} \n'
            else:
                ans = ans + f'{node_id} \n'
        return ans

    def get_node_list(self, node_id_list):
        ans = []
        for i_el in node_id_list:
            ans.append(self.__nodes_in_graph.get(i_el))
        return ans


if __name__ == '__main__':
    g = DiGraph()
    g.add_node(0)
    for i in range(1, 15):
        g.add_node(i)
        g.add_edge(0, i, i + 1)
    g.add_edge(1, 0, 3)
    g.add_edge(2, 0, 4)
    g.add_edge(3, 0, 52)
    print(g)

    g.remove_node(0)

    print(g)
