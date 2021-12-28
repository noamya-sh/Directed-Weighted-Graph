# Directed Weighted Graph - Ex3
#### Noamya Shani and Eitan Shenkolevski

### Abstract
Our project is building weighted directed graphs, executing algorithms on them and presenting them graphically (GUI).<br>
We have created 2 central classes that implement 2 interfaces - 
1. `DiGraph` implement `GraphInterface`.
2. `GraphAlgo ` implement `GraphInterfaceAlgo`.<br>

The `Node` class representing a vertex in the graph, the `gui` class and `menu` file (contain `Button`,`MenuItem`,`SubMenuItem` and `MenuBar` classes) for GUI.
To create the GUI we used the `pygame`, `tkinter` and `Numpy` packages.<br><br>
*UML of the project:*<br>
![image](https://user-images.githubusercontent.com/77248387/147591151-5ce94660-1131-4fac-8523-c5367bf5eda1.png)
There are also classes tests in the `test` folder.

### Run GUI




To run the GUI, open `cmd` in directory of [Ex3.py](https://github.com/noamya-sh/Ex3/blob/master/src/Ex3.py) and run the command:<br>
```
python Ex3.py <json file path>
```

Alternatively, create a `GraphAlgo` object, use the `load_from_json` function and then the `plot_graph` command. You can also load another graph and save it.

https://user-images.githubusercontent.com/77248387/147603233-8337d15f-0ca3-4e75-a2a4-3b64ecad7f28.mp4

By using Menu you can draw in the center point graph, and ask for the shortest path and solution to TSP.<br>
*Examples of windows that open when you press menu buttons:*<br>
![image](https://user-images.githubusercontent.com/77248387/147590823-77195a7e-e320-4bde-9cfe-8d42fce641e3.png)
![image](https://user-images.githubusercontent.com/77248387/147590795-8a5fe3ae-256f-4b61-aa6a-9c6329f386bc.png)

### Classes and functions
* `Node` class contain id of the node, position (x,y,z) and 2 dictionaries - for outgoing edges and for inbound edges.
* `DiGraph` class contains functions for adding and deleting nodes and adding and deleting edges,
as well as information about number of edges and nodes in the graph.
We implemented the directed graph using 2 dictionaries - one for the edges and one for the nodes.
If we need to delete a node we know exactly which edges we will need to delete along with it, using the dictionaries inside the node. With each addition of node we add it to the dict of nodes, and with each addition of edge we add it to the dict of edges,
to the dict of outgoing edges of the source node and to the dict of incoming edges of the destination node.<br>
* `GraphAlgo` class contain a graph and runs algorithms on it. The algorithms are - finding the shortest path between 2 nodes, finding the center node of graph and 
finding 'tsp' - a shortest path that get through a list of nodes given as an argument. In the implementation of the 'GraphAlgo' we used the dijkstra's algorithm in all kinds of variations.
We also implemented functions for loading a graph from a json file and saving a graph to a json file.
* `gui` class is platform to plot the graph. the class contain functions to draw graph, path of specific nodes and center point. In addition We have added computational functions - scaling of points and normalization of vectors (for drawing an arrow)
* `menu.py` contain some classes - `Button`,`MenuItem`,`SubMenuItem` and `MenuBar`, for draw menu on pygame screen. If a button is clicked in the menu, a function defined in `gui` class is performed.

### Performances
Comparison between this project (Python) and a previous project (Java):
| size graph | center_point | shortest_path|
| :-: | :-: | :-: |
| 1000 Nodes | *Python:* 8.3 sec  <-> *Java:* 8.5 sec | *Python:* 31 ms  <-> *Java:* 8.5 sec|
| 10000 Nodes | *Python:* 22 min 15 sec  <-> *Java:* 9 min 21 sec |*Python:* 385 ms  <-> *Java:* 156 ms |
| 1000000 Nodes |*Python:* timeout  <-> *Java:* timeout |*Python:* 8 sec 794 ms <-> *Java:* 1 min 33 sec |
<br>

*Computer info on which the projects were tested:*
windows 64 bit
Intel (R) Core (TM) i5-1035G1 CPU @
1.00GHz 1.19 GHz
RAM 8.00 GB
