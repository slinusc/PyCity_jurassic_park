#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' to do: expand and experiment
    delete this task as it is destroying your scenery '''

__description__ = 'cells turn to Forests an return the Jungle\nbe carful using palm oil'
__author__ = 'Stephan Metzler'

import sys

sys.path.append('../')  # search moduls in parent folder too

from cells.Cells import *
from tasks.Task import Task


class JungleReturning(Task):
    ''' simulates forest grow '''

    def do_task(self, cell=None):
        ''' mutate any cell to Forest
            grow if Forest '''
        if not cell:
            cell = self.get_random_cell()  # use any cell
        if isinstance(cell, Forest):  # grow
            cell + 1  # keep aging - magic method __add__
        else:
            Forest = cell.mutate_to(Forest)  # and let a Forest grow
            self.update(Forest)  # update cells


if __name__ == '__main__':  # test only
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)
    CELLS = 30
    RUNS = 1000
    # generate lots of Holes
    cells = [[Hole(row, col)
              for col in range(CELLS)]
             for row in range(CELLS)]
    print('lots of holes:', len(cells) * len(cells[0]))

    def count_Forests(cells):
        Forests = 0
        grow = 0
        for row in cells:
            for cell in row:
                if isinstance(cell, Forest):
                    Forests += 1
                    grow += cell.get_index()
        return Forests, grow  # return as tupel

    # simulate JungleReturning
    jungleReturning = JungleReturning(cells)
    print(f'simulate {RUNS} runs of {jungleReturning}')
    print(f' - starting with {count_Forests(cells)[0]} Forests')
    for run in range(RUNS):
        jungleReturning.do_task()
    Forests, grow = count_Forests(cells)  # return tupel
    print(f' - produced {Forests} Forests and {grow} grow index')
