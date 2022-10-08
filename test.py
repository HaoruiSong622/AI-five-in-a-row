import board
from board import AI
import config
from functools import cmp_to_key

def pointcompare(a, b):
    return a.score - b.score

class Point_test(object):
    def __init__(self, x_=-1, y_=-1, score_=0):
        self.x = x_
        self.y = y_
        self.score = score_

a = Point_test(1, 1, 1)
b = Point_test(2, 2, 2)
c = Point_test(3, 3, 3)

# l = [b, a, c]
# print(l[0].x, l[1].x, l[2].x)
# l = sorted(l, key=cmp_to_key(pointcompare))
# print(l[0].x, l[1].x, l[2].x)
# d = Point_test()
# d = -1
# if type(d) == int:
#     print('yes')
