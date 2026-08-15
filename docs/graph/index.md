# Module `mnemosine.graph`

## Overview

Graph traversal over node_links using recursive CTEs and BFS.

The links between nodes form an undirected graph (each link connects two
nodes; direction is a property of the link, traversal can go either way).
This module provides neighbor lookup, breadth-first subgraph expansion via a
`WITH RECURSIVE` query, and shortest-path search.

## Functions

- [_as_id](_as_id.md)

## Class Graph

- [Graph](Graph.md)
  - [Graph.__init__](Graph.__init__.md)
  - [Graph.neighbors](Graph.neighbors.md)
  - [Graph.subgraph](Graph.subgraph.md)
  - [Graph.reachable](Graph.reachable.md)
  - [Graph.path](Graph.path.md)
  - [Graph._neighbor_ids](Graph._neighbor_ids.md)
