"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: April, 2017

blines:

This file contains an implementation of the Bresenham Algorithm.
This method returns the discrete (integral) coordinates
of all points along a line between two arbitrary points in
a two-dimensional array.

For vertical or horizontal lines this trivially returns the
row or column. For diagonal lines, it discerns which array
elements are crossed by the line and returns the points.
"""

import numpy as np


def bline(x0, y0, xf, yf):
    """Implementation of Bresenham Algorithm - Adapted from Java.

    Based on algorithm listed here:
    http://tech-algorithm.com/articles/drawing-line-using-bresenham-algorithm/
    Translated to Python by Maxwell Grady

    :param x0: int initial x location of line segment
    :param y0: int initial y location of line segment
    :param xf: int final x location of line segment
    :param yf: int final y location of line segment
    :returns:  list of points in (x, y) format for pixels along the line segment
    """
    w = xf - x0  # run
    h = yf - y0  # rise
    dx1 = 0
    dy1 = 0
    dx2 = 0
    dy2 = 0
    # To speed up this calculation, first check for pure vertical or horizontal lines
    if w != 0 and h == 0:
        # horizontal line:
        points = [(x0, y0)]
        dx = 1*np.sign(xf - x0)
        while len(points) < w + 1:
            points.append((points[-1][0] + dx, y0))
        return points
    if w == 0 and h != 0:
        # vertical line
        points = [(x0, y0)]
        dy = 1*np.sign(yf - y0)
        while len(points) < h + 1:
            points.append((x0, points[-1][1] + dy))
        return points

    # configure settings for which Octant the line falls in
    if w < 0:
        dx1 = -1
        dx2 = -1
    elif w > 0:
        dx1 = 1
        dx2 = 1

    if h < 0:
        dy1 = -1
    elif h > 0:
        dy1 = 1

    longest = abs(w)
    shortest = abs(h)
    if not longest > shortest:
        longest = abs(h)
        shortest = abs(w)
        if h < 0:
            dy2 = -1
        elif h > 0:
            dy2 = 1
        dx2 = 0

    # start calculation
    numerator = longest >> 1
    x = x0
    y = y0  # the first point appended will be the initial point of the line
    points = []
    for i in range(longest + 1):
        points.append((x, y))
        numerator += shortest
        if not numerator < longest:
            numerator -= longest
            x += dx1
            y += dy1
        else:
            x += dx2
            y += dy2
    return points
