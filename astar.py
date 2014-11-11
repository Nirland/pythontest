#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementation pathfinding A*
"""

from Queue import PriorityQueue


class Cell(object):
    def __init__(self, x, y, reachable):
        self.x = x
        self.y = y
        self.reachable = reachable

        self.parent = None

        self.tostart = 0
        self.heuristic = 0
        self.distance = 0

    def __eq__(self, cell):
        return (isinstance(cell, Cell) and
                (self.x == cell.x and self.y == cell.y))


class AStar(object):
    def __init__(self, height=10, width=10,
                 start=(0, 0), target=(9, 9), walls=()):
        self.height = height
        self.width = width
        try:
            self.height = int(self.height)
            self.width = int(self.width)
        except ValueError:
            self.height = 10
            self.width = 10

        self.cells = []
        self.path = []
        self.opened = PriorityQueue()
        self.closed = set()

        for x in xrange(self.height):
            for y in xrange(self.width):
                if (x, y) in walls:
                    cell = Cell(x, y, False)
                else:
                    cell = Cell(x, y, True)
                self.cells.append(cell)

        self.start = self.get_cell(start[0], start[1])
        self.target = self.get_cell(target[0], target[1])

    def get_cell(self, x, y):
        return self.cells[x * self.width + y]

    def get_heuristic(self, cell):
        return abs(cell.x - self.target.x) + abs(cell.y - self.target.y)

    def get_children(self, cell):
        children = []
        if ((cell.x > 0) and (self.get_cell(cell.x-1, cell.y).reachable)):
            children.append(self.get_cell(cell.x-1, cell.y))

        if ((cell.x < self.width-1) and
                (self.get_cell(cell.x+1, cell.y).reachable)):
            children.append(self.get_cell(cell.x+1, cell.y))

        if ((cell.y > 0) and (self.get_cell(cell.x, cell.y-1).reachable)):
            children.append(self.get_cell(cell.x, cell.y-1))

        if ((cell.y < self.height-1) and
                (self.get_cell(cell.x, cell.y+1).reachable)):
            children.append(self.get_cell(cell.x, cell.y+1))
        return children

    def update_cell(self, cell, parent):
        cell.tostart = parent.tostart + 1
        cell.heuristic = self.get_heuristic(cell)
        cell.distance = cell.tostart + cell.heuristic
        cell.parent = parent
        return cell

    def create_path(self):
        cell = self.target
        if cell.parent is None:
            return
        while cell.parent is not self.start:
            cell = cell.parent
            self.path.append((cell.x, cell.y))
        return self.path

    def find_path(self):
        self.opened.put((0, self.start))
        while self.opened.qsize:
            cell = self.opened.get()[1]
            self.closed.add(cell)

            if (cell is self.target):
                return self.create_path()

            children = self.get_children(cell)
            for child in children:
                if child not in self.closed:
                    if (child.distance, child) in self.opened.queue:
                        if (child.parent.tostart > cell.tostart):
                            self.update_cell(child, cell)
                    else:
                        self.update_cell(child, cell)
                        self.opened.put((child.distance, child))


###========================================================================
###========================================================================
###========================================================================


if __name__ == "__main__":
    walls = ((2, 3), (3, 3), (3, 4), (3, 5), (2, 5),
            (1, 8), (1, 7), (1, 6), (2, 6),
            (2, 9), (5, 9),
            (6, 8), (5, 8), (4, 8), (4, 7),
            (4, 6), (4, 5), (4, 4),
            (3, 2), (3, 3),
            (7, 9), (7, 8), (7, 7), (7, 6),
            (5, 5), (6, 6))
    start = (0, 0)
    target = (9, 9)
    astar = AStar(start=start, target=target, walls=walls)
    result = astar.find_path()
    print result
