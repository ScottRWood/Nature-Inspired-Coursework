from operator import itemgetter
from time import time

from ant_colony_optimisation import AntColonyOpt
from bin import gen_bins
from item import gen_items


def run_tests(b=10, scale=False):
    '''
    Run all the tests
    :param b: Number of bins
    :param scale: Boolean determining the item generation
    :return: List of results
    '''

    res_list = []

    i = 500
    rules = [
        {'p': 100, 'e': 0.9},
        {'p': 100, 'e': 0.6},
        {'p': 10, 'e': 0.9},
        {'p': 10, 'e': 0.6},
    ]

    for r in rules:
        res = run_test(b, i, r['p'], r['e'], scale=scale, verbose=True)
        res_list.append(res)
        print("Test [B=%d, I=500, S=%s, P=%d, E=%.1f]" %
              (b, scale, r['p'], r['e'])
              )
        print("Average fit: %.1f; Average runtime: %.2f s" %
              (res['avg_fitness'], res['avg_runtime']))

    return res_list


def run_test(b_num, i_num, p, e, scale=False, verbose=False):
    '''
    Run a test
    :param b_num: Number of bins
    :param i_num: Number of items
    :param p: Population size
    :param e: Evaporation rate
    :param scale: Boolean determining the item generation
    :param verbose: Boolean determining whether to log all steps
    :return: Dictionary containing results of test
    '''

    res = []
    avg_fitness = 0
    avg_runtime = 0

    total_runtime = 0

    for i in range(5):
        b = gen_bins(b_num)
        i = gen_items(n=i_num, scale=scale)

        t = AntColonyOpt(b, i, p, e, verbose=False)
        t.run()
        t.graph_averages()

        fitness, runtime = t.stats()
        res.append((fitness, runtime))

        avg_fitness += fitness * 0.2
        avg_runtime += runtime * 0.2

        total_runtime += runtime

    log("Test Complete; Time: %d s" % total_runtime, verbose)
    log("Stats: ", verbose)
    log("Average Fitness: %f" % avg_fitness, verbose)
    log("Average Runtime: %f" % avg_runtime, verbose)

    return {
        "res" : res,
        "b_num" : b_num,
        "i_num" : i_num,
        "p" : p,
        "e" : e,
        "scale" : scale,
        "avg_fitness" : avg_fitness,
        "max_fitness" : max(res, key=itemgetter(0))[0],
        "min_fitness" : min(res, key=itemgetter(0))[0],
        "avg_runtime" : avg_runtime,
        "max_runtime" : max(res, key=itemgetter(1))[1],
        "min_runtime" : min(res, key= itemgetter(1))[1],
        "total_runtime" : total_runtime
    }


def show_results(res_list):
    '''
    Show results
    :param res_list: The list of results
    :return: None
    '''

    for i, res in enumerate(res_list):
        print("Results for run %s\n" % str(i+1))

        for j, test in enumerate(res):
            print("PARAMETERS")
            print("B=%d, I=%d, P=%d, E=%f, S=%s" %
                  (test['b_num'], test['i_num'], test['p'], test['e'], test['scale'])
                  )
            print("Fitness - AVG: %6.1f; MAX: %6s; MIN:%6s" %
                  (test['avg_fitness'], test['max_fitness'], test['min_fitness']))
            print("Time - AVG: %6.2f; MAX: %6.2f; MIN: %6.2f\n" %
                  (test['avg_runtime'], test['max_runtime'], test['min_runtime'])
                  )


def log(message, verbose=False):
    '''
    Print message if running in verbose mode
    :param message: Message to print
    :param verbose: Boolean indicating verbose mode
    :return: None
    '''

    if verbose:
        print(message)


if __name__ == "__main__":
    print("Starting")
    start = time()
    total_res = []
    print("Starting First run")
    total_res.append(run_tests())
    print("Finished First run")
    print("Starting Second run")
    total_res.append(run_tests(50, True))
    print("Finished Second run")

    print("Full test complete; Runtime: %.2f" % float(time() - start))
    print("Results\n")
    show_results(total_res)
