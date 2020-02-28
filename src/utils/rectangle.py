import cv2
import numpy as np
from scipy.spatial import distance as dist

HEIGHT_INFERIOR = 42
HEIGHT_SUPERIOR = 59
WIDTH_INFERIOR = 21
WIDTH_SUPERIOR = 35


class Rectangle:

    def __init__(self, points):
        self.points = self.order_points(points)
        self.distances()
        self.sin = (self.points[0][1] - self.points[1][1]) / self.width

    def order_points(self, points):
        x_sorted = points[np.argsort(points[:, 0]), :]
        left = x_sorted[:2, :]
        right = x_sorted[2:, :]
        (top_left, bottom_left) = left[np.argsort(left[:, 1]), :]
        D = dist.cdist(top_left[np.newaxis], right, "euclidean")[0]
        (bottom_right, top_right) = right[np.argsort(D)[::-1], :]
        return np.array([top_left, top_right, bottom_right,
                         bottom_left], dtype="float32")

    def dist_box(self, new):
        dist_dot = []
        for i in range(4):
            dist_dot.append(
                np.sqrt(
                    np.power(
                        self.points[i][0] -
                        new[i][0],
                        2) +
                    np.power(
                        self.points[i][1] -
                        new[i][1],
                        2)))
        return np.average(np.array(dist_dot))

    def dimension_limits(self):
        if ((self.height >= HEIGHT_INFERIOR and self.height <= HEIGHT_SUPERIOR) and (
                self.width >= WIDTH_INFERIOR and self.width <= WIDTH_SUPERIOR)):
            return True
        else:
            return False

    def distances(self):
        dist_1 = np.sqrt(np.power(self.points[0][0] - self.points[1][0], 2) +
            np.power(self.points[0][1] - self.points[1][1], 2))
        dist_2 = np.sqrt(np.power(self.points[0][0] - self.points[2][0], 2) +
            np.power(self.points[0][1] - self.points[2][1], 2))
        dist_3 = np.sqrt(np.power(self.points[0][0] - self.points[3][0], 2) +
            np.power(self.points[0][1] - self.points[3][1], 2))
        dist_4 = np.sqrt(np.power(self.points[1][0] - self.points[2][0], 2) +
            np.power(self.points[1][1] - self.points[2][1], 2))
        dist_5 = np.sqrt(np.power(self.points[1][0] - self.points[3][0], 2) +
            np.power(self.points[1][1] - self.points[3][1], 2))
        dist_6 = np.sqrt(np.power(self.points[2][0] - self.points[3][0], 2) +
            np.power(self.points[2][1] - self.points[3][1], 2))
        dists = sorted([dist_1, dist_2, dist_3, dist_4, dist_5, dist_6])
        self.width = dists[0]
        self.height = dists[2]