# Directed Weighted Graph - Ex3
### Noamya Shani and Eitan Shenkolevski

#### Abstract
Our project is about building weighted directed graphs, executing algorithms on them and presenting them graphically (GUI).<br>
We have created 2 central classes that implement 2 interfaces - 
1. `DiGraph` implement `GraphInterface`.
2. `GraphAlgo ` implement `GraphInterfaceAlgo`.<br>

The `Node` class representing a vertex in the graph, the `gui` class and `menu` file (contain `Button`,`MenuItem`,`SubMenuItem` and `MenuBar` classes) for GUI.
To create the GUI we used the `pygame`, `tkinter` and `Numpy` packages.

#### Run GUI

To run the GUI, open `cmd` in directory of Ex3.py and run the command:<br>
```
python Ex3.py <json file path>
```
Alternatively, create a `GraphAlgo` object, use the `load_from_json` function and then the `plot_graph` command.
#### Classes and functions
The `DiGraph` class contains functions for adding and deleting nodes and adding and deleting edges,
as well as information about number of edges and nodes in the graph.
We implemented the directed graph using 2 dictionaries - one for the edges and one for the nodes,
where each `Node` object also contains 2 'dictionaries' - one for the edges that come out of it and the other for the edges that go into it.
So if we need to delete node we know exactly which edges We'll have to delete along with it. With each addition of node we add it to the dict of nodes,
and with each addition of edge we add it to the dict of edges, to the dict of outgoing edges of the source node and to the dict of incoming edges of the destination node.<br><br>


