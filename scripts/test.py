#!/usr/bin/env python
# Script for testing Matt Rueben's 2-d tree implementation. 

from matplotlib import pyplot
from iris import get_iris_data
from kd_trees import Tree

if __name__ == '__main__':

    # The data
    x, y = get_iris_data()
    pyplot.plot(x, y, 'k.')

    # The 2-d tree
    tree = Tree()
    tree.set_members(x, y)
    result = tree.branch_out('y', depth=4)
    tree.plot_tree(depth=4)
