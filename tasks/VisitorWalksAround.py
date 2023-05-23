#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' task: Visitor
    Visitor walks on Path only
    - when Visitor meet Brachiosaurus, Trex, or Parasaurolophus, they turn into Path
    walks only left, right or up
'''

__description__ = 'Visitor walks on Path and  dies when he meets dinosaurs'
__author__ = 'Linus Stuhlmann'

import sys
import copy
sys.path.append('../')

from cells.Cells import *
from tasks.Task import Task

class VisitorWalksAround(Task):
    ''' simulates visitor behavior '''
    def do_task(self, cell=None):
        ''' do the task > manipulate cells '''
        if cell is None:  # if not cell clicked by mouse
            cell = self.get_random_cell(Visitor)  # want a Visitor only to ..
        if isinstance(cell, Visitor):  # it's a Visitor
            neighbor = self.get_neighbor_cell_direction(cell, ["up", "left", "right"])  # get a random neighbor
            if isinstance(neighbor, (Brachiosaurus, Trex, Parasaurolophus)):  # meet a dinosaur
                cell = cell.mutate_to(Path)  # transform into Path
                self.update(cell)
            elif isinstance(neighbor, Path):
                cell.swap(neighbor)
                self.update(cell)
                self.update(neighbor)


if __name__ == '__main__':  # test only
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)
    CELLS = 30
    RUNS = 1000

    def count_Visitors_Dinos(cells):
        visitors = 0
        dinos = 0
        for row in cells:
            for cell in row:
                if isinstance(cell, Visitor):
                    visitors += 1
                elif isinstance(cell, (Trex, Brachiosaurus, Parasaurolophus)):
                    dinos += 1
        return visitors, dinos  # return as tuple

    # simulate VisitorWalksAround
    cells = [[random.choice([Path(row, col), Visitor(row, col), Trex(row, col), Brachiosaurus(row, col), Parasaurolophus(row, col)]) for col in range(CELLS)] for row in range(CELLS)]
    visitorWalksAround = VisitorWalksAround(cells)
    print(f'simulate {RUNS} runs of {visitorWalksAround}')
    print(f' - starting with {count_Visitors_Dinos(cells)[0]} Visitors and {count_Visitors_Dinos(cells)[1]} Dinosaurs')
    for run in range(RUNS):
        visitorWalksAround.do_task()
    visitors, dinos = count_Visitors_Dinos(cells)  # return tuple
    print(f' - ended with {visitors} Visitors and {dinos} Dinosaurs')