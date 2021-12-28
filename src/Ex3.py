import sys
from GraphAlgo import *


def Ex3() -> None:
    """Function for run GUI from cmd."""
    arg = sys.argv
    g = GraphAlgo()
    g.load_from_json(arg[1])
    g.plot_graph()


if __name__ == '__main__':
    Ex3()
