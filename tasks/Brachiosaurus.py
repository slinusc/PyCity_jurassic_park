#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' task: Brachiosaurus
    Brachiosaurus walk on land, eat and get eaten
    - when Brachiosaurus meet, they may reproduce
    - when Brachiosaurus meet trex, 50% chance to die
    index:           size of dinosaur
'''

__description__ = 'Brachiosaurus walk on land, eat Trees, and interact with other dinosaurs'
__author__ = 'Obermühlner'

import sys
import random
import copy
sys.path.append('../')  # search moduls in parent folder too

from cells.Cells import *
from tasks.Task import Task
from scenes.Scenes import Scenes



class Brachiosaurus(Task):
    ''' simulates brachiosaurus behavior '''

    def do_task(self, cell=None):
        if cell is None:
            cell = self.get_random_cell(Brachiosaurus)
        if isinstance(cell, Brachiosaurus):
            neighbor = self.get_neighbor_cell(cell)
            if isinstance(neighbor, Tree):
                cell + neighbor
                neighbor = neighbor.mutate_to(Dirt)
            elif isinstance(neighbor, Brachiosaurus):
                if random.random() < 0.5:
                    dirt = self.get_random_cell(Dirt)
                    new_brachio = dirt.mutate_to(Brachiosaurus)
                    self.update(new_brachio)
            elif isinstance(neighbor, Parasaurolophus):
                if random.random() < 0.5:
                    neighbor = neighbor.mutate_to(Dirt)
            elif isinstance(neighbor, Trex):
                if random.random() < 0.5:
                    cell = cell.mutate_to(Dirt)
            elif not (isinstance(neighbor, Water) or isinstance(neighbor, Mountain)):
                temp_cell = copy.deepcopy(cells[neighbor.get_row()][neighbor.get_col()])
                cells[neighbor.get_row()][neighbor.get_col()] = copy.deepcopy(cells[cell.get_row()][cell.get_col()])
                cells[cell.get_row()][cell.get_col()] = temp_cell

                cell.set_row_col(neighbor.get_row(), neighbor.get_col())

                self.update(cell)
                self.update(neighbor)
            self.update(cell)
            self.update(neighbor)


if __name__ == '__main__':  # test only
    print('''
    test Brachiosaurus
    - brachiosaurus walk on land, eat plants, and interact with other dinosaurs
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
    # simulate Brachiosaurus
    brachioBehavior = Brachiosaurus(cells)  # get task
    brachio = brachioBehavior.get_random_cell(Brachiosaurus)  # get a brachiosaurus
    row, col = brachio.get_row_col()  # get row and col
    for i in range(STEPS):
        cell = copy.copy(brachio)  # copy to cell
        brachioBehavior.do_task(brachio)  # do task
        if not cell == cells[row][col]:  # on changed cell
            print(f'{brachioBehavior} on {cell!r} effects {brachio!r} and {cells[row][col]!r}')
    # test magic methods
    other_brachio = brachioBehavior.get_random_cell(Brachiosaurus)  # get a brachiosaurus
    brachio + 5  # magic method __add__
    other_brachio + 3  # be careful! += is not supported as magic method
    brachio + other_brachio  # add index of other_brachio to brachio
    print(f'{brachio!r} is bigger than {other_brachio!r}:', brachio > other_brachio)
    # test move
    dirt = brachioBehavior.get_random_cell(Dirt)  # get dirt
    print(f'brachio and dirt: {brachio!r} - {dirt!r}')
    brachio.swap(dirt)  # swap
    print(f'swapped       : {brachio!r} - {dirt!r}')
