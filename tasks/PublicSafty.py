#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' to do: implement task '''

__description__ = '... '  # complete
__author__ = '...'  # complete

import sys
import random
sys.path.append('../')  # search moduls in parent folder too

from cells.Cells import *
from tasks.Task import Task


class PublicSafty(Task):
    ''' simulates dynamic economy '''

    def do_task(self, cell=None):
        ''' do task > manipulate cell(s)
            - parameter cell:
              - mouse click on cell
              - otherwise get_random_cell()
            - modify cell(s)
            - update() if cell instance changes
            - no return
        '''
        print('method do_task called', flush=True)  # flush prints!


if __name__ == '__main__':  # test only
    CELLS = 30
    all_cells = Cell.__subclasses__()
    cell_names = [cell.__name__ for cell in all_cells]
    print('all cells:', *cell_names)
    # generate random cells
    cells = [[random.choice(all_cells)(row, col)
              for col in range(CELLS)]
             for row in range(CELLS)]
    # task
    task_class = Task.__subclasses__()[0]  # only one subclass here
    task = task_class(cells)  # get the task
    print(f'do {task} with {len(cells) * len(cells[0])} random cells')
    # do the task
    task.do_task()
    print('\n >> your turn now ... ')
