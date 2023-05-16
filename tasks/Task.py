#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Task base class
    method: to_task
            - is called dynamically
            - modifies cell(s)
            - parameter cell on mouse click on cell
            - otherwise get_random_cell
'''

__description__ = 'Task (used as super class for further tasks)'
__version__ = '1.0.4'
__author__ = 'Stephan Metzler'

import sys
import random
import numpy as np
from abc import ABCMeta, abstractmethod

sys.path.append('../')  # search moduls in parent folder too
from cells.Cells import *
from utils.Decorator import log


class Task(metaclass=ABCMeta):
    ''' task  base class '''
    cell_modules = __import__('cells.Cells')  # all cell objects
    counter = 0  # access counter (used as class attribute)

    def __init__(self, cells):
        ''' constructor '''
        self.cells = cells  # cells as [[]]
        self.__class__.counter += 1  # increase class access counter

    @abstractmethod  # sub classes must implement this method
    def do_task(self, cell=None):
        ''' do task > manipulate cell(s)
            - parameter cell:
              - mouse click on cell
              - otherwise get_random_cell()
            - modify cell(s)
            - update() if cell instance changes
            - no return
        '''

    def get_random_cell(self, cell=None):
        ''' return a random cell (of type if specified) '''
        if cell is None:  # get any random cell
            return random.choice(random.choice(self.cells))  # random cell
        else:  # check if the requested cell is in cells
            types = [type(c) for row in self.cells for c in row]  # all types
            contains = np.isin(types, cell)  # contains cell 
            if not contains.any():  # cell not found
                return None
        while True:  # get requested random cell
            random_cell = random.choice(random.choice(self.cells))
            if random_cell.__class__.__name__ == cell.__name__:
                break  # requested cell found
        return random_cell

    def get_neighbor_cell(self, cell):
        ''' get ramdom neighbor cell '''
        h, v = row, col = cell.get_row_col()  # get cordinates
        while (h, v) == (row, col):  # get random neighbor but not itself
            h = random.choice(range(max(0, row - 1),
                                    min(len(self.cells), row + 2)))
            v = random.choice(range(max(0, col - 1),
                                    min(len(self.cells[0]), col + 2)))
        return self.cells[h][v]
    def get_neighbor_cell_direction(self, cell, directions):
        ''' get neighbor cell based on specified direction '''
        row, col = cell.get_row_col()  # get coordinates
        # define movements
        movements = {
            'up': (-1, 0),
            'left': (0, -1),
            'right': (0, 1),
            'down': (1, 0)
        }

        possible_neighbors = []
        for direction in directions:
            if direction in movements:
                h = (row + movements[direction][0]) % len(self.cells)
                v = (col + movements[direction][1]) % len(self.cells[0])
                possible_neighbors.append(self.cells[h][v])

        if possible_neighbors:
            return random.choice(possible_neighbors)
        else:
            return None  # no valid neighbors

    def swap(self, cell, other):
        self.__dict__, other.__dict__ = other.__dict__, self.__dict__
        self.update(cell)
        self.update(other)

    def update(self, cell):
        ''' update cell in cells - use when instance of cell changes '''
        row, col = cell.get_row_col()
        self.cells[row][col] = cell

    def __str__(self):
        ''' built-int str() method to return a string representation '''
        return self.__class__.__name__  # return task name


if __name__ == '__main__':  # test only
    size = 30
    # get all cell sub classes
    all_cells = Cell.__subclasses__()
    print('cell sub class definitions:')
    for cell in all_cells:
        print(' ', cell)
    # random burnable cells
    burnable_cells = [cell for cell in all_cells if cell.burnable]
    cells = [[random.choice(burnable_cells)(row, col)
              for col in range(size)]
             for row in range(size)]
    print('\nnumber of random generated cells:', len(cells) * len(cells[0]))

    # task = Task() > is not possible > need to create sub class first
    class MyTask(Task):  # must inheritance Task ...
        ''' simulate task '''
        @log
        def do_task(self, cell):  # ... and implement method do_task
            ''' do task '''
            cell.index += 1  # cell should increase index
            cell + 1  # also works, cell index is now 2 -> see log file
            cell + cell  # also ok: cell index is now 4
            '''
            cell += 1  be careful: += is no magic method
                       also changes type of cell, cell is now type int
            '''

    class SimulateTask:
        ''' simulate task '''

        def call_task(self):
            ''' call the task '''
            task_instance = MyTask(cells)  # now instantion is possible
            cell = task_instance.get_random_cell()
            task_instance.do_task(cell)  # do the task
            print(f'cell with increased index: {cell!r}')  # !r > use __repr__
            # test counter
            for i in range(10):
                task = MyTask(cells)
            print(f'{task} called {MyTask.counter} times')  # class attr.

    SimulateTask().call_task()  # do task

    # test neighbor
    task = MyTask(cells)
    random_cell = task.get_random_cell()
    neighbor = task.get_neighbor_cell(random_cell)
    print(f'neighbor of {random_cell!r} is {neighbor!r}')
    # test swap
    random_cell.swap(neighbor)  # swap two cells
    task.update(random_cell)  # update cells
    task.update(neighbor)  # update cells
    # test specific random cell
    forest = task.get_random_cell(Forest)  # use class name
    print('should be Forest only:', forest)

    # test specific random cell but cells are only burnable cells
    hole = task.get_random_cell(Hole)  # use class name
    print('should be Hole only:', hole)  # None found > Hole does not burn
