#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' task: Fire Blace
    change burnable cell after AGE_INDEX: Fire > Chark > Tree > Fire ... '''

__description__ = 'change burnable cell after AGE_INDEX to\n ... Fire > Chark > Tree > Fire ...'
__author__ = 'Stephan Metzler'

import sys
import random
sys.path.append('../')  # search moduls in parent folder too

from cells.Cells import *
from tasks.Task import Task


class FireBlaze(Task):
    ''' simulates fire blaze - a burnable cell changes after AGE_INDEX:
        Cell > Fire > Chark > Tree > Chark > Tree ... '''

    AGE_INDEX = 3  # index after cell changes

    def do_task(self, cell=None):
        ''' do the task > only manipulate one cell at time and
            return manipulated cell or None '''
        def change_cell_on_age_index(cell):
            ''' age cell and change after AGE_INDEX '''
            if cell.index >= self.AGE_INDEX:  # reached age index
                if isinstance(cell, Fire):  # still burning
                    cell = cell.mutate_to(Chark)  # burned out
                elif isinstance(cell, Chark):  # stoped burning
                    cell = cell.mutate_to(Tree)  # recover
                else:  # burnable cell
                    cell = cell.mutate_to(Fire)  # catch fire
                self.cells[cell.row][cell.col] = cell  # update cells
            else:
                cell.index += 1  # keep aging
        if cell is None:  # get a cell if not provided
            cell = self.get_random_cell()  # get random cell
        if cell.burnable:  # only burnable cells
            cell = change_cell_on_age_index(cell)  # change after AGING


if __name__ == '__main__':  # test only
    print('''
    test FireBlaze
    - change burnable cell on AGE index: Fire > Chark > Tree >
    ''')
    CELLS = 30  # number of cells
    CALLS = 12  # number of tasks
    burable_cells = [c for c in Cell.__subclasses__() if c.burnable]
    build_cell_from = burable_cells + [Water, Rock]  # add Water and Rock
    cell_names = [cell.__name__ for cell in build_cell_from]
    cells = [[random.choice(build_cell_from)(row, col)
              for col in range(CELLS)]
             for row in range(CELLS)]
    print(f'{len(cells) * len(cells[0])} \
          cells on random scene with {cell_names}')

    class SimulateTask:  # simulate task
        ''' simulate fire blaze '''
        @classmethod
        def call_task(self):
            ''' call the task '''
            task = FireBlaze(cells)
            cell = task.get_random_cell(Tree)
            row, col = cell.get_row_col()
            print(f'get random cell: {cells[row][col]!r} \
                  and call {CALLS} times {task} ')
            for i in range(1, CALLS + 1):  # index based: Fire > Chark > Tree >
                task.do_task(cells[row][col])
                print(f'{i:02}. {task} results in {cells[row][col]!r}')

    SimulateTask.call_task()
