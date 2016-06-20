#!/usr/bin/env python
#coding:utf-8

"""
Name: Haoxiang Gao
UNI: hg2412
Email: hg2412@columbia.edu
"""

from random import randint
from BaseAI import BaseAI
from copy import deepcopy
import math
import Queue

MAX_DEPTH = 8
TURN = [0,1] #0 represents player's turn; 1 represents Computer's turn

class PlayerAI(BaseAI):
    
    def getMove(self, grid):
        # I'm too naive, please change me!
        max_move = 0
        max_score = float("-inf")
        
        for d in xrange(1, MAX_DEPTH):
            move, score = self.search(grid, float('-inf'), float('inf'), 1, 0, d)
            if score > max_score:
                max_score = score
                max_move = move
        return max_move

    def search(self, grid, alpha, beta, depth, turn, max_depth):
        if depth > max_depth or not grid.canMove():
            return self.evaluate(grid)
        # player's turn
        if turn == TURN[0]:
            moves = grid.getAvailableMoves()
            result_move = moves[0]
            v = float('-inf')
            for m in moves:
                grid_copy = grid.clone()
                grid_copy.move(m)
                prev_v = v
                v = max(v, self.search(grid_copy, alpha, beta, depth + 1, 1 - turn, max_depth))
                if v > prev_v and depth == 1:
                    result_move = m
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            if depth == 1:
                return (result_move, v)
            return v
        # computer's turn        
        else:
            available_tiles = grid.getAvailableCells()
            v = float('inf')
            for t in available_tiles:
                grid_copy = grid.clone()
                grid_copy.insertTile(t, 2)
                v = min(v, self.search(grid_copy, alpha, beta, depth + 1, 1 - turn, max_depth))
                if v <= alpha:
                    return v
                beta = min(beta, v)
                
    def evaluate(self, grid):
        num_blank = len(grid.getAvailableCells())
        max_tile = grid.getMaxTile()
        if num_blank == 0:
            return math.log(max_tile, 2) - 100
        monoticity = self.get_monoticity2(grid) * 2
        if math.log(max_tile, 2) >= 8:
            monoticity = self.get_monoticity2(grid) * 2

        smoothness = self.get_smoothness(grid) * 0.1 + self.get_smoothness2(grid)
        return math.log(max_tile, 2) * 10 + num_blank * 3 + monoticity + smoothness * 0.1

    def get_monoticity(self, grid):
        max_value = grid.getMaxTile()
        max_pos = (1,1)
        max_dec = float('-inf')
        for i in xrange(0, grid.size):
            for j in xrange(0, grid.size):
                if grid.map[i][j] == max_value:
                    dec = abs(i - 1.5) + abs(j - 1.5)
                    if dec > max_dec:
                        max_pos = (i, j)
                        max_dec = dec

        sum_mono = 0
        if max_dec == 3:

            for i in xrange(1,grid.size):
                if not grid.crossBound((max_pos[0] + i, max_pos[1])):
                    if grid.getCellValue((max_pos[0] + i, max_pos[1])) == 0:
                        break
                    if math.log(grid.getCellValue((max_pos[0] + i, max_pos[1])),2) - math.log(grid.getCellValue((max_pos[0] + i - 1, max_pos[1])),2) <= 1:
                        sum_mono += 1

    
            for i in xrange(1,grid.size):
                if not grid.crossBound((max_pos[0] - i, max_pos[1])):
                    if grid.getCellValue((max_pos[0] - i, max_pos[1])) == 0:
                        break
                    if math.log(grid.getCellValue((max_pos[0] - i, max_pos[1])),2) - math.log(grid.getCellValue((max_pos[0] - i + 1, max_pos[1])),2) <= 1:
                        sum_mono += 1

    
            for i in xrange(1,grid.size):
                if not grid.crossBound((max_pos[0], max_pos[1] + i)):
                    if grid.getCellValue((max_pos[0], max_pos[1] + i)) == 0:
                        break
                    if math.log(grid.getCellValue((max_pos[0], max_pos[1] + i)),2) - math.log(grid.getCellValue((max_pos[0], max_pos[1] + i - 1)),2) <= 1:
                        sum_mono += 1
                        
                        
            for i in xrange(1,grid.size):
                if not grid.crossBound((max_pos[0], max_pos[1] - i)):
                    if grid.getCellValue((max_pos[0], max_pos[1] - i)) == 0:
                        break
                    if math.log(grid.getCellValue((max_pos[0], max_pos[1] - i)),2) - math.log(grid.getCellValue((max_pos[0], max_pos[1] - i + 1)),2) <= 1:
                        sum_mono += 1
        
        if sum_mono >=3:
            return 3
        return sum_mono

    def get_monoticity2(self, grid):
        
        max_value = grid.getMaxTile()
        max_pos = [0,0]
        max_dec = float('-inf')
        for i in xrange(0, grid.size):
            for j in xrange(0, grid.size):
                if grid.map[i][j] == max_value:
                    dec = abs(i - 1.5) + abs(j - 1.5)
                    if dec > max_dec:
                        max_pos = (i, j)
                        max_dec = dec

        sum_mono = 0

        if max_dec == 3:
            sum_mono += math.log(max_value)
            x_dir = 0
            y_dir = 0
            if max_pos[0] == 0 and max_pos[1] == 0:
                x_dir = 1
                y_dir = 1
            elif max_pos[0] == 3 and max_pos[1]== 3:
                x_dir = -1
                y_dir = -1
            elif max_pos[0] == 3 and max_pos[1] == 0:
                x_dir = -1
                y_dir = 1
            else:
                x_dir = 1
                y_dir = -1

            xy_dir = (x_dir, y_dir)

            sum_mono1 = 0

            cursor = deepcopy(max_pos)
            for i in xrange(1, grid.size * 2):
                prev = deepcopy(cursor)
                if grid.getCellValue(cursor) == 0:
                    break
                if i % 4 == 0:
                    cursor = (cursor[0], cursor[1] + y_dir)
                    x_dir = -1 * x_dir
                else:
                    cursor = (cursor[0] + x_dir, cursor[1])
                if grid.getCellValue(cursor) - grid.getCellValue(prev) >= 0 and (math.log(grid.getCellValue(cursor), 2) - math.log( grid.getCellValue(prev), 2)) <= 2:
                    sum_mono1 +=  math.log( grid.getCellValue(prev), 2)
                    if math.log(grid.getCellValue(cursor), 2) - math.log( grid.getCellValue(prev), 2) <= 1:
                        pass
                else:
                    break

            sum_mono2 = 0

            x_dir = xy_dir[0]
            y_dir = xy_dir[1]

            cursor = deepcopy(max_pos)
            history = []
            for i in xrange(1, grid.size * 2):
                history.append((cursor,i))  
                prev = deepcopy(cursor)
                if grid.getCellValue(cursor) == 0:
                    break
                if i % 4 == 0:
                    cursor = (cursor[0] + x_dir, cursor[1])
                    y_dir = -1 * y_dir
                else:
                    cursor = (cursor[0], cursor[1] + y_dir)
                if grid.getCellValue(cursor) - grid.getCellValue(prev) >= 0:
                    sum_mono2 += math.log( grid.getCellValue(prev), 2)
                    if math.log(grid.getCellValue(cursor), 2) - math.log( grid.getCellValue(prev), 2) <= 1:
                        pass
                else:
                    break

            sum_mono = sum_mono + max(sum_mono1, sum_mono2)

        return sum_mono


    def get_smoothness(self, grid):
        tiles = []
        for i in xrange(0, grid.size):
            for j in xrange(0, grid.size):
                if grid.map[i][j] > 0:
                    tiles.append((i, j))
        smoothness = 0

        for i, t in enumerate(tiles):
            for j in xrange(i+1, len(tiles)):
                if math.log(grid.getCellValue(t), 2) - math.log(grid.getCellValue(tiles[j]), 2) == 0 and math.log(grid.getCellValue(t), 2):
                    if abs(t[0] - tiles[j][0]) + abs(t[1] - tiles[j][1]) == 1:
                        smoothness += 1 * math.log(grid.getCellValue(t), 2)/5
                        continue

        for i, t in enumerate(tiles):
            for j in xrange(i+1, len(tiles)):
                if math.log(grid.getCellValue(t), 2) - math.log(grid.getCellValue(tiles[j]), 2) == 1 and math.log(grid.getCellValue(t), 2):
                    if abs(t[0] - tiles[j][0]) + abs(t[1] - tiles[j][1]) == 1:
                        smoothness += 0.5 * max(math.log(grid.getCellValue(t), 2), math.log(grid.getCellValue(tiles[j]), 2))/5
                        continue

        return smoothness

    def get_smoothness2(self, grid):
        queue = Queue.PriorityQueue(100)
        for i in xrange(0, grid.size):
            for j in xrange(0, grid.size):
                if grid.map[i][j] > 0:
                    queue.put((20 - grid.map[i][j], (i, j)))
        tiles = []
        smoothness = 0
        while not queue.empty():
            tiles.append(queue.get()[1])

        for i in xrange(1, min(len(tiles), 8)):
            if abs(tiles[i-1][0] - tiles[i][0]) + abs(tiles[i][1] - tiles[i-1][1]) == 1:
                smoothness += math.log(grid.getCellValue(tiles[i]), 2)
        return smoothness

        
















       