import argparse
import random
import sys
import time
from collections import defaultdict
from progress import Progress

def load_graph(args):
    """Load graph from text file
    Parameters:
    args -- arguments named tuple
    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    # Load the graph as a dictionary
    graph = defaultdict(list)
    # Read the graph structure line by line from the data file
    for line in args.datafile:
        line = line.strip()
        if line:
            node, target = line.split(' ', 1)

            if node in graph:
                graph[node].append(target) # Add the target to the existing list
            else:
                graph[node] = [target] # Create a new entry to the target list
    return graph

def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    # Initialize number of nodes and edges
    num_nodes = len(graph)
    # Calculate number of edges by summing the length of the target
    num_edges = sum(len(targets) for  targets in graph.values())
    print(f"Graph contains {num_nodes} nodes and {num_edges} edges")


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation
    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple
    Returns:
    A dict that assigns each page its hit frequency
    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """

    pages = list(graph.keys()) # Get list of all nodes (pages)
    hits = defaultdict(int) # Initialize visit counts for each node
    num_repeats = args.repeats # Number of random walks to perform

    for node in range(num_repeats):
        current = random.choice(pages)  # Start from a random page.

        hits[current] += 1
        if graph[current]:  # If the page has outgoing links, choose one.
            current = random.choice(graph[current])
        else:  # Dead-end, teleport to a random page.
            current = random.choice(pages)

    # Normalize the hits into probabilities.

    return hits

def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation
    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple
    Returns:
    A dict that assigns each page its probability to be reached
    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    num_nodes = len(graph) # Number of nodes in the graph
    num_steps = args.steps# Number of iterations to perform
    # Initialize the probability distribution for each node
    node_prob = {}
    for node in graph:
        node_prob[node] = 1 / num_nodes
    for node in range(num_steps): # Perform the specified number of iterations
        next_prob = {}
        for node in graph:
            # Initialize the next probability distribution
            next_prob[node] = 0
            # Distribute probabilities from each node to its targets
        for node, target in graph.items():
            if not target: # If the node is a dead-end (no outgoing links)
                # Redistribute equally to all nodes
                p = node_prob[node] / len(target)
                for i in target:
                    next_prob[i] += p
            else:
                # Redistribute equally to all nodes
                p = node_prob[node] / len(target)
                for i in target:
                    next_prob[i] += p
        # Update the current probability distribution
        node_prob = next_prob
    return node_prob


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'),default=sys.stdin,help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'),default='stochastic',help="selected page rank algorithm")
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
    time = stop - start
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")





