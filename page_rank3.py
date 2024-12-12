import sys
import time
import argparse
import numpy as np


def load_graph(args):
    """Load graph as a transition probability matrix."""
    url_to_index = {}
    edges = []

    # Read the file and collect edges
    for line in args.datafile:
        src, dest = line.strip().split()
        if src not in url_to_index:
            url_to_index[src] = len(url_to_index)
        if dest not in url_to_index:
            url_to_index[dest] = len(url_to_index)
        edges.append((url_to_index[src], url_to_index[dest]))

    # Create adjacency matrix
    n = len(url_to_index)
    adjacency_matrix = np.zeros((n, n), dtype=float)
    for src, dest in edges:
        adjacency_matrix[src, dest] = 1.0

    # Normalize rows to create transition probability matrix
    row_sums = adjacency_matrix.sum(axis=1, keepdims=True)
    transition_matrix = np.divide(adjacency_matrix, row_sums,
                                  out=np.zeros_like(adjacency_matrix), where=row_sums != 0)

    return transition_matrix, url_to_index


def print_stats(graph):
    """Print number of nodes and edges in the given graph."""
    transition_matrix, url_to_index = graph
    num_nodes = transition_matrix.shape[0]
    num_edges = int(transition_matrix.sum())  # Sum of all entries equals number of edges
    print(f"Graph has {num_nodes} nodes and {num_edges} edges.")


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation."""
    transition_matrix, url_to_index = graph
    n = transition_matrix.shape[0]
    hit_counts = np.zeros(n, dtype=int)

    for _ in range(args.repeats):
        current_node = np.random.randint(n)  # Start at a random node
        for _ in range(args.steps):
            next_node = np.random.choice(n, p=transition_matrix[current_node])
            current_node = next_node
        hit_counts[current_node] += 1

    # Normalize hit counts to obtain frequencies
    hit_frequencies = hit_counts / args.repeats
    return {url: hit_frequencies[idx] for url, idx in url_to_index.items()}


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation."""
    transition_matrix, url_to_index = graph
    n = transition_matrix.shape[0]
    damping_factor = 0.85
    ranks = np.ones(n) / n  # Start with uniform ranks

    for _ in range(args.steps):
        ranks = (1 - damping_factor) / n + damping_factor * np.dot(ranks, transition_matrix)

    return {url: ranks[idx] for url, idx in url_to_index.items()}


# Argument parser setup
parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="Selected PageRank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000,
                    help="Number of repetitions for stochastic PageRank")
parser.add_argument('-s', '--steps', type=int, default=100,
                    help="Number of steps a walker takes or iterations for distribution PageRank")
parser.add_argument('-n', '--number', type=int, default=20,
                    help="Number of results to show")

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank
    graph = load_graph(args)
    print_stats(graph)
    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    elapsed = stop - start
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100 * v:.2f}\t{k}' for k, v in top[:args.number]))
    sys.stderr.write(f"Calculation took {elapsed:.2f} seconds.\n")
