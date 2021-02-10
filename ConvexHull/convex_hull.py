from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QPointF, QObject, QLineF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QPointF, QObject, QLineF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


# Global methods to use within the graphical aspects to make it easier to make polygons and lines

# Slices a list to include items within a starting and ending point
def circular_inclusive_slice(items, start, end):
    if start <= end:
        return items[start:end + 1]
    else:
        return items[start:] + items[:end + 1]


# Creates a polygon from QLineF's
def polygon_to_qt_lines(polygon):
    return [QLineF(polygon[i], polygon[(i + 1) % len(polygon)]) for i in range(len(polygon))]


# Creates a QLineF from a line
def lines_to_qt_lines(lines):
    return [QLineF(*line) for line in lines]

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(lines_to_qt_lines(line), color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(lines_to_qt_lines(line))

    def blinkTangent(self, line, color=BLUE):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color=RED):
        self.view.addLines(polygon_to_qt_lines(polygon), color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon_to_qt_lines(polygon))

    def showText(self, text):
        self.view.displayStatusText(text)

    # Sorts the points in ascending order
    def sortPoints(self, points: [QPointF]):
        sorted_points = sorted(points, key=lambda point: point.x())
        return sorted_points

    # Checks to see if 3rd point is crossing points a and b
    def isClockwise(self, a: QPointF, b: QPointF, c: QPointF):
        val = (b.y() - a.y()) * (c.x() - b.x()) - (c.y() - b.y()) * (b.x() - a.x())
        if (val == 0):
            return 0
        if (val > 0):
            return 1
        return -1

    # Merging the two hulls by finding the upper and lower tangents
    def conquer(self, leftHull: [QPointF], rightHull: [QPointF]):
        leftSize = len(leftHull)
        rightSize = len(rightHull)
        iL = 0
        iR = 0

        # Find the left most and rightmost points of the two hulls
        for i in range(leftSize):
            if leftHull[i].x() > leftHull[iL].x():
                iL = i
        for i in range(rightSize):
            if rightHull[i].x() < rightHull[iR].x():
                iR = i
        left_index = iL
        right_index = iR
        is_done = False

        # Finding the upper tangent through given algorithm
        while not is_done:
            is_done = True
            while len(leftHull) > 1 and self.isClockwise(rightHull[right_index], leftHull[left_index],
                                                         leftHull[(left_index + 1) % leftSize]) >= 0:
                left_index = (left_index + 1) % leftSize
            while len(rightHull) > 1 and self.isClockwise(leftHull[left_index], rightHull[right_index],
                                                          rightHull[(rightSize + right_index - 1) % rightSize]) <= 0:
                right_index = (rightSize + right_index - 1) % rightSize
                is_done = False

        upper_L = left_index
        upper_R = right_index
        left_index = iL
        right_index = iR
        is_done = False

        # Finding the lower tangent through the given algorithm
        while not is_done:
            is_done = True
            while len(rightHull) > 1 and self.isClockwise(leftHull[left_index], rightHull[right_index],
                                                          rightHull[(right_index + 1) % rightSize]) >= 0:
                right_index = (right_index + 1) % rightSize
            while len(leftHull) > 1 and self.isClockwise(rightHull[right_index], leftHull[left_index],
                                                         leftHull[(left_index - 1) % leftSize]) <= 0:
                left_index = (left_index - 1) % leftSize
                is_done = False

        lower_L = left_index
        lower_R = right_index

        # Shows tangent upon pausing
        if self.pause:
            self.blinkTangent([[leftHull[upper_L], rightHull[upper_R]], [leftHull[lower_L], rightHull[lower_R]]])

        hull = circular_inclusive_slice(leftHull, upper_L, lower_L) + circular_inclusive_slice(rightHull, lower_R,
                                                                                               upper_R)
        return hull

    # Divides and conquers two hulls
    def divide(self, points: [QPointF]):
        if len(points) <= 2:
            if len(points) == 2 and self.pause:
                self.showHull(points)
            return points

        half = len(points) // 2
        left = points[:half]
        right = points[half:]
        left_hull = self.divide(left)
        right_hull = self.divide(right)

        hull = self.conquer(left_hull, right_hull)
        if self.pause:
            self.eraseHull(left_hull)
            self.eraseHull(right_hull)
            self.showHull(hull)
        return hull

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        # Sorts the points left to right (ascending order) and saves the points
        left_to_right = self.sortPoints(points)

        t3 = time.time()

        # Resaves the left_to_right as points after divide and conquering
        points = self.divide(left_to_right)
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(points, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
