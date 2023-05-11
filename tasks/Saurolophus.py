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
                cell = cell.mutate_to(Dirt)  # back to dirt
            elif not (isinstance(neighbor, Water) or isinstance(neighbor, Mountain)):
                previous_state = cell.get_state()  # save current state before moving
                cell.swap(neighbor)  # swap -> Parasaurolophus moves
                cell.set_index(neighbor.get_index())  # keep index
                neighbor.set_state(previous_state)  # restore previous state
                neighbor.set_index(0)  # reset dirt index
                self.update(cell)  # update (new) cell
                self.update(neighbor)  # update (new) neighbor
            self.update(cell)  # update (new) cell
            self.update(neighbor)  # update (new) neighbor



if __name__ == '__main__':  # test only
    print('''
    test Saurolophus
    - parasaurolophus walk on land, eat plants, and interact with other dinosaurs
    ''')
    CELLS = 30  # scene with 900 cells
    STEPS = 10  # do the task 10 times
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    cells = Cell.__subclasses__()
    all_cells = [cell.__name__ for cell in
    Cell.__subclasses__()]
    print('cells:', *all_cells)
    # generate random cells
    cells = [[random.choice(cells)(row, col)
              for col in range(CELLS)]
             for row in range(CELLS)]
    print('# random cells:', len(cells) * len(cells[0]))
    # simulate Saurolophus
    paraBehavior = Saurolophus(cells)  # get task
    para = paraBehavior.get_random_cell(Parasaurolophus)  # get a parasaurolophus
    row, col = para.get_row_col()  # get row and col
    for i in range(STEPS):
        cell = copy.copy(para)  # copy to cell
        paraBehavior.do_task(para)  # do task
        if not cell == cells[row][col]:  # on changed cell
            print(f'{paraBehavior} on {cell!r} effects {para!r} and {cells[row][col]!r}')
    # test magic methods
    other_para = paraBehavior.get_random_cell(Parasaurolophus)  # get a parasaurolophus
    para + 5  # magic method __add__
    other_para + 3  # be careful! += is not supported as magic method
    para + other_para  # add index of other_para to para
    print(f'{para!r} is bigger than {other_para!r}:', para > other_para)
    # test move
    dirt = paraBehavior.get_random_cell(Dirt)  # get dirt
    print(f'para and dirt: {para!r} - {dirt!r}')
    para.swap(dirt)  # swap
    print(f'swapped       : {para!r} - {dirt!r}')

