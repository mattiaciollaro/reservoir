#! /usr/bin/env python3
import numpy as np


#
# Utilities to check user input
#
def _check_int(n, name):
    if not isinstance(n, int):
        raise TypeError("%s must be an integer" % name)


def _check_positive_int(n, name):
    if n < 1:
        raise ValueError("%s must be strictly positive" % name)


def _check_iterable(itrbl, name):
    try:
        _ = (item for item in itrbl)  # noqa
    except TypeError:
        raise TypeError("%s needs to be an iterable" % name)


#
# Reservoir sampling implementation
#
class Reservoir(object):
    """
    Implementation of reservoir sampling.
    """
    def __init__(self, size):
        # check that size is an integer
        _check_int(size, "size")

        # check that size is positive
        _check_positive_int(size, "size")

        # store size as an attribute
        self._size = size

        # initialize an empty list for samples
        self._samples = []

        # number of elements seen
        self._seen = 0

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        _check_int(value, "size")
        _check_positive_int(value, "size")
        self._size = value

    @property
    def samples(self):
        # read only!
        return self._samples

    @property
    def seen(self):
        # read only!
        return self._seen

    def sample(self, gen, seed=None):
        """
        Main method implementing reservoir sampling.
        """
        # checks
        _check_iterable(gen, "gen")

        # if a seed is passed by the user, set it
        if seed is not None:
            _check_int(seed, "seed")
            np.random.seed(seed)

        # stream
        for item in gen:
            # increment counter of seen elements
            self._seen += 1

            # while the length of the stream is less
            # then the number of samples requested,
            # simply store data as they come
            if self._seen <= self.size:
                self.samples.append(item)
            else:
                # probability of acceptance
                p = float(self.size / self._seen)

                # keep or discard
                keep = np.random.uniform(size=1) <= p

                if keep:
                    swap_index = int(np.random.choice(self.size))
                    self._samples[swap_index] = item

    def reset(self):
        """
        Reset the reservoir.
        Note that the size attribute is *not* reset!
        """
        self._seen = 0
        self._samples = []


#
# Try it out! (plus minimal testing)
#
if __name__ == "__main__":

    print("\nInitializing a reservoir of size 10...")
    reservoir = Reservoir(size=10)

    print("\nA stream is coming!")
    stream_one = (n for n in range(10000))

    print("\nSampling 10 items from the first stream...")
    reservoir.sample(stream_one, seed=0)
    _samples_one = {str(s) for s in reservoir.samples}

    print("\nSo far, we have seen %d items!" % reservoir.seen)
    print("\nThese are the items in the current sample:")
    print(reservoir.samples)

    print("\nWhoa! Another stream is coming!")
    stream_two = (n for n in range(10000, 15000))

    print("\nKeep on sampling!")
    reservoir.sample(stream_two)
    _samples_two = {str(s) for s in reservoir.samples}

    print("\nNow the sampled items are:")
    print(reservoir.samples)

    print("\nThese items survived in the sample after the second stream:")
    print([int(s) for s in (set(_samples_one) & set(_samples_two))])

    print("\nAt this point, we have seen %d items in total!" % reservoir.seen)

    print("\nTime to reset the reservoir...")
    reservoir.reset()

    print("\nThe sample is now:")
    print(reservoir.samples)

    print("\nThe number of seen items is now %d." % reservoir.seen)

    print("\nBut the size attribute is still %d.\n\n\n" % reservoir.size)

    # Try to break stuff
    print("===== size smaller than one test =====")
    try:
        reservoir.size = -10
        print("This test didn't pass")
    except ValueError:
        print("Caught size smaller than 1!")

    print("===== size not integer test =====")
    try:
        reservoir.size = 1.45
        print("This test didn't pass")
    except TypeError:
        print("Caught size non integer!")

    print("===== setting samples test =====")
    try:
        reservoir.samples = [1, 2, 3]
        print("This test didn't pass")
    except AttributeError:
        print("Caught trying to set samples!")

    print("===== setting seen test =====")
    try:
        reservoir.seen = 100
        print("This test didn't pass")
    except AttributeError:
        print("Caught trying to set size!")

    print("===== passing a non iterable test =====")
    try:
        reservoir.sample(gen=int)
        print("This test didn't pass")
    except TypeError:
        print("Caught trying to pass a non iterable stream!")
