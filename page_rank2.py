import argparse
import random
import sys
import time
import networkx as nx

def load_graph(args):
    """Load graph from text file"""
    # Load graph from DiGraph
    graph = nx.DiGraph()
    # Read the graph structure line by line from the data file
    for line in args.datafile:
        line = line.strip()
        if line:
            node, target = line.split(' ', 1)
            graph.add_edge(node, target)
    return graph

def print_stats(graph):

    """Print number of nodes and edges in the given graph"""
    # Load number of nodes and number of edges
    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()
    print(f"Graph contains {nodes} nodes and {edges} edges")

def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation"""

    nodes = list(graph.nodes)
    hits = {node: 0 for node in nodes}
    # This initializes hit counts for all nodes. Clear and efficient for this purpose
    for _ in range(args.repeats):
        # Starting at a random node is standard for random walks
        current = random.choice(nodes)
        for _ in range(args.steps):
            hits[current] += 1
            targets = list(graph.successors(current))
            if targets:
                current = random.choice(targets)
            else:
                current = random.choice(nodes)
    return hits

def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation"""
    return nx.pagerank(graph, max_iter=args.steps)
   # Delegating to NetworkX's built-in method is efficient and reliable.
parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic', help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank
    graph = load_graph(args)
    print_stats(graph)
    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    elapsed_time = stop - start
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k, v in top[:args.number]))
    sys.stderr.write(f"Calculation took {elapsed_time:.2f} seconds.\n")



