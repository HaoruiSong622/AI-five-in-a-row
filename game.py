from board import AI
import config
from point import Point


class Game(object):
    def __init__(self):
        self.board = AI()

    def start(self):
        self.board = AI()

    def begin(self):
        if len(self.board.allsteps) == 0:
            self.set(7, 7, config.com)
            return Point(7, 7, config.com)
        p = self.board.deeping(config.searchdeep)
        self.board.put(p, config.com)
        self.board.increment()
        return p

    def set(self, x, y, role):
        self.board.put(Point(x, y), role)
        self.board.increment()

    def check(self):
        temp = self.board.win()
        if temp != -1:
            print(temp, "win")
        return temp
