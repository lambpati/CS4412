from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
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
		self.view.addLines(line, color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self, line, color):
		self.showTangent(line, color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon, color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self, polygon):
		self.view.clearLines(polygon)

	def showText(self, text):
		self.view.displayStatusText(text)

	# Sorts the points in ascending order
	def sortPoints(self, points: [QPointF]):
		sorted_points = sorted(points, key=lambda point: point.x())
		return sorted_points

	# Checks which quadrant the points are in
	def findQuad(self, point: QPointF):
		if point.x() >= 0:
			if point.y() >= 0:
				return 1
			return 4
		if point.x() <= 0:
			if point.y() <= 0:
				return 3
			return 2

	# Checks to see if 3rd point is crossing points a and b
	def isCrossing(self, a: QPointF, b: QPointF, c: QPointF):
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
		for i in leftSize:
			if leftHull[i].x() > rightHull[iL].x():
				iL = i
		for i in rightSize:
			if rightHull[i].x() < rightHull[iR].x():
				iR = i
		left_index = iL
		right_index = iR
		is_done = False

		# Finding the upper tangent through given algorithm
		while not is_done:
			is_done = True
			while self.isCrossing(rightHull[right_index], leftHull[left_index],
			                      leftHull[(left_index + 1) % leftSize]) >= 0:
				left_index = (left_index + 1) % leftSize
			while self.isCrossing(leftHull[left_index], rightHull[right_index],
			                      rightHull[(rightSize + right_index - 1) % rightSize] <= 0):
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
			while self.isCrossing(leftHull[left_index], rightHull[right_index],rightHull[(right_index + 1) % rightSize]) >= 0:
				right_index = (right_index + 1) % rightSize
			while self.isCrossing(rightHull[right_index], leftHull[left_index],leftHull[leftSize + left_index - 1] % leftSize) <= 0:
				left_index = (leftSize + left_index - 1) % leftSize
				is_done = False

		lower_L = left_index
		lower_R = right_index

	# Divides and conquers two hulls
	def divide(self, points: [QPointF]):
		if len(points) <= 3:
			return points
		half = len(points) // 2
		left = points[:half]
		right = points[:half]
		left_hull = self.divide(left)
		right_hull = self.divide(right)

		return self.conquer(left_hull, right_hull)

	# This is the method that gets called by the GUI and actually executes
	# the finding of the hull
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert (type(points) == list and type(points[0]) == QPointF)

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		print(self.sortPoints(points))
		# points = self.sortPoints(points)
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		# polygon = [QLineF(points[i], points[(i + 1) % 3]) for i in range(3)]
		polygon = [self.divide(points)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()
		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon, RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
