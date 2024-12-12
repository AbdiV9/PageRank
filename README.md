# README 
## Purpose of the program
The purpose of this program is to represent graphs in various ways using urls as nodes and 
## How it works 
python page_rank.py school_web2024-1.txt -m stochastic.

- This will calculate the number edges and nodes in the graph and calculate the urls that are connected to target link
by using graphs.

 python page_rank.py school_web2024-1.txt -m distribution -s 100.

- This will calculate the probability of each link being connected to each other by a random walker 

# Optimization  Report

## Structural improvements
I will explain how I optimised the code to increase the speed and reduce time taken to do the pagerank function. The 
documentation was improved for readability. Examples of this are the comments were used to better describe the 
functionality and intent of the code.Across all functions there was consistent docstring formatting was applied to 
standard conventions. Consistent naming of variables improves readability and understanding such as target was used 
uniformly instead of varying terms, and node_prob was clearly labelled to reflect its purpose as a probability 
distribution. 
----------------------
## Performance enhancements 
Efficient use of data structures. The use of default dict was obtained but optimised in certain areas to prevent redundant 
operations. For example conditional logic load_graph was streamlined to prevent redundant checking for node existence 
explicitly before appending target. How I optimised stochastic page_rank.py. The random walk implementation was enhanced by
reducing operations that were going to be redundant. Instead of recalculating random.choice(pages) at each teleportation, 
precomputed values were used when feasible. How I optimised distribution page_rank.py. I reduced the redundancy in the 
computation by directly normalizing and updating probabilities. Ensured that nodes don't have outgoing links. So they can 
distribute their probabilities more efficiently by broadcasting uniformly to all nodes in a single step.
-----------------------
## Error handling
Dead-end nodes were handled robustly as the code was changed to ensure that there was more constant redistribution of 
probabilities even if the target list was empty. The utility functions were introduced for repetitive tasks. The algorithm 
section logic in the main function was simplified. 
-----------------------
## Improved Output
The output was reformatted to be more user-friendly. The top ranked pages are now displayed with clear percentages ranks 
and neat alignment, making it easier to interpret results. Execution time has a higher precisions, helping users understand
the scripts performance. 
-----------------------
## Speed reduction
Redirecting walkers from dead-end nodes to random nodes adds overhead, especially if the graph contains many such nodes.

## Conclusion
The optimized script is now more efficient, easier to read and also faster to run. These changes improve the usability
without risking the functionality. Future improvements that could be made to optimize the code even more is parallel 
processing for faster computations and support weighted graphs.

