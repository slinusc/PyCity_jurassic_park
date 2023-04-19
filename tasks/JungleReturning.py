#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' to do: expand and experiment
    delete this task as it is destroying your scenery '''

__description__ = 'cells turn to Trees an return the Jungle\nbe carful using palm oil'
__author__ = 'Stephan Metzler'

import sys

sys.path.append('../')  # search moduls in parent folder too

from cells.Cells import *
from tasks.Task import Task


class JungleReturning(Task):
    ''' simulates forest grow '''

    def do_task(self, cell=None):
        ''' mutate any cell to tree
            grow if tree '''
        if not cell:
            cell = self.get_random_cell()  # use any cell
        if isinstance(cell, Tree):  # grow
            cell + 1  # keep aging - magic method __add__
        else:
            tree = cell.mutate_to(Tree)  # and let a tree grow
            self.update(tree)  # update cells


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

    def count_trees(cells):
        trees = 0
        grow = 0
        for row in cells:
            for cell in row:
                if isinstance(cell, Tree):
                    trees += 1
                    grow += cell.get_index()
        return trees, grow  # return as tupel

    # simulate JungleReturning
    jungleReturning = JungleReturning(cells)
    print(f'simulate {RUNS} runs of {jungleReturning}')
    print(f' - starting with {count_trees(cells)[0]} trees')
    for run in range(RUNS):
        jungleReturning.do_task()
    trees, grow = count_trees(cells)  # return tupel
    print(f' - produced {trees} trees and {grow} grow index')
