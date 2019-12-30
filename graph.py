import numpy as np


class Graph(object):
    '''
    Represents pheromone weights across bin-item matrix

    :attr graph: 3D array of pheromone weights
    :attr e: Pheromone evaporation rate

    :method evaporate():
    '''

    def __init__(self, b, i, e):
        self.graph = np.random.rand(b, i, b)
        self.e = e

    def __repr__(self):
        return "Graph: " + str(self.graph)

    def evaporate(self):
        '''
        Reduce pheromone weights across the graph
        :return: None
        '''

        self.graph = self.graph * self.e


if __name__ == "__main__":
    print("Generating graph [10 bins, 200 items, 0.9 evap. rate]")
    g = Graph(10, 200, 0.9)
    print(g)
