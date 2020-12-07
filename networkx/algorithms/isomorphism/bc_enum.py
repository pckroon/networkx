from itertools import product


class ConnectedClique:
    def __init__(self, product_graph, nodes, head=None):
        self.graph = product_graph
        self.nodes = nodes
        self.head = head or min(nodes)
        self.distances = ...

    def order(self, head=None):
        if head is None:
            return self.distances
        seen = [head]
        distances = [0]
        current = 0
        while set(seen) != set(self.nodes):
            to_see = seen[current]
            neighbours = set(self.graph.neighbours(to_see)).intersection(self.nodes) - set(seen)
            seen.extend(neighbours)
            distances.extend([distances[current]+1] * len(neighbours))
            current += 1

        return zip(distances, seen)


class ProductGraph:
    def __init__(self, graph1, graph2):
        self.graph1 = graph1
        self.graph2 = graph2
        # self.nodes1 = list(graph1)
        # self.nodes2 = list(graph2)

    # @property
    # def nodes(self):
    #     yield from range(len(self.graph1) * len(self.graph2))

    # def map(self, node_idx, node_jdx=None):
    #     if node_jdx is None:
    #         # map product node to nodes in graph1 and 2
    #         node_idx, node_jdx = divmod(node_idx, len(self.graph1))
    #         return self.nodes1[node_idx], self.nodes2[node_jdx]
    #     else:
    #         # graph1 and 2 nodes, to product node
    #         return self.nodes1.index(node_idx) * len(self.graph1) + self.nodes2.index(node_jdx)

    def has_edge(self, idx, jdx):
        idx1, idx2 = idx
        jdx1, jdx2 = jdx
        g1_edge = self.graph1.has_edge(idx1, jdx1)
        g2_edge = self.graph2.has_edge(idx2, jdx2)
        return (g1_edge and g2_edge) or (not g1_edge and not g2_edge)

    def expands_clique(self, clique, candidate):
        is_connected = False
        black_connected = False
        can_idx, can_jdx = candidate
        for node in clique:
            node_idx, node_jdx = node
            g1_edge = self.graph1.has_edge(can_idx, node_idx)
            g2_edge = self.graph2.has_edge(can_jdx, node_jdx)
            black_edge = g1_edge and g2_edge
            white_edge = not g1_edge and not g2_edge
            # Must be connected to all nodes, so and. And it can be connected by
            # either a black or white edge.
            is_connected = is_connected and (black_edge or white_edge)
            if not is_connected:
                return False
            # One black edge is enough
            black_connected = black_connected or black_edge
        return black_connected and is_connected

    def neighbours(self, node):
        node_idx, node_jdx = node
        neighbours1 = set(self.graph1[node_idx])
        neighbours2 = set(self.graph2[node_jdx])
        black_edges = ((idx, jdx) for idx, jdx in product(neighbours1, neighbours2))
        # white_edges = ((idx, jdx) for idx, jdx in
        #                   product(set(self.graph1) - neighbours1,
        #                           set(self.graph2) - neighbours2)
        #               )
        yield from black_edges
        # yield from white_edges

    def candidates(self, clique):
        out = set()
        for node in clique:
            out.update(self.neighbours(node))
        return out

    def order(self, clique, head=None):
        if head is None:
            head = min(clique)
        seen = [head]
        distances = [0]
        current = 0
        while set(seen) != set(clique):
            to_see = seen[current]
            neighbours = set(self.neighbours(to_see)).intersection(clique) - set(seen)
            seen.extend(neighbours)
            distances.extend([distances[current]+1] * len(neighbours))
            current += 1

        return zip(distances, seen)




def bc_enum(product_graph):
    for root in roots(product_graph):
        spawn(root)

def spawn(bc_clique):
    for solution in children(bc_clique):
        spawn(solution)
    return bc_clique

def black_edge_distance(bc_clique, node_idx):
    # Distance in the induced subgraph G_b[K] between node_idx and the head of K.
    # If node_idx not in K, but K + {node_idx} is a BC_clique, the distance is
    # similarly defined on G_b[K + {node_idx}.
    return distance between node_idx in bc_clique and head of bc_clique


def complete(bc_clique):
    while A := {v in N(k): v has black neighbour in K} != 0
        bc_clique += add argmin_{x in A} (black_edge_distance(x), x)
    return bc_clique

def parent_index(bc_clique):
    return argmax_{v in bc_clique} {(black_edge_distance(v), v): complete(bc_clique_{<v}) != bc_clique}

def parent(bc_clique):
    v = parent_index(bc_clique)
    return complete(bc_clique_{<v})


def roots(product_graph):
    return {complete(v): v = min(complete({v}))}


def candidate(bc_clique):
    return union_{u in bc_clique} N_b(u)

def children(bc_clique):
    for v in candidate(bc_clique):
        bc_clique_v_prime = unique maximal BC-clique containing v in G_b[bc_clique intesection N(v) union {v}]
        for h in bc_clique_v_prime:
            bc_clique_v_doubleprime = prefix of bc_clique_v_prime with respect to h, truncated at v
            d = complete(bc_clique_v_doubleprime)
            if bc_clique == parent(d) and h == min(d) and v == parent_index(d):
                yield d