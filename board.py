import numpy as np
import config
from functools import cmp_to_key
from point import Point
from point import Node
import copy
from point import Obj
# Now I add a line directly on the website on my pc. And pull on the working copy. what will happen.

class Zobrist(object):
	def __init__(self):
		self.com = np.random.randint(low=1, high=1000000000, size=15*15)
		self.hum = np.random.randint(low=1, high=1000000000, size=15*15)
		self.code = np.random.randint(1000000000)

	def go(self, point, role):
		index = 15*point.x + point.y
		if role == config.com:
			self.code ^= self.com[index]
		else:
			self.code ^= self.hum[index]
		return self.code


class Board(object):
	def __init__(self):
		self.counter = 0  # number of chessmen
		self.board = np.zeros((15, 15), dtype=int)
		self.zobrist = Zobrist()

	def hasNeighbor(self, point, distance, cnt):
		sx = point.x - distance
		ex = point.x + distance
		sy = point.y - distance
		ey = point.y + distance
		for i in range(sx, ex + 1):
			if (i < 0 or i >= 15):
				continue
			for j in range(sy, ey + 1):
				if (j < 0 or j >= 15):
					continue
				if (i == point.x and j == point.y):
					continue
				if (self.board[i, j] != config.empty):
					cnt -= 1
					if (cnt <= 0):
						return True
		return False

	def increment(self):
		self.counter += 1

	def decrement(self):
		self.counter -= 1

	def getCounter(self):
		return self.counter


def pointCompare(a, b):
	return b.score - a.score

def pointCompare2(a, b):
	if a.score == b.score:
		if a.score >= 0:
			if a.step != b.step: return a.step - b.step
			else: return b.step - a.step
		else:
			if a.step != b.step: return -1 * (a.step - b.step)
			else: return -1 * (b.step - a.step)
	else: return b.score - a.score


class AI(Board):
	def __init__(self):
		Board.__init__(self)
		self.humScore = np.zeros((15, 15), dtype=int)
		self.comScore = np.zeros((15, 15), dtype=int)
		self.scoreCache = np.zeros((3, 4, 15, 15), dtype=int)
		self.allsteps = []
		self.comMaxScore = 0
		self.humMaxScore = 0
		self.Max = config.FIVE
		self.Min = config.FIVE * (-1)
		self.cache = {}
		# self.count = 0
		self.initScore()

	def isfive(self, point, role):  # checked
		len = 15
		cnt = 1
		i = point.y + 1
		while True:
			if i >= len: break
			t = self.board[point.x, i]
			if t != role: break
			cnt += 1
			i += 1
		i = point.y - 1
		while True:
			if i < 0: break
			t = self.board[point.x, i]
			if t != role: break
			cnt += 1
			i -= 1
		if cnt >= 5:
			print("1dir", point.x, point.y, "win")
			return True

		cnt = 1

		i = point.x + 1
		while True:
			if i >= len: break
			t = self.board[i, point.y]
			if t != role: break
			cnt += 1
			i += 1
		i = point.x - 1
		while True:
			if i < 0: break
			t = self.board[i, point.y]
			if t != role: break
			cnt += 1
			i -= 1
		if cnt >= 5:
			print("2dir", point.x, point.y, "win")
			return True

		cnt = 1

		i = 1
		while True:
			x, y = point.x + i, point.y + i
			if x >= len or y >= len: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		i = 1
		while True:
			x, y = point.x - i, point.y - i
			if x < 0 or y < 0: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		if cnt >= 5:
			print("3dir", point.x, point.y, "win")
			return True

		cnt = 1

		i = 1
		while True:
			x, y = point.x + i, point.y - i
			if x >= len or y < 0: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		i = 1
		while True:
			x, y = point.x - i, point.y + i
			if x < 0 or y >= len: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		if cnt >= 5:
			print("4dir", point.x, point.y, "win")
			return True
		return False

	def win(self):  # checked
		for i in range(0, 15):
			for j in range(0, 15):
				t = self.board[i, j]
				if t != config.empty:
					if self.isfive(Point(i, j), t):
						return t
		return -1

	def update(self, point, dir = -1):
		role = self.board[point.x, point.y]
		if role != config.hum:
			cs = self.scorePoint(point, config.com, dir)
			self.comScore[point.x, point.y] = cs
		else: self.comScore[point.x, point.y] = 0

		if role != config.com:
			hs = self.scorePoint(point, config.hum, dir)
			self.humScore[point.x, point.y] = hs
		else: self.humScore[point.x, point.y] = 0

	def updateScore(self, point):
		radius = 6
		for i in range(-radius, radius + 1):
			x, y = point.x, point.y + i
			if y < 0: continue
			if y >= 15: break
			self.update(Point(x, y), 0)

		for i in range(-radius, radius + 1):
			x, y = point.x + i, point.y
			if x < 0: continue
			if x >= 15: break
			self.update(Point(x, y), 1)

		for i in range(-radius, radius + 1):
			x, y = point.x + i, point.y + i
			if x < 0 or y < 0: continue
			if x >= 15 or y >= 15: break
			self.update(Point(x, y), 2)

		for i in range(-radius, radius + 1):
			x, y = point.x + i, point.y - i
			if x < 0 or y < 0: continue
			if x >= 15 or y >= 15: continue
			self.update(Point(x, y), 3)

	def put(self, point, role):
		point.role = role
		self.board[point.x, point.y] = role
		self.zobrist.go(point, role)
		self.updateScore(point)
		self.allsteps.append(point)

	def remove(self, point):
		r = self.board[point.x, point.y]
		self.zobrist.go(point, r)
		self.board[point.x, point.y] = config.empty
		self.updateScore(point)
		self.allsteps.pop()
		# todo: finish the function
		pass

	def initScore(self):
		for i in range(0, 15):
			for j in range(0, 15):
				if self.board[i][j] == config.empty:
					if self.hasNeighbor(Point(i, j), 2, 2):
						cs = self.scorePoint((i, j), config.com)
						hs = self.scorePoint((i, j), config.hum)
						self.comScore[i, j] = cs
						self.humScore[i, j] = hs
				elif self.board[i][j] == config.com:
					self.comScore[i][j] = self.scorePoint((i, j), config.com)
					self.humScore[i][j] = 0
				else:
					self.humScore[i][j] = self.scorePoint((i, j), config.hum)
					self.comScore[i][j] = 0

