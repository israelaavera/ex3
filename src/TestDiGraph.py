import unittest
from DiGraph import DiGraph


class MyTestCase(unittest.TestCase, DiGraph):

    def test_size(self):
        g = DiGraph()
        self.assertEqual(0, g.v_size())
        for i in range(0, 174):
            g.add_node(i)
        self.assertEqual(174, g.v_size())

    def test_e_size(self):
        g = DiGraph()
        self.assertEqual(0, g.e_size())
        for i in range(0, 174):
            g.add_node(i)
        for i in range(0, 20):
            g.add_edge(i, i + 1, i * 2)
        self.assertEqual(20, g.e_size())

    #
    # def test_get_all_v(self):
    #     g = DiGraph()
    #     for i in range(0, 14):
    #         g.add_node(i)

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        for i in range(0, 14):
            g.add_node(i)
        self.assertEqual(0, len(g.all_in_edges_of_node(0)))
        for i in range(8, 14):
            g.add_edge(i, 0, i * 2)
        self.assertEqual(6, len(g.all_in_edges_of_node(0)))

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        for i in range(0, 14):
            g.add_node(i)
        self.assertEqual(0, len(g.all_out_edges_of_node(0)))
        for i in range(8, 14):
            g.add_edge(0, i, i * 2)
        self.assertEqual(6, len(g.all_out_edges_of_node(0)))

    def test_get_mc(self):
        g = DiGraph()
        self.assertNotEqual(150, g.get_mc())
        self.assertEqual(0,g.get_mc())
        g.add_node(1)
        g.add_node(2)
        self.assertEqual(2, g.get_mc())
        g.add_edge(1, 2, 15)
        self.assertEqual(3, g.get_mc())
        g.remove_node(2)
        self.assertEqual(5, g.get_mc())

    def test_add_node(self):
        g = DiGraph()
        g.add_node(1)
        self.assertTrue(g.add_node(2))
        self.assertFalse(g.add_node(2))

    def test_add_edge(self):
        g = DiGraph()
        g.add_node(1)
        self.assertFalse(g.add_edge(1, 1, 15))
        g.add_node(2)
        self.assertTrue(g.add_edge(1, 2, 15))

    def test_remove_edge(self):
        g = DiGraph()
        self.assertFalse(g.remove_edge(4, 3))
        g.add_node(3)
        g.add_node(4)
        g.add_edge(3, 4, 12)
        self.assertTrue(g.remove_edge(3, 4))

    def test_remove_node(self):
        g = DiGraph()
        self.assertFalse(g.remove_node(20))
        g.add_node(15)
        g.add_node(2)
        g.add_node(184)
        self.assertFalse(g.remove_node(20))
        self.assertTrue(g.remove_node(184))


if __name__ == '__main__':
    unittest.main()
