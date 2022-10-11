from src.inference.utils.graph_utils import compareNames

from src.inference.utils.graph_utils import GraphUtils as gu
from src.inference.utils.set_utils import SetUtils as su
from src.common.object_utils import ObjectUtils as ou

errors = {
    'treatment': 'Please specify the treatment variable(s).',
    'outcome': 'Please specify the outcome variable(s).',
    'treatmentAndOutcome': 'Please specify the treatment & outcome variables.',
    'IinR': '\'I\' must be a subset or equal to \'R\'.',
    'treatmentInI': '\'I\' cannot include treatment variable(s).',
    'outcomeInI': '\'I\' cannot include outcome variable(s).',
    'treatmentInR': '\'R\' cannot include treatment variable(s).',
    'outcomeInR': '\'R\' cannot include outcome variable(s).',
}


def comparePairs(a, b):
    return a['node'] == b['node'] and a['edge'] == b['edge']


def writeNodeNames(nodes):
    return ', '.join(nodes) if len(nodes) > 0 else 'emptyset'


class AdjustmentSetUtils():

    # caution: implicitly assumes all latent nodes are explicit
    @staticmethod
    def TestSep(G, X, Y, Z=[]):
        X = ou.makeArray(X)
        Y = ou.makeArray(Y)
        Z = ou.makeArray(Z)

        # Bayes Ball
        # https://github.com/lingxuez/bayes-net/blob/9ba18d08f85d04b566c6a103be67242eab8dc95a/src/BN.py#L114
        obsAnc = AdjustmentSetUtils.getObservedAnc(G, Z)

        Q = []

        for x in X:
            Q.append((x['name'], 'up'))

        visited = set()

        while len(Q) > 0:
            (name, dir) = Q.pop()
            node = gu.getNodeByName(name, G)

            if (name, dir) not in visited:
                visited.add((name, dir))

                if not su.belongs(node, Z, compareNames) and su.belongs(node, Y, compareNames):
                    return False

                if dir == 'up' and not su.belongs(node, Z, compareNames):
                    for parent in G.parents(node):
                        Q.append((parent['name'], 'up'))

                    for child in G.children(node):
                        Q.append((child['name'], 'down'))

                elif dir == 'down':
                    if not su.belongs(node, Z, compareNames):
                        for child in G.children(node):
                            Q.append((child['name'], 'down'))

                    if su.belongs(node, Z, compareNames) or su.belongs(node, obsAnc, compareNames):
                        for parent in G.parents(node):
                            Q.append((parent['name'], 'up'))

        return True

    @staticmethod
    def getObservedAnc(G, Z):
        ancObserved = dict()

        for z in Z:
            An = gu.ancestors(z, G)

            for node in An:
                ancObserved[node['name']] = True

        nodeNames = []

        for name in ancObserved:
            nodeNames.append(name)

        return gu.getNodesByName(nodeNames, G)

    @staticmethod
    def FindSep(G, X, Y, I=[], R=[]):
        if not G or not X or not Y:
            return None

        X = ou.makeArray(X)
        Y = ou.makeArray(Y)

        if len(X) == 0 or len(Y) == 0:
            return []

        # check if I or R includes X or Y
        if len(su.intersection(I, X, 'name')) > 0:
            return None
        if len(su.intersection(I, Y, 'name')) > 0:
            return None
        if len(su.intersection(R, X, 'name')) > 0:
            return None
        if len(su.intersection(R, Y, 'name')) > 0:
            return None

        # check if I is in R
        if not (su.isSubset(I, R, 'name') or su.equals(I, R, 'name')):
            return None

        XY = su.union(X, Y, 'name')
        XYI = su.union(XY, I, 'name')
        AnXYI = gu.ancestors(XYI, G)
        Rprime = su.difference(R, XY, 'name')
        Z = su.intersection(AnXYI, Rprime, 'name')

        if AdjustmentSetUtils.TestSep(G, X, Y, Z) == True:
            return Z
        else:
            return None
