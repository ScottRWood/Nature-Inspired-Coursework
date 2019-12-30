class Bin(object):
    '''
    Represents a bin that can hold items

    :attr total_weight: sum of items in the bin
    :attr items: item weights currently in bin

    :method add:
    :method copy:
    :method empty:
    '''


    total_weight = 0
    items = []

    def __repr__(self):
        return "Item Count: %d ; Weight: %d ; Items: %s" \
                % (len(self.items), self.total_weight, self.items)

    def add(self, item):
        '''
        Add item to bin
        :param item:  item to be added
        :return: None
        '''

        self.items.append(item)
        self.total_weight += item

    def copy(self):
        '''
        Creates a copy of the bin
        :return: copy of bin
        '''

        n_bin = Bin()
        n_bin.total_weight = self.total_weight
        n_bin.items = [i for i in self.items]
        return n_bin

    def empty(self):
        '''
        Resets contents of bin
        :return:  None
        '''

        self.items = []
        self.total_weight = 0


def gen_bins(n):
    '''
    Creates number of bins given
    :param n: number of bins to create
    :return: list of generated bins
    '''

    return [Bin() for _ in range(n)]


if __name__ == "__main__":
    print("Generating 10 bins")
    b = gen_bins(10)
    print(b)
    print(len(b))