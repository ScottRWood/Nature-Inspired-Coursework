class Ant(object):
    '''
    Class representing an ant

    :attr route: list of co-ordinates that represent the bin-item config
    :attr fitness: current fitness of the ant's route
    :attr bins: the bin config if the ant is the best in a generation

    :method lay_pheromones(graph):
    :method copy():
    :method get_route_str():
    '''

    route = []
    fitness = -1
    bins = []

    def lay_pheromones(self, graph):
        '''
        Distribute a pheremone weight on the graph at positions defined in route
        :param graph: Construction graph of the problem
        :return: None
        '''

        weight = 100.0 / self.fitness
        previous_bin = 0

        for bin, item in self.route:
            graph.graph[previous_bin, item, bin] += weight
            previous_bin = bin

    def copy(self):
        '''
        Creates a copy of the ant
        :return: copy of ant
        '''

        n_ant = Ant()
        n_ant.route = [r for r in self.route]
        n_ant.bins = self.bins.copy()
        n_ant.fitness = self.fitness
        return n_ant

    def get_route_str(self):
        '''
        Give a string representing the ant's route
        :return: String representing the ant's route
        '''

        return " -> ".join("Item %d in Bin %d" % (point[1] + 1, point[0]) for point in self.route)
