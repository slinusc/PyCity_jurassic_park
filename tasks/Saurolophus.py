#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' task: parasaurolophus
    parasaurolophus walk on land, eat and get eaten
    - when parasaurolophus meet, they may reproduce
    - when parasaurolophus meet trex, 50% chance to die
    index:           size of dinosaur
'''

__description__ = 'parasaurolophus walk on land, eat plants, and interact with other dinosaurs'
__author__ = 'Stephan Metzler'

import sys
import random
import copy
sys.path.append('../')  # search moduls in parent folder too

from cells.Cells import *
from tasks.Task import Task
from scenes.Scenes import Scenes


class Saurolophus(Task):
    ''' simulates parasaurolophus behavior '''

    def do_task(self, cell=None):
        ''' do the task > manipulate cells '''
        if cell is None:  # if not cell clicked by mouse
            cell = self.get_random_cell(Parasaurolophus)  # want a parasaurolophus only to ..
        if isinstance(cell, Parasaurolophus):  # it's a Parasaurolophus
            neighbor = self.get_neighbor_cell(cell)  # get a random neighbor
            if isinstance(neighbor, Plants):  # eat plants
                cell + neighbor  # grow
                neighbor = neighbor.mutate_to(Dirt)  # back to dirt
            elif isinstance(neighbor, Parasaurolophus):  # meet another parasaurolophus
                if random.random() < 0.5:  # 50% chance to reproduce
                    dirt = self.get_random_cell(Dirt)
                    new_para = dirt.mutate_to(Parasaurolophus)  # mutate to parasaurolophus
                    self.update(new_para)  # update (new) cell
            elif isinstance(neighbor, Trex):  # meet trex
                if random.random() < 0.5:  # 50% chance to die
                    cell = cell.mutate_to(Dirt)  # back to dirt
            else:
                cell.swap(neighbor)  # swap -> parasaurolophus moves
                cell.set_index(neighbor.get_index())  # keep index
                neighbor.set_index(0)  # reset dirt index
                self.update(cell)  # update (new) cell
                self.update(neighbor)  # update (new) neighbor
            self.update(cell)  # update (new) cell
            self.update(neighbor)  # update (new) neighbor


if __name__ == '__main__':  # test only
    print('''
    test ParasaurolophusBehavior
    - parasaurolophus walk on land, eat plants, and interact with other dinosaurs
    ''')
    CELLS = 30  # scene with 900 cells
    STEPS = 10  # do the task 10 times
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    cells = Cell.__subclasses__()
    all_cells = [cell.__name__ for cell in
