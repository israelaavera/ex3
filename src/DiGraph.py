from GraphInterface import GraphInterface
from NodeData import NodeData


class DiGraph(GraphInterface):
    """
        This class represent a directed weighted graph.
    """
    def __init__(self):
        """
        A graph constructor.
        nodes_in_graph : dict(int, NodeData)
            dictionary of the nodes on the graph.
        neighbors : dict(int, dict(int, float))
            each node on the graph is added to the dictionary and if he have neighbors
            then we add the neighbor to the value (that is a dictionary) with
             key = neighbor id, val = weight of the edge.
        pointers : dict(int, dict(int, float))
            each node on the graph is added to the dictionary and if he have nodes that pointing at him we add
            them to the value dictionary as (node id: int : weight of the edge: float)
        edge_size : int
            The number of edges on the graph.
        mc_counter : int
            The number of operations that we did on the graph.
        """
        self.__nodes_in_graph = {}  # A dictionary that contains all the nodes on the graph
        self.__neighbors = {}
        self.__pointers = {}  # { '1' : [2,3,4,5],
        self.__edge_size = 0
        self.__mc_counter = 0

    def v_size(self):
        """
        returns the number of nodes on the graph.
        :return:
        int
            The number of nodes on the graph
        """
        return len(self.__nodes_in_graph)

    def e_size(self):
        """
        returns the number of edges on the graph.
        :return:
        int
            The number of edges on the graph
        """
        return self.__edge_size

    def get_all_v(self):
        return self.__nodes_in_graph

    def all_in_edges_of_node(self, id1: int):
        """
        if the node with the given id have nodes that pointing at him then returns a dictionary of all those nodes
        and the weight of the edges.
        :param id1: int
            the node we want to operate on
        :return: dictionary
            dictionary of the nodes that pointing at id1.

        """
        if id1 in self.__nodes_in_graph.keys():
            if self.__pointers.get(id1) is not None:
                return self.__pointers.get(id1)
        else:
            return None

    def all_out_edges_of_node(self, id1: int):
        """
        if the node with the given id have neighbors then returns a dictionary of all those nodes
        and the weight of the edges.
        :param id1: int
            the node we want to operate on
        :return: dictionary
            dictionary of the neighbors nodes
        """
        if id1 in self.__nodes_in_graph:
            if self.__neighbors.get(id1) is not None:
                return self.__neighbors.get(id1)
        else:
            return None

    def get_mc(self):
        """
        :return the number of operations on the graph.
        :return: int
            the number of operations on the graph
        """
        return self.__mc_counter

    def add_node(self, node_id: int, pos: tuple = None):
        """
        Add a new node to the graph, if there is already a node with the given key on the
         graph then the function will do nothing.
        :param node_id: int
            the id of the node we want to add to the graph
        :param pos: float
            the position we want to place the node
        :return: bool
            True if succeed, else False
        """
        if node_id not in self.__nodes_in_graph:
            tmp = NodeData(node_id, pos)
            self.__nodes_in_graph[node_id] = tmp
            self.__neighbors[node_id] = {}
            self.__pointers[node_id] = {}
            self.__mc_counter = self.__mc_counter + 1
            return True
        else:
            return False

    def add_edge(self, id1: int, id2: int, weight: float):
        """
        Add an edge from id1 to id2 (if there is no edge from id1 to id2)
        :param id1: int
            source node
        :param id2: int
            destination node
        :param weight: float
            the weight of the edge
        :return: bool
            True if succeed, else False
        """
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
        """
        Remove the edge between the two given nodes.
        :param node_id1: int
            source node
        :param node_id2: int
            destination node
        :return: bool
            True if succeed, else False
        """
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
        """
            Deletes the node (with the given ID) from the graph and removes all edges which starts
            or ends at this node.
        :param node_id: int
            the node we wish to remove from the graph
        :return: bool
            True if the node removed, else False
        """
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
        """
        display all the nodes on the graph, for example:
        node_a neighbor_of_a weight
        node_c
        .
        .
        .
        node_y neighbor_of_y weight
        :return: string
            Each node on the graph
        """
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



