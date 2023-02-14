import numpy as np


class Vector:
    def __init__(self, data):
        self.data = np.array(data)

    def norm(self):
        return np.linalg.norm(self.data)

    def __add__(self, other):
        return Vector(self.data + other.data)

    def __sub__(self, other):
        return Vector(self.data - other.data)

    def __mul__(self, scalar):
        return Vector(self.data * scalar)

    def __truediv__(self, scalar):
        return Vector(self.data / scalar)

    def dot(self, other):
        return np.dot(self.data, other.data)

    def cross(self, other):
        return Vector(np.cross(self.data, other.data))