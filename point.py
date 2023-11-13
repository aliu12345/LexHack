

class Point:

    def __init__(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis

    def shift(self, x, y):
        self.x_axis += x
        self.y_axis += y

    def to_tuple(self):
        return self.x_axis, self.y_axis