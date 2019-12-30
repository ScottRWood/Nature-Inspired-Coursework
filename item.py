def gen_items(lower=1, upper=200, n=200, scale=False, test=False):
    '''
    Creates array of int weights
    :param n: number of items to be generated
    :param scale: boolean to decide how to generate items
    :param test: boolean to decide how to generate items
    :return: list of items
    '''

    if not (scale or test):
        return [i for i in range(1, n+1)]

    if scale:
        return [int((i**2) / 2) for i in range(1, n+1)]

    return [1 for _ in range(n)]


if __name__ == "__main__":
    print("Generating items [DEFAULT]")
    i = gen_items()
    print(i)
    print(len(i))

    print("Generating items [SCALE]")
    i = gen_items(scale=True)
    print(i)
    print(len(i))

    print("Generating items [TEST]")
    i = gen_items(test=True)
    print(i)
    print(len(i))