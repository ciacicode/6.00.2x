# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

import pdb

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    def __init__(self, src, dest, tot, outd):
        Edge.__init__(self, src, dest)
        self.tot = tot
        self.outd = outd

    def getTotalDistance(self):
        return self.tot

    def getOutdoorDistance(self):
        return self.outd

    def __str__(self):
        return self.getSource().name + '->' + self.getDestination().name + ' (' + str(self.tot) + ', ' + str(self.outd) + ')'

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedDigraph(Digraph):
    def __init__(self):
        Digraph.__init__(self)

    def addEdge(self, edge):
        edge_info = list()
        src = edge.getSource()
        dest = edge.getDestination()
        tot = edge.getTotalDistance()
        outd = edge.getOutdoorDistance()
        distance = (tot, outd)
        edge_info.append(dest)
        edge_info.append(distance)
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(edge_info)

    def childrenOf(self, node):
        children = list()
        for child in self.edges[node]:
            children.append(child[0].name)
        return children

    def __str__(self):
        #a->b (15.0, 10.0)
        #a->c (14.0, 6.0)
        #b->c (3.0, 1.0)
        res = ''
        for key in self.edges.keys():
            for value in self.edges[key]:
                edge = ''
                destination = value[0].name
                raw_tuple = value[1]
                tot = float(raw_tuple[0])
                outd = float(raw_tuple[1])
                formatted_tuple = (tot, outd)
                edge += str(key) + '->' + destination + ' ' + str(formatted_tuple) + '\n'
                res += edge
        return res



def test_weighted_digraph():
    nj = Node('j')
    nk = Node('k')
    nm = Node('m')
    ng = Node('g')
    g = WeightedDigraph()
    g.addNode(nj)
    g.addNode(nk)
    g.addNode(nm)
    g.addNode(ng)
    g.addEdge(WeightedEdge(nk, nj, 10, 12))
    g.addEdge(WeightedEdge(nk, nm, 30, 2))
    g.addEdge(WeightedEdge(nm, ng, 34, 45))

    print g