#  point[x, y, score, step]
	def scorePoint(self, point, role, dir=-1):
		ret = 0
		empty = 0
		cnt = block = secondCount = 0



		if dir == -1 or dir == 0:
			cnt = 1
			block = secondCount = 0
			empty = -1
			i = point.y + 1
			while True:

				if i >= 15:
					block += 1
					break
				t = self.board[point.x, i]
				if t == config.empty:
					if empty == -1 and i < 15 - 1 and self.board[point.x, i + 1] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break
			i = point.y - 1
			while True:

				if i < 0:
					block += 1
					break
				t = self.board[point.x, i]
				if t == config.empty:
					if empty == -1 and i > 0 and self.board[point.x, i - 1] == role:
						empty = 0
						i -= 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != -1:
						empty += 1
					i -= 1
					continue
				else:
					block += 1
					break
			cnt += secondCount
			self.scoreCache[role, 0, point.x, point.y] = self.countToScore(cnt, block, empty)
		ret += self.scoreCache[role, 0, point.x, point.y]



		if dir == -1 or dir == 1:
			cnt = 1
			block = secondCount = 0
			empty = -1
			i = point.x + 1
			while True:

				if i >= 15:
					block += 1
					break
				t = self.board[i, point.y]
				if t == config.empty:
					if empty == -1 and i < 15 - 1 and self.board[i + 1, point.y] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break
			i = point.x - 1

			while True:

				if i < 0:
					block += 1
					break
				t = self.board[i, point.y]
				if t == config.empty:
					if empty == -1 and i > 0 and self.board[i - 1, point.y] == role:
						empty = 0
						i -= 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != 1:
						empty += 1
					i -= 1
					continue
				else:
					block += 1
					break
			cnt += secondCount
			self.scoreCache[role, 1, point.x, point.y] = self.countToScore(cnt, block, empty)
		ret += self.scoreCache[role, 1, point.x, point.y]



		if dir == -1 or dir == 2:
			cnt = 1
			block = secondCount = 0
			empty = -1
			i = 1
			while True:

				x, y = point.x + i, point.y + i
				if x >= 15 or y >= 15:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and x < 15 - 1 and y < 15 - 1 and self.board[x + 1, y + 1] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break
			i = 1
			while True:

				x, y = point.x - i, point.y - i
				if x < 0 or y < 0:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and x > 0 and y > 0 and self.board[x - 1, y - 1] == role:
						empty = 0
						i += 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != -1:
						empty += 1
					i += 1
					continue
				else:
					block += 1
					break
			cnt += secondCount
			self.scoreCache[role, 2, point.x, point.y] = self.countToScore(cnt, block, empty)
		ret += self.scoreCache[role, 2, point.x, point.y]

		if dir == -1 or dir == 3:
			cnt = 1
			block = secondCount = 0
			empty = -1
			i = 1
			while True:

				x, y = point.x + i, point.y - i
				if x >= 15 or y >= 15 or x < 0 or y < 0:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and x < 15 - 1 and 0 < y and self.board[x + 1, y - 1] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break
			i = 1
			while True:

				x, y = point.x - i, point.y + i
				if x >= 15 or y >= 15 or x < 0 or y < 0:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and 0 < x and y < 15 - 1 and self.board[x - 1, y + 1] == role:
						empty = 0
						i += 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != -1:
						empty += 1
					i += 1
					continue
				else:
					block += 1
					break
			cnt += secondCount
			self.scoreCache[role, 3, point.x, point.y] = self.countToScore(cnt, block, empty)
		ret += self.scoreCache[role, 3, point.x, point.y]
		return ret

	def countToScore(self, cnt, block, empty):
		if empty <= 0:
			if cnt >= 5: return config.FIVE
			if block == 0:
				if cnt == 1: return config.ONE
				elif cnt == 2: return config.TWO
				elif cnt == 3: return config.THREE
				elif cnt == 4: return config.FOUR
			elif block == 1:
				if cnt == 1: return config.BLOCKED_ONE
				elif cnt == 2: return config.BLOCKED_TWO
				elif cnt == 3: return config.BLOCKED_THREE
				elif cnt == 4: return config.BLOCKED_FOUR
		elif empty == 1 or empty == cnt - 1:
			if cnt >= 6: return config.FIVE
			if block == 0:
				if cnt == 2: return config.TWO / 2
				elif cnt == 3: return config.THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.FOUR
			if block == 1:
				if cnt == 2: return config.BLOCKED_TWO
				elif cnt == 3: return config.BLOCKED_THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.BLOCKED_FOUR
		elif empty == 2 or empty == cnt - 2:
			if cnt >= 7: return config.FIVE
			if block == 0:
				if cnt == 3: return config.THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.BLOCKED_FOUR
				elif cnt == 6: return config.FOUR
			elif block == 1:
				if cnt == 3: return config.BLOCKED_THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.BLOCKED_FOUR
				elif cnt == 6: return config.FOUR  # ?
			elif block == 2:
				if cnt == 4 or cnt == 5 or cnt == 6: return config.BLOCKED_FOUR
		elif empty == 3 or empty == cnt - 3:
			if cnt >= 8: return config.FIVE
			if block == 0:
				if cnt == 4 or cnt == 5: return config.THREE
				elif cnt == 6: return config.BLOCKED_FOUR
				elif cnt == 7: return config.FOUR
			elif block == 1:
				if cnt == 4 or cnt == 5 or cnt == 6: return config.BLOCKED_FOUR
				elif cnt == 7: return config.FOUR
			elif block == 2:
				if 4 <= cnt <= 7: return config.BLOCKED_FOUR
		elif empty == 4 or empty == cnt - 4:
			if cnt >= 9: return config.FIVE
			if block == 0:
				if 5 <= cnt <= 8:return config.FOUR
			elif block == 1:
				if 4 <= cnt <= 7: return config.BLOCKED_FOUR
				elif cnt == 8: return  config.FOUR
			elif block == 2:
				if 5 <= cnt <= 8: return config.BLOCKED_FOUR
		elif empty == 5 or empty == cnt - 5: return config.FIVE

		return 0



	def deeping(self, deep):
		candidates = self.gen(config.com)
		self.Cache = {}
		for i in range(2, deep + 1, 2):
			bestScore = self.negamax(candidates, i, -1 * config.FIVE, config.FIVE)
			if bestScore >= config.FIVE: break

		candidates = sorted(candidates, key=cmp_to_key(pointCompare2))
		for i in candidates:
			if self.isfive(i, config.com) or self.isfive(i, config.hum):
				return i
		ret = -1
		for i in range(15):
			for j in range(15):
				if self.board[i, j] == config.empty:
					if self.isfive(Point(i, j), config.com):
						return Point(i, j, config.com)
					elif self.isfive(Point(i, j), config.hum):
						ret = Point(i, j, config.com)

		if type(ret) == Point:
			return ret


		result = candidates[0]
		return result



	def gen(self, role, onlyThrees=False, starSpread=False):
		fives = []
		comfours = []
		humfours = []
		comblockedfours = []
		humblockedfours = []
		comtwothrees = []
		humtwothrees = []
		comthrees = []
		humthrees = []
		comtwos = []
		humtwos = []
		neighbors = []
		si = sj = 0
		ei = ej = 14
		lastpoint1, lastpoint2 = Point(), Point()  # point len = 4

		if starSpread and config.star:
			i = len(self.allsteps) - 1
			while lastpoint1.x != -1 and i >= 0:
				p = self.allsteps[i]
				if p.role != role and p.attack != role:
					lastpoint1 = p
				i -= 2

			if lastpoint1.x != -1:
				lastpoint1 = self.allsteps[0] if self.allsteps[0].role != role else self.allsteps[1]

			i = len(self.allsteps) - 2
			while lastpoint2.x != -1 and i >= 0:
				p = self.allsteps[i]
				if p.attack == role:
					lastpoint2 = p
				i -= 2

			if lastpoint2.x != -1:
				lastpoint2 = self.allsteps[0] if self.allsteps[0].role != role else self.allsteps[1]

			si = min(lastpoint1.x - 5, lastpoint2.x - 5)
			sj = min(lastpoint1.y - 5, lastpoint2.y - 5)
			si = max(si, 0)
			sj = max(sj, 0)
			ei = max(lastpoint1.x + 5, lastpoint2.x + 5)
			ej = max(lastpoint1.y + 5, lastpoint2.y + 5)
			ei = min(14, ei)
			ej = min(14, ej)

		for i in range(si, ei + 1):
			for j in range(sj, ej + 1):
				if self.board[i, j] == config.empty:
					if len(self.allsteps) < 6:
						if not self.hasNeighbor(Point(i, j), 1, 1): continue
					elif not self.hasNeighbor(Point(i, j), 2, 2): continue
					p = Point(i, j)
					scoreHum = p.scoreHum = self.humScore[i, j]
					scoreCom = p.scoreCom = self.comScore[i, j]
					maxScore = max(scoreCom, scoreHum)
					p.score = maxScore
					p.role = role

					if scoreCom > scoreHum: p.attack = config.com
					else: p.attack = config.hum
					if starSpread and config.star:
						if ((abs(i - lastpoint1.x) > 5 or abs(j - lastpoint1.y) > 5)
							and (abs(i - lastpoint2.x) > 5 or abs(j - lastpoint2.y) > 5)): continue
						if (maxScore >= config.FIVE or
								(i == lastpoint1.x or j == lastpoint1.y or abs(i - lastpoint1.x) == abs(j - lastpoint1.y)) or
								(i == lastpoint2.x or j == lastpoint2.y or abs(i - lastpoint2.x) == abs(j - lastpoint2.y))):
							pass
						else: continue

					if scoreCom >= config.FIVE: fives.append(p)
					elif scoreHum >= config.FIVE: fives.append(p)
					elif scoreCom >= config.FOUR: comfours.append(p)
					elif scoreHum >= config.FOUR: humfours.append(p)
					elif scoreCom >= config.BLOCKED_FOUR: comblockedfours.append(p)
					elif scoreHum >= config.BLOCKED_FOUR: humblockedfours.append(p)
					elif scoreCom >= config.THREE * 2: comtwothrees.append(p)
					elif scoreHum >= config.THREE * 2: humtwothrees.append(p)
					elif scoreCom >= config.THREE: comthrees.append(p)
					elif scoreHum >= config.THREE: humthrees.append(p)
					elif scoreCom >= config.TWO: comtwos.insert(0, p)
					elif scoreHum >= config.TWO: humtwos.insert(0, p)
					else: neighbors.append(p)

		if len(fives) > 0: return fives
		if role == config.com and len(comfours) > 0: return comfours
		if role == config.hum and len(humfours) > 0: return humfours  # here I made a mistake
		if role == config.com and len(humfours) > 0 and len(comblockedfours) == 0: return humfours
		if role == config.hum and len(comfours) > 0 and len(humblockedfours) == 0: return comfours



		if role == config.com: fours = comfours + humfours
		else: fours = humfours + comfours

		if role == config.com: blockedfours = comblockedfours + humblockedfours
		else: blockedfours = humblockedfours + comblockedfours

		if len(fours) > 0: return fours + blockedfours

		ret = []
		if role == config.com:
			ret = (comtwothrees + humtwothrees + comblockedfours + humblockedfours
				   + comthrees + humthrees)
		if role == config.hum:
			ret = (humtwothrees + comtwothrees + humblockedfours + comblockedfours
				   + humthrees + comthrees)
		if len(comtwothrees) > 0 or len(humtwothrees) > 0: return ret

		if onlyThrees: return ret

		if role == config.com: twos = comtwos + humtwos
		else: twos = humtwos + comtwos

		twos = sorted(twos, key=cmp_to_key(pointCompare))
		if len(twos) > 0: ret += twos
		else: ret += neighbors

		countlimit = 20
		if len(ret) > countlimit: ret = ret[0:20]

		return ret

	def fixScore(self, type):
		if config.BLOCKED_FOUR <= type < config.FOUR:
			if config.BLOCKED_FOUR <= type < config.BLOCKED_FOUR + config.THREE:
				return config.THREE
			elif config.BLOCKED_FOUR + config.THREE <= type < config.BLOCKED_FOUR * 2:
				return config.FOUR
			else:
				return config.FOUR * 2

		return type

	def cachefunc(self, deep, score):
		if not config.cache: return
		obj = Obj()
		obj.deep = deep
		obj.score.score = score.score
		obj.score.step = score.step
		obj.score.steps = score.steps
		# obj.b = self.toString() attention here
		self.cache[self.zobrist.code] = obj

	def evaluate(self, role):
		self.comMaxScore = 0
		self.humMaxScore = 0
		
		for i in range(0, 15):
			for j in range(0, 15):
				if self.board[i, j] == config.com:
					self.comMaxScore += self.fixScore(self.comScore[i, j])
				elif self.board[i, j] == config.hum:
					self.humMaxScore += self.fixScore(self.humScore[i, j])
		if role == config.com:
			result = self.comMaxScore - self.humMaxScore
		else:
			result = (self.comMaxScore - self.humMaxScore) * (-1)
		
		return result

	def r(self, deep, alpha, beta, role, step, steps, spread):
		if config.cache:
			if self.zobrist.code in self.cache:
				c = self.cache[self.zobrist.code]
				if c.deep >= deep:
					ret = Node()
					ret.score = c.score.score
					ret.steps = c.steps
					ret.step = c.step
					return ret
				else:
					if c.score.score >= config.FOUR or c.score.score <= -1 * config.FOUR:
						return c.score
		
		_e = self.evaluate(role)
		
		leaf = Node()
		leaf.score = _e
		leaf.step = step
		leaf.steps = steps  # attention not copy here
		
		if deep <= 0 or _e >= config.FIVE or _e <= -1 * config.FIVE:
			return leaf
		best = Node()
		best.score = self.Min
		best.step = step
		best.steps = steps
		
		points = self.gen(role, step > 4, step > 4)
		
		if len(points) == 0: return leaf
		
		for i in points:
			self.put(i, role)
			_deep = deep - 1
			
			_spread = spread
			
			if _spread < config.spreadLimit:
				if (role == config.com and i.scoreHum >= config.FIVE) or (role == config.hum and i.scoreCom >= config.FIVE):
					_deep += 2
					_spread += 1
			
			_steps = copy.copy(steps)
			_steps.append(i)
			v = self.r(_deep, -beta, -alpha, config.reverse(role), step+1, _steps, _spread)
			v.score *= -1
			self.remove(i)
			
			if v.score > best.score:
				best = v
			alpha = max(best.score, alpha)
			# cutting
			if v.score >= beta:
				v.score = self.Max - 1
				return v
		
		self.cachefunc(deep, best)
		
		return best

	def negamax(self, candidates, deep, alpha, beta):
		for i in range(0, len(candidates)):
			p = candidates[i]
			self.put(p, config.com)
			steps = []
			steps.append(p)
			v = self.r(deep - 1, -beta, -alpha, config.hum, 1, copy.copy(steps), 0)
			v.score *= -1
			alpha = max(alpha, v.score)
			self.remove(p)
			candidates[i].score = v.score
			candidates[i].steps = v.steps
		return alpha




