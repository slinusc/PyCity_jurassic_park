#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' task: Brachiosaurus
    Brachiosaurus walk on land, eat and get eaten
    - when Brachiosaurus meet, they may reproduce
'''

__description__ = 'Brachiosaurus walk on land, eat Forest, and interact with other dinosaurs'
__author__ = 'Andrés Mock'

import sys
import copy
import random
sys.path.append('../')

from cells.Cells import *
from tasks.Task import Task



class BrachiosaurusLife(Task):
    ''' simulates brachiosaurus behavior '''
    def do_task(self, cell=None):
        ''' do the task > manipulate cells '''
        if cell is None:  # if not cell clicked by mouse
            cell = self.get_random_cell(Brachiosaurus)  # want a Brachiosaurus only to ..
        if isinstance(cell, Brachiosaurus):  # it's a Brachiosaurus
            neighbor = self.get_neighbor_cell(cell)  # get a random neighbor
            if isinstance(neighbor, Forest):  # eat forest
                cell.swap(neighbor)
                neighbor = neighbor.mutate_to(Trunk)  # back to grass
                self.update(cell)
                self.update(neighbor)
            elif isinstance(neighbor, Brachiosaurus):  # meet another Brachiosaurus
                for _ in range(2):
                    empty_cell = self.get_random_cell(Plants)
                    prob = random.random()
                    if (prob < 0.1):
                        new_brachio = empty_cell.mutate_to(Brachiosaurus)
                        self.update(new_brachio)
            elif isinstance(neighbor, Trex):
                cell = cell.mutate_to(Grass)
                self.update(cell)
            elif not isinstance(neighbor, (Water, Mountain, Fence)):
                cell.swap(neighbor)
                cell.set_index(neighbor.get_index())
                neighbor.set_index(0)
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
    grass = brachioBehavior.get_random_cell(Grass)  # get grass
    print(f'brachio and grass: {brachio!r} - {grass!r}')
    brachio.swap(grass)  # swap
    print(f'swapped       : {brachio!r} - {grass!r}')
