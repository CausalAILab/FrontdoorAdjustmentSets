import sys

from src.inference.utils.set_utils import SetUtils as su
from src.inference.utils.graph_utils import GraphUtils as gu
from src.adjustment.classes.constraints_section import ConstraintsSection
from src.editor.sections.experiments_section import ExperimentsSection
from src.editor.sections.populations_section import PopulationsSection
from src.editor.sections.task_section import TaskSection
from src.editor.sections.edges_section import EdgesSection
from src.editor.sections.nodes_section import NodesSection
from src.editor.classes.bidirected_options_parser import BidirectedOptionsParser
from src.editor.classes.latent_options_parser import LatentOptionsParser
from src.editor.input_parser import InputParser
from src.adjustment.frontdoor_adjustment import FrontdoorAdjustment
from src.adjustment.adjustment_sets_utils import writeNodeNames
from src.adjustment.classes.constraints_task import constraintsIDefName, constraintsRDefName
from src.task.basic_task import treatmentDefName, outcomeDefName
from src.graph.classes.graph_defs import latentNodeType, bidirectedEdgeType


def FindFDSet(fileContent):
    parsedData = parseInput(fileContent)

    if parsedData is None:
        return

    G = parsedData['graph']
    T = parsedData['task']

    X = gu.getNodesByName(T.sets[treatmentDefName], G)
    Y = gu.getNodesByName(T.sets[outcomeDefName], G)

    if constraintsIDefName in T.sets:
        I = gu.getNodesByName(T.sets[constraintsIDefName], G)
    else:
        I = []

    if constraintsRDefName in T.sets:
        R = gu.getNodesByName(T.sets[constraintsRDefName], G)
    else:
        R = su.difference(G.nodes, su.union(X, Y, 'name'), 'name')

    Z = FrontdoorAdjustment.FindFDSet(G, X, Y, I, R)

    if Z is None:
        print('No admissible set exists.')
    else:
        Znames = list(map(lambda n: n['name'], Z))
        print('Admissible set: ' + writeNodeNames(Znames))


def ListFDSets(fileContent):
    parsedData = parseInput(fileContent)

    if parsedData is None:
        return

    G = parsedData['graph']
    T = parsedData['task']

    X = gu.getNodesByName(T.sets[treatmentDefName], G)
    Y = gu.getNodesByName(T.sets[outcomeDefName], G)

    if constraintsIDefName in T.sets:
        I = gu.getNodesByName(T.sets[constraintsIDefName], G)
    else:
        I = []

    if constraintsRDefName in T.sets:
        R = gu.getNodesByName(T.sets[constraintsRDefName], G)
    else:
        R = su.difference(G.nodes, su.union(X, Y, 'name'), 'name')

    result = FrontdoorAdjustment.ListFDSets(G, X, Y, I, R)

    if (len(result)) == 0:
        print('No admissible set.')
    else:
        print(str(len(result)) + ' admissible set' +
              ('s' if len(result) > 1 else '') + '.')


def parseInput(fileContent):
    parser = InputParser()
    parser.sections = [getNodesSection(), getEdgesSection(),
                       TaskSection(), PopulationsSection(), ExperimentsSection(), ConstraintsSection()]

    parsedData = parser.parse(fileContent)

    return parsedData


def getNodesSection():
    nodeTypeParsers = {}
    nodeTypeParsers[latentNodeType.id_] = LatentOptionsParser()

    return NodesSection(nodeTypeParsers)


def getEdgesSection():
    edgeTypeParsers = {}
    edgeTypeParsers[bidirectedEdgeType.id_] = BidirectedOptionsParser()

    return EdgesSection(edgeTypeParsers)


if __name__ == '__main__':

    # read arguments
    if len(sys.argv) != 3:
        print('Please specify 2 arguments: 1) the name of the task (e.g., \'find\' or \'list\'), and 2) input file path (e.g., graphs/canonical.txt).')

        sys.exit()

    task = sys.argv[1]
    filePath = sys.argv[2]

    try:
        with open(filePath, 'r') as f:
            fileContent = f.read()

            # decide which feature to run
            if task == 'find':
                FindFDSet(fileContent)
            elif task == 'list':
                ListFDSets(fileContent)
            else:
                print('Please specify a valid task to run (e.g., \'find\' or \'list\').')

            f.close()
    except IOError:
        line = 'Please specify the input file correctly.'

        print(line)
