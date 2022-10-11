from setuptools import setup, find_packages

setup(name='FrontdoorAdjustmentSets', packages=find_packages(), description='Finds and Lists Pearl\'s Front-door Adjustment Sets',
      author='Hyunchai Jeong', author_email='jeong3@purdue.edu', keywords=['causality', 'algorithm', 'frontdoor adjustment'], url='https://github.com/CausalAILab/FrontdoorAdjustmentSets', requires=['networkx', 'pydash', 'toposort'])
