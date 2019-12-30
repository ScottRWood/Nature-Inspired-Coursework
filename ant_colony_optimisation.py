from random import random
from time import time
from itertools import repeat
from matplotlib import pyplot as plt

from graph import Graph
from ant import Ant


class AntColonyOpt(object):
    '''
    All relevant info for objects required for running ACO

    :attr bins: bin object holding items and total weight
    :attr items: list of item weights
    :attr ants: list of ant objects to be controlled
    :attr b_ant: best ant of final gen of a run
    :attr graph: graph to store pheromone weights
    :attr num_paths: number of routes evaluated
    :attr limit: generation limit
    :attr verbose: whether or not to print to console when log called
    :attr ran: has the ACO been run
    :attr runtime: duration of last run
    :attr avg_fitnesses: timeseries of averages fitnesses over each cycle

    :method summary():
    :method stats():
    :method run():
    :method explore():
    :method ant_run(a):
    :method create_route(a):
    :method route_step(p_bin, i):
    :method route_fitness():
    :method set_best():
    :method empty_bins():
    :method log(message):
    :method graph_averages():
    '''

    def __init__(self, b, i, p, e, limit=10000, verbose=False):

        self.bins = b
        self.items = i

        self.p = p
        self.e = e

        self.ants = [Ant() for _ in range(p)]
        self.b_ant = None

        self.graph = Graph(len(b), len(i), e)

        self.num_paths = 0
        self.limit = limit
        self.verbose = verbose

        self.ran = False
        self.runtime = 0

        self.avg_fitnesses = []

    def summary(self):
        '''
        Give summary data on the run
        :return: None
        '''

        if hasattr(self, 'ran') and self.ran:
            print("Run Successful")
            print("Runtime: %d seconds" % int(self.runtime))
            print("Best Fitness: %d" % self.b_ant.fitness)
            print("Best Configuration: ")
            for i, b in enumerate(self.b_ant.bins):
                print("%4d. %s" % (i + 1, b))

    def stats(self):
        '''
        Give stats about the run
        :return: best fitness of run and runtime
        '''

        if hasattr(self, 'ran') and self.ran:
            return self.b_ant.fitness, self.runtime

    def run(self):
        '''
        Run the ACO
        :return: None
        '''

        self.log("Starting Run")
        self.ran = False
        self.b_fitnesses = []
        self.avg_fitnesses = []
        start = time()

        while self.num_paths < self.limit:
            self.explore()

        self.set_best()
        self.ran = True
        self.runtime = time() - start

    def explore(self):
        '''
        Run a cycle of route creation and evaporation
        :return: None
        '''

        self.ants = [*map(self.ant_run, self.ants)]
        best = None

        for a in self.ants:
            a.lay_pheromones(self.graph)

        fitnesses = [a.fitness for a in self.ants]
        self.b_fitnesses.append(min(fitnesses) / sum(self.items))
        self.avg_fitnesses.append(sum(fitnesses) / len(fitnesses))
        self.graph.evaporate()

    def ant_run(self, a):
        '''
        Reset and recreate route of ant
        :param a: Ant to recreate route of
        :return: Ant with new route
        '''
        self.empty_bins()
        a = self.create_route(a)
        a.bins = self.bins.copy()
        return a

    def create_route(self, a):
        '''
        Create route through graph
        :param a: Ant to travel the route
        :return: Ant
        '''

        p_bin = 0
        a.route = []

        for i in enumerate(self.items):
            p_bin, i = self.route_step(p_bin, i)
            a.route.append((p_bin, i))

        a.fitness = self.route_fitness()
        self.num_paths += 1

        return a

    def route_step(self, p_bin, i):
        '''
        Step from current bin to next bin solution
        :param p_bin: The previous bin
        :param i: The item
        :return: The next bin
        '''

        col = self.graph.graph[p_bin][i[0]].tolist()
        total = sum(col)
        threshold = total * random()

        cur = 0.0

        for ind, w in enumerate(col):
            if cur + w >= threshold:
                self.bins[ind].add(i[1])
                return ind, i[0]

            cur += w

    def route_fitness(self):
        '''
        Calculate fitness of the route
        :return: The fitness value
        '''

        max_w = self.bins[0].total_weight
        min_w = self.bins[0].total_weight

        for b in self.bins:
            if b.total_weight > max_w:
                max_w = b.total_weight
            if b.total_weight < min_w:
                min_w = b.total_weight

        return max_w - min_w

    def set_best(self):
        '''
        Set best ant of generation
        :return: The best ant
        '''

        for a in self.ants:
            if self.b_ant and a.fitness < self.b_ant.fitness:
                self.b_ant = a.copy()
            elif not self.b_ant:
                self.b_ant = a.copy()

    def empty_bins(self):
        '''
        Empty the bins
        :return: List of emptied bins
        '''

        [b.empty() for b in self.bins]

    def log(self, message):
        '''
        Print a message if running in verbose mode
        :param message: Message to be printed
        :return: None
        '''

        if self.verbose:
            print(message)

    def graph_averages(self):
        '''
        Graph the averages of each generation
        :return: None
        '''

        plt.title("Pop: %d; ER: %2f" % (self.p, self.e))
        plt.plot(self.avg_fitnesses)
        plt.show()


if __name__ == "__main__":
    from bin import gen_bins
    from item import gen_items

    b = gen_bins(10)
    i = gen_items(n=200)
    p = 10
    e = 0.4

    t = AntColonyOpt(b, i, p, e, verbose=True)
    t.run()
    t.graph_averages()
