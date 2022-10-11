import copy
import itertools


class ObjectUtils():

    @staticmethod
    def clone(a, deep=True):
        return copy.deepcopy(a) if deep else copy.copy(a)

    # symmetric if true, symmetric pairs will be outputted (e.g., X,Y and Y,X). defaults to false.
    @staticmethod
    def pairs(array, symmetric=False):
        if symmetric:
            return list(itertools.permutations(array, 2))
        else:
            return list(itertools.combinations(array, 2))

    @staticmethod
    def makeArray(elements):
        if not isinstance(elements, list):
            elements = [elements]

        return elements
