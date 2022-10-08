import config


class Point:
    def __init__(self, x_=-1, y_=-1, role_=config.empty):
        self.x = x_
        self.y = y_
        self.scoreHum = 0
        self.scoreCom = 0
        self.score = 0
        self.role = role_
        self.attack = config.empty
        self.steps = []
        self.step = 0


class Node:
    def __init__(self):
        self.steps = []
        self.step = 0
        self.score = 0


class Obj:
    def __init__(self):
        self.deep = 0
        self.score = Node()
        self.step = 0
        self.steps = []
        self.b = ''