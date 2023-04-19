#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' task: FishFight
    fish swim in water, grow while swimmig, eat and get eaten
    - when fish meet, the bigger one wins
    - the size of its prey is added to the own size
    index:           size of fish
    span_index       fish spawns on index > span_index

    number_of_spans  number of new fish '''

__description__ = 'fish swim in water, grow while swimmig, eat and get eaten'
__author__ = 'Stephan Metzler'

import sys
import random
import copy
sys.path.append('../')  # search moduls in parent folder too

from cells.Cells import *
from tasks.Task import Task
from scenes.Scenes import Scenes


class FishFight(Task):
    ''' simulates fish fight '''
    spawn_index = 100  # fish spawns on index > 100
    number_of_spawn = 10  # number of new fish

    def do_task(self, cell=None):
        ''' do the task > manipulate cells '''
        if cell is None:  # if not cell clicked by mouse
            cell = self.get_random_cell(Fish)  # want a fish only to ..
        if isinstance(cell, Fish):  # it's a Fish
            neighbor = self.get_neighbor_cell(cell)  # get a random neighbor
            if cell.get_index() > self.spawn_index:
                new_fish = []
                for i in range(self.number_of_spawn):
                    water = self.get_random_cell(Water)
                    fish = water.mutate_to(Fish)  # mutate to fish
                    new_fish.append(fish)  # add to lust
                    self.update(fish)  # update (new) cell
                water = cell.mutate_to(Water)  # old fish dies now
                self.update(water)  # update cell
                new_fish.append(water)  # cell also changed
            elif isinstance(neighbor, Water):  # .. move
                cell.swap(neighbor)  # swap -> fish moves
                cell.set_index(neighbor.get_index())  # keep index
                neighbor.set_index(0)  # reset water index
                cell + 1  # grow while swimming
                self.update(cell)  # update (new) cell
                self.update(neighbor)  # update (new) neighbor
            elif isinstance(neighbor, Fish):  # meet other fish
                if neighbor <= cell:  # prey
                    cell + neighbor  # eat
                    neighbor = neighbor.mutate_to(Water)  # back to water
                else:
                    neighbor + cell  # get eaten
                    cell = cell.mutate_to(Water)  # back to water
                self.update(cell)  # update (new) cell
                self.update(neighbor)  # update (new) neighbor


if __name__ == '__main__':  # test only
    print('''
    test FishFight
    - fish swim in the water, grow while swimmig, eat and get eaten
    - when they meet, the bigger one wins and adds the size of its prey
    ''')
    CELLS = 30  # scene with 900 cells
    FIGHTS = 10  # do the task 30 times
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    cells = Cell.__subclasses__()
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)
    # generate random cells
    cells = [[random.choice(cells)(row, col)
              for col in range(CELLS)]
             for row in range(CELLS)]
    print('# random cells:', len(cells) * len(cells[0]))
    # simulate FishFight
    fishFight = FishFight(cells)  # get task
    fish = fishFight.get_random_cell(Fish)  # get a fish
    row, col = fish.get_row_col()  # get row and col
    for i in range(FIGHTS):
        cell = copy.copy(fish)  # copy to cell
        fishFight.do_task(fish)  # do task
        if not cell == cells[row][col]:  # on changed cell
            print(f'{fishFight} on {cell!r} effects {fish!r} and {cells[row][col]!r}')
    # test magic methods
    other_fish = fishFight.get_random_cell(Fish)  # get a fish
    fish + 5  # magic method __add__
    other_fish + 3  # be carfull! += is not suported as magic method
    fish + other_fish  # add index of other_fish to fish
    print(f'{fish!r} is bigger than {other_fish!r}:', fish > other_fish)
    # test move
    water = fishFight.get_random_cell(Water)  # get water
    print(f'fish and water: {fish!r} - {water!r}')
    fish.swap(water)  # swap
    print(f'swapped       : {fish!r} - {water!r}')
