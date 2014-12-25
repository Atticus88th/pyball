from cmath import sqrt

class Vector:
    def __init__(self, (x, y)):
        self.x = x
        self.y = y
        self.v = abs(sqrt(x**2 + y**2))
