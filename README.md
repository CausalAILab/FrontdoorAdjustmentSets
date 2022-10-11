# Finding and Listing Front-door Adjustment Sets

This repository contains the code for the paper "Finding and Listing Front-door Adjustment Sets" by Hyunchai Jeong, Jin Tian, and Elias Bareinboim.

## How to install

Please run the following commands to install the package:

```
git clone https://github.com/jeong10/frontdoor_adjustment_sets.git
cd frontdoor_adjustment_sets
pip install -r requirements.txt
pip install -e .
```

## How to run

To run some examples, try running the following commands:

```
python3 main.py find graphs/fig1a.txt
```

```
python3 main.py list graphs/fig1b.txt
```

1. First argument: `find` or `list`. `find` is used for finding any valid front-door adjustment set. Specify `list` for enumerating all valid front-door adjustment sets.
2. Second argument: `graphs/fig1a.txt`. the path to a file that contains all necessary information, such as graph, query, and constraints (i.e., `I` and `R`). Please check the formatting for details.

## Formatting of the input file

Consider `graphs/fig1b.txt` as an example.

*&#60;NODES&#62;*

Each line represents the name of a variable/node (e.g., `X` and `A`).

*&#60;EDGES&#62;*

Each line describes an edge. Two types of edges are supported:

1. Directed edge: `X -> A` represents a directed edge from `X` to `A`.
2. Bidirected edge: `X -- Y` means there exists some unmeasured confounder (i.e., latent variable) between `X` and `Y`.

*&#60;TASK&#62;*

The task represents the query of interest. The lines:

```
treatment: X
outcome: Y
```

specifies a casual effect from `X` to `Y`. Multiple nodes may be specified by separating each name of a node with comma (e.g., `treatment: A, B, C`).

*&#60;CONSTRAINTS&#62;*

The lines:

```
I: B
R: A,B,C,D
```

represent the constraints as follows:
1. `I` specifies a set of nodes that *must* be in any candidate front-door adjustment set. If `I` is not specifed (i.e., by removing the line `I: B`), then `I` will be an empty set by default.
2. `R` specifies a set of nodes that *could* be in any candidate front-door adjustment set. If `R` is not specifed (i.e., by removing the line `R: A,B,C,D`), then every node but treatment and outcome nodes will be included by default.