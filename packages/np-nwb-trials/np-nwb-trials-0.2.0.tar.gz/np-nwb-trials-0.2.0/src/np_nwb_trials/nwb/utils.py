import numpy as np
from collections import Iterable


def dict_to_indexed_array(dc, order=None):
    """Given a dictionary and an ordered arr, build a concatenation of the dictionary's values and an index describing
    how that concatenation can be unpacked

    Notes
    -----
    - Polyfil from allensdk
    """

    if order is None:
        order = dc.keys()

    data = []
    index = []
    counter = 0

    for key in order:
        if isinstance(dc[key], (np.ndarray, list)):
            extended = dc[key]
        if isinstance(dc[key], Iterable):
            extended = [x for x in dc[key]]
        else:
            extended = [dc[key]]

        counter += len(extended)
        index.append(counter)
        data.append(extended)

    data = np.concatenate(data)
    return index, data
