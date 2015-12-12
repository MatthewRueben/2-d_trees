#!/usr/bin/env python
# Class definitions for Matt Rueben's 2-d tree implementation.

class Point(object):
    """ A 2D point. """
    def __init__(self, x, y):
        self.x = x
        self.y = y


import numpy as np

class PointList(object):
    """ Contains a list of Point objects.  Has methods for splitting
    along the median in either the x- or y-direction. """
    def __init__(self):
        self.points = []

    def add_point(self, pt):
        self.points.append(pt)

    def set_points(self, pts):
        self.points = pts

    def get_median(self, axis):
        """ Finds median point along one axis. 
        Can be 'x' or 'y'. """
        array = np.asarray([pt.__getattribute__(axis) for pt in self.points])
        median = np.median(array)
        return median

    def get_points_below(self, axis, juncture):
        array = np.asarray([pt.__getattribute__(axis) for pt in self.points])
        return [pt for i, pt in enumerate(self.points) if array[i] <= juncture]  # inclusive
        
    def get_points_above(self, axis, juncture):
        array = np.asarray([pt.__getattribute__(axis) for pt in self.points])
        return [pt for i, pt in enumerate(self.points) if array[i] > juncture]  # strict


from matplotlib import pyplot        
from copy import deepcopy

class Tree(object):
    def __init__(self, limits={'x':[-10, 10],'y':[-10, 10]}, last=None):
        """ 'last' is expected to be of form {'axis': <either 'x' or 'y'>, 
                                              'juncture': <float>, 
                                              'direction': <either 'lower' or 'higher'>}. 
        (it should really be a custom object) """
        self.members = PointList()

        self.limits = limits
        if not isinstance(last, type(None)):  # if we have info about the last juncture
            # handle the inheritance of region limits
            print 'info!', 'last juncture:', last['juncture']
            if last['direction'] == 'lower':
                print 'low', last['juncture']
                limits[last['axis']][1] = last['juncture']
            elif last['direction'] == 'higher':
                print 'high', last['juncture']
                limits[last['axis']][0] = last['juncture']
        print ''
        print ''

    def set_members(self, x, y):
        """ Load points as two Nx1 lists, one for x and one for y. """
        for x_i, y_i in zip(x, y):
            member = Point(x_i, y_i)
            self.members.add_point(member)

    def branch_out(self, axis, depth):
        """ Sets breakpoint along one axis. 
        Axis can be 'x' or 'y'. 
        Will branch recursively until depth is zero. """
        self.axis = axis  # remember which way this node branched
        
        self.juncture = self.members.get_median(axis)  # set median as juncture point

        self.branch_lower = Tree(limits=deepcopy(self.limits), 
                                 last={'axis': self.axis, 'juncture': self.juncture, 'direction': 'lower'})  # make the two child trees
        self.branch_higher = Tree(limits=deepcopy(self.limits), 
                                  last={'axis': self.axis, 'juncture': self.juncture, 'direction': 'higher'})

        # Next time, branch along the other axis
        if axis == 'x': 
            next_axis = 'y'
        elif axis == 'y':
            next_axis = 'x'

        # Divide the points between the two branches
        self.branch_lower.members.set_points(
            self.members.get_points_below(axis, self.juncture))  # INCLUDES branch point!
        self.branch_higher.members.set_points(
            self.members.get_points_above(axis, self.juncture))

        # Keep branching recursively until depth is zero
        if depth > 0:
            result_lower = self.branch_lower.branch_out(next_axis, depth-1)
            result_higher = self.branch_higher.branch_out(next_axis, depth-1)
            return {'lower': result_lower, 'higher': result_higher}  # results will quickly become lengthy
        elif depth == 0:
            return 0 

    def plot_tree(self, depth):
        """ Plots all the points in this node and all the divisions
        below it using self.plot_branch() """
        x = [pt.__getattribute__('x') for pt in self.members.points]  # These can't go in the recursion, says I. 
        y = [pt.__getattribute__('y') for pt in self.members.points]
        pyplot.plot(x, y, 'k.')
        pyplot.autoscale(False)  # toggles autoscaling off
        self.plot_branch(depth)
        pyplot.show()

    def plot_branch(self, depth):
        """ Plot division lines. """
        if depth >= 0:  # note that this is strict inequality in self.branch_out()
            # Plot the branch line
            print self.axis, self.limits, self.juncture
            if self.axis == 'x':
                print 'vert!'
                pyplot.plot([self.juncture, self.juncture], 
                            [self.limits['y'][0], self.limits['y'][1]], 'b')  # vertical line
            elif self.axis == 'y':
                print 'horiz!'
                pyplot.plot([self.limits['x'][0], self.limits['x'][1]], 
                            [self.juncture, self.juncture], 'r')  # horizontal line

            # Recurse
            self.branch_lower.plot_branch(depth-1)
            self.branch_higher.plot_branch(depth-1)

        elif depth < 0:
            return 0
