#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Tests for ISMAGS isomorphism algorithm.
"""

from nose.tools import assert_true, assert_equal
from nose import SkipTest
import networkx as nx
from networkx.algorithms import isomorphism as iso


def _matches_to_sets(matches):
    """
    Helper function to facilitate comparing collections of dictionaries in
    which order does not matter.
    """
    return set(map(lambda m: frozenset(m.items()), matches))


class TestSelfIsomorphism(object):
    data = [
        (
            [(0, dict(name='a')),
             (1, dict(name='a')),
             (2, dict(name='b')),
             (3, dict(name='b')),
             (4, dict(name='a')),
             (5, dict(name='a'))],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
        ),
        (
            range(1, 5),
            [(1, 2), (2, 4), (4, 3), (3, 1)]
        ),
        (
            [],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 6), (6, 7),
             (2, 8), (8, 9), (4, 10), (10, 11)]
        ),
        (
            [],
            [(0, 1), (1, 2), (1, 4), (2, 3), (3, 5), (3, 6)]
        ),
    ]

    def test_self_isomorphism(self):
        """
        For some small, symmetric graphs, make sure that 1) they are isomorphic
        to themselves, and 2) that only the identity mapping is found.
        """
        for node_data, edge_data in self.data:
            graph = nx.Graph()
            graph.add_nodes_from(node_data)
            graph.add_edges_from(edge_data)

            ismags = iso.ISMAGS(graph, graph, node_match=iso.categorical_node_match('name', None))
            assert_true(ismags.is_isomorphic())
            assert_true(ismags.subgraph_is_isomorphic())
            assert_equal(list(ismags.subgraph_isomorphisms_iter(symmetry=True)),
                         [{n: n for n in graph.nodes}])

    @SkipTest
    def test_directed_self_isomorphism(self):
        """
        For some small, directed, symmetric graphs, make sure that 1) they are
        isomorphic to themselves, and 2) that only the identity mapping is
        found.
        """
        for node_data, edge_data in self.data:
            graph = nx.Graph()
            graph.add_nodes_from(node_data)
            graph.add_edges_from(edge_data)

            ismags = iso.ISMAGS(graph, graph, node_match=iso.categorical_node_match('name', None))
            assert_true(ismags.is_isomorphic())
            assert_true(ismags.subgraph_is_isomorphic())
            assert_equal(list(ismags.subgraph_isomorphisms_iter(symmetry=True)),
                         [{n: n for n in graph.nodes}])


class TestSubgraphIsomorphism(object):
    

    def test_isomorphism(self):
        g1 = nx.Graph()
        g1.add_cycle(range(4))

        g2 = nx.Graph()
        g2.add_cycle(range(4))
        g2.add_edges_from([(n, m) for n, m in zip(g2, range(4, 8))])
        ismags = iso.ISMAGS(g2, g1)
        assert_equal(list(ismags.subgraph_isomorphisms_iter(symmetry=True)),
                     [{n: n for n in g1.nodes}])

    def test_isomorphism2(self):
        g1 = nx.Graph()
        g1.add_path(range(3))

        g2 = g1.copy()
        g2.add_edge(1, 3)

        ismags = iso.ISMAGS(g2, g1)
        matches = ismags.subgraph_isomorphisms_iter(symmetry=True)
        expected_symmetric = [{0: 0, 1: 1, 2: 2},
                              {0: 0, 1: 1, 3: 2},
                              {2: 0, 1: 1, 3: 2}]
        assert_equal(_matches_to_sets(matches),
                     _matches_to_sets(expected_symmetric))

        matches = ismags.subgraph_isomorphisms_iter(symmetry=False)
        expected_asymmetric = [{0: 2, 1: 1, 2: 0},
                               {0: 2, 1: 1, 3: 0},
                               {2: 2, 1: 1, 3: 0}]
        assert_equal(_matches_to_sets(matches),
                     _matches_to_sets(expected_symmetric + expected_asymmetric))


class TestWikipediaExample(object):
    # Nodes 'a', 'b', 'c' and 'd' form a column.
    # Nodes 'g', 'h', 'i' and 'j' form a column.
    g1edges = [['a', 'g'], ['a', 'h'], ['a', 'i'],
               ['b', 'g'], ['b', 'h'], ['b', 'j'],
               ['c', 'g'], ['c', 'i'], ['c', 'j'],
               ['d', 'h'], ['d', 'i'], ['d', 'j']]

    # Nodes 1,2,3,4 form the clockwise corners of a large square.
    # Nodes 5,6,7,8 form the clockwise corners of a small square
    g2edges = [[1, 2], [2, 3], [3, 4], [4, 1],
               [5, 6], [6, 7], [7, 8], [8, 5],
               [1, 5], [2, 6], [3, 7], [4, 8]]

    def test_graph(self):
        g1 = nx.Graph()
        g2 = nx.Graph()
        g1.add_edges_from(self.g1edges)
        g2.add_edges_from(self.g2edges)
        gm = iso.ISMAGS(g1, g2)
        assert_true(gm.is_isomorphic())


class TestLargestCommonSubgraph(object):
    def test_mcis(self):
        # Example graphs from DOI: 10.1002/spe.588
        graph1 = nx.Graph()
        graph1.add_edges_from([(1, 2), (2, 3), (2, 4), (3, 4), (4, 5)])
        graph1.nodes[1]['color'] = 0

        graph2 = nx.Graph()
        graph2.add_edges_from([(1, 2), (2, 3), (2, 4), (3, 4), (3, 5),
                               (5, 6), (5, 7), (6, 7)])
        graph2.nodes[1]['color'] = 1
        graph2.nodes[6]['color'] = 2
        graph2.nodes[7]['color'] = 2

        ismags = iso.ISMAGS(graph1, graph2, node_match=iso.categorical_node_match('color', None))
        assert_equal(list(ismags.subgraph_isomorphisms_iter(True)), [])
        assert_equal(list(ismags.subgraph_isomorphisms_iter(False)), [])
        found_mcis = _matches_to_sets(ismags.largest_common_subgraph())
        expected = _matches_to_sets([{2: 2, 3: 4, 4: 3, 5: 5},
                                     {2: 4, 3: 2, 4: 3, 5: 5}])
        assert_equal(expected, found_mcis)

        ismags = iso.ISMAGS(graph2, graph1, node_match=iso.categorical_node_match('color', None))
        assert_equal(list(ismags.subgraph_isomorphisms_iter(True)), [])
        assert_equal(list(ismags.subgraph_isomorphisms_iter(False)), [])
        found_mcis = _matches_to_sets(ismags.largest_common_subgraph())
        # Same answer, but reversed.
        expected = _matches_to_sets([{2: 2, 3: 4, 4: 3, 5: 5},
                                     {4: 2, 2: 3, 3: 4, 5: 5}])
        assert_equal(expected, found_mcis)

    def test_symmetry_mcis(self):
        graph1 = nx.Graph()
        graph1.add_path(range(4))
        
        graph2 = nx.Graph()
        graph2.add_path(range(3))
        graph2.add_edge(1, 3)
        
        # Only the symmetry of graph2 is taken into account here.
        ismags = iso.ISMAGS(graph1, graph2, node_match=iso.categorical_node_match('color', None))
        assert_equal(list(ismags.subgraph_isomorphisms_iter(True)), [])
        found_mcis = _matches_to_sets(ismags.largest_common_subgraph())
        expected = _matches_to_sets([{0: 0, 1: 1, 2: 2},
                                     {1: 0, 3: 2, 2: 1}])
        assert_equal(expected, found_mcis)
        
        # Only the symmetry of graph1 is taken into account here.
        ismags = iso.ISMAGS(graph2, graph1, node_match=iso.categorical_node_match('color', None))
        assert_equal(list(ismags.subgraph_isomorphisms_iter(True)), [])
        found_mcis = _matches_to_sets(ismags.largest_common_subgraph())
        expected = _matches_to_sets([{3: 2, 0: 0, 1: 1}, 
                                     {2: 0, 0: 2, 1: 1},
                                     {3: 0, 0: 2, 1: 1},
                                     {3: 0, 1: 1, 2: 2},
                                     {0: 0, 1: 1, 2: 2},
                                     {2: 0, 3: 2, 1: 1}])

        assert_equal(expected, found_mcis)