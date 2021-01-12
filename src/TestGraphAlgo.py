import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):
    def test_init(self):
        g = DiGraph()
        ga = GraphAlgo(g)
        self.assertEqual(g, ga.get_graph())

    def test_get_graph(self):
        g = DiGraph()
        ga = GraphAlgo(g)
        f = DiGraph()
        self.assertNotEqual(ga.get_graph(), f)
        self.assertEqual(g, ga.get_graph())

    def test_set_graph(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.set_graph(g)
        self.assertIsNotNone(ga.get_graph())

    def test_shortest_path(self):
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
        temp = ga.shortest_path(0, 2)
        self.assertEqual(4, temp[0])
        self.assertEqual([0, 1, 2], temp[1])

        # not works
        temp = ga.shortest_path(2, 0)
        self.assertEqual(float('inf'), temp[0])
        self.assertEqual([], temp[1])

    def test_connected_component(self):
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
        temp = ga.connected_component(1)
        self.assertIn(g.get_all_v().get(1), temp)
        self.assertIn(g.get_all_v().get(2), temp)
        # not works
        temp = ga.connected_component(0)
        self.assertNotIn(g.get_all_v().get(1), temp)

    def test_connected_components(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        ga = GraphAlgo(g)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 9)
        g.add_edge(1, 2, 3)
        g.add_edge(2, 1, 3)
        self.assertEqual(2, len(ga.connected_components()))

    def test_save_to_json(self):
        g = DiGraph()
        ga = GraphAlgo(g)
        g.add_node(0)
        self.assertTrue(ga.save_to_json('testSave.json'))

    def test_load_from_json(self):
        g = DiGraph()
        ga = GraphAlgo(g)
        self.assertTrue(ga.load_from_json('testSave.json'))

    def test_dijkstra(self):
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
        ga.dijkstra(g.get_all_v().get(0))
        self.assertEqual(3, ga.get_dijkstra_counter())
        # not works
        ga.dijkstra(g.get_all_v().get(2))
        self.assertNotEqual(3, ga.get_dijkstra_counter())
    def test_tarjan(self):
        g = DiGraph()
        ga = GraphAlgo(g)
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_node(4)
        g.add_node(5)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 9)
        g.add_edge(1, 2, 3)
        g.add_edge(2, 1, 3)
        g.add_edge(1, 4, 1)
        g.add_edge(4, 5, 2)
        g.add_edge(5, 4, 234)
        g.add_edge(3, 5, 2)
        g.add_edge(2, 3, 4)
        self.assertEqual(4, len(ga.tarjan()))

if __name__ == '__main__':
    unittest.main()
