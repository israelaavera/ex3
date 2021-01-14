# ex3

## This project presents the implementation of a weighted and directed graph in python.
### The implementation includes three class:
## NodeData class:
each graph made up of vertices therefore there is another class called NodeData that describes the properties of a vertex and contains methods such as:
* get_key(self).
* get_pos(self).
* get_weight(self).
* get_info(self)
* get_tag(self).
* set_pos(self, p: tuple).
* set_weight(self, t).
* set_info(self, i).
* set_tag(self, t). 
* repr(self)- display the vertex.
* lt(self, other)- compares two vertices based on their weight

## A class of weighted and directed graph called DiGraph:
This class inherits from the abstract class GraphInterface which represents an interface of a graph.
### The DiGraph class contains methods such as:
* graph-v_size(self) -> int - returns the number of vertices in this graph.
* e_size(self) -> int- returns the number of edges in this graph.
* get_all_v(self) -> dict- return a dictionary of all the nodes in the Graph.
* all_in_edges_of_node(self, id1: int) -> dict- return a dictionary of all the nodes connected to (into) node_id.
* all_out_edges_of_node(self, id1: int) -> dict- return a dictionary of all the nodes connected from node_id.
*  get_mc(self) -> int- returns a variable that counts the amount of changes made on the graph.
* add_edge(self, id1: int, id2: int, weight: float) -> bool-  adds an edge to the graph,return True if the edge was added successfully, False o.w.
* add_node(self, node_id: int, pos: tuple = None) -> bool-   adds a node to the graph.
*  remove_node(self, node_id: int) -> bool -removes a node from the graph,return True if the node was removed successfully, False o.w.
* remove_edge(self, node_id1: int, node_id2: int) -> bool- removes an edge from the graph,True if the edge was removed successfully, False o.w.

## The other class is the class of algorithms on graphs called GraphAlgo:
This class inherits from the abstract class GraphAlgoInterface which represents an interface of a graph.
The class contains special algorithms that can be performed on a graph and methods such as:
* get_graph(self) -> GraphInterface- return the directed graph on which the algorithm works on.
* load_from_json(self, file_name: str) -> bool- loads a graph from a json file,return True if the loading was successful, False o.w.
* save_to_json(self, file_name: str) -> bool-  saves the graph in JSON format to a file,return True if the save was successful, False o.w.
* shortest_path(self, id1: int, id2: int) -> (float, list)- returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm.
* connected_component(self, id1: int) -> list- finds the Strongly Connected Component(SCC) that node id1 is a part of and return the list of nodes in this SCC.
* connected_components(self) -> List[list]-  finds all the Strongly Connected Component(SCC) in the graph and return a list all SCC by using scc_check() function that
we will expand about it in the wiki.
.
* plot_graph(self) -> None- Plots the graph,if the nodes have a position the nodes will be placed there ,Otherwise they will be placed in a random but elegant manner.

## So how does it actually work?
if you wish to create a new graph simply write the following code line:

    g = DiGraph()
    
if you want to add a vertex to this graph write:

    g.add_node(x)

 to add a edge between vertex X and vertex Y with a weight of 15 for example write:

     g.add_node(y)
     g.add_edge(x, y, 15)

if you want to run algorithms on the graph you can write the following:

     ga = GraphAlgo(g)
     ga.plot_graph()
     ga.shortest_path(x,y)
     ga.connected_components()
    
### all the special functions and algorithms that we described are available for you ,So enjoy!
      
      

   
 
