__description__ = 'cells turn to Trees and return the Jungle\nbe careful using palm oil'
__author__ = 'Stephan Metzler'

import sys
import random

sys.path.append('../')  # search modules in parent folder too

from cells.Cells import *
from tasks.Task import Task


class PlantLifeReturning(Task):
    ''' simulates forest grow '''

    def do_task(self, cell=None):
        ''' mutate any cell to tree or plants
            grow if tree '''
        if not cell:
            cell = self.get_random_cell()  # use any cell

        if isinstance(cell, Tree):  # grow
            cell + 1  # keep aging - magic method __add__
        elif isinstance(cell, Dirt):
            prob = random.random()
            if prob < 0.4:
                tree = cell.mutate_to(Tree)
                self.update(tree)
            elif 0.4 <= prob < 0.80:
                plants = cell.mutate_to(Plants)
                self.update(plants)

if __name__ == '__main__':  # test only
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)
    CELLS = 30
    RUNS = 1000

    def count_trees(cells):
        trees = 0
        grow = 0
        for row in cells:
            for cell in row:
                if isinstance(cell, Tree):
                    trees += 1
                    grow += cell.get_index()
        return trees, grow  # return as tuple

    # simulate PlantLifeReturning
    plantLifeReturning = PlantLifeReturning(cells)
    print(f'simulate {RUNS} runs of {plantLifeReturning}')
    print(f' - starting with {count_trees(cells)[0]} trees')
    for run in range(RUNS):
        plantLifeReturning.do_task()
    trees, grow = count_trees(cells)  # return tuple
    print(f' - produced {trees} trees and {grow} grow index')