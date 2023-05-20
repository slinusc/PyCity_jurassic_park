#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' basic application contains a surface of 30 x 30 fields
    each field contains a typical city structure:
    - land, water, house, business, street, car, person, etc.

    the fields are subclasses of Cell and contain
    - color: String (RGB as HEX) e.g. "#FF0000"  > red
    - index: int (e.g. increment on task)

    to do: add your own Fields and individual properties (e.g. burnable) '''

__description__ = 'Cells inherit from Cell - compose your own '
__version__ = '1.0.4'
__author__ = 'Stephan Metzler'
__email__ = 'metl@zhaw.ch'
__status__ = 'build your way to extraordinary'

import random
import csv
from math import sqrt
import json
import inspect


class Cell():
    ''' cell with row, col, index and color
        - row, col: cell position in (GUI) grid
        - index: e.g. increases with time (on do_task)
        - color: displayed color in GUI
        - more individuel attributes ... '''
    row = col = -1
    index = 0
    color = "#000000"  # RGB (red green blue) > all 0 > black
    burnable = False
    state = None
  #  previous_type = None



    def __init__(self, row=-1, col=-1):  # -1 for void
        ''' constructor '''
        self.row = row
        self.col = col

    def get_previous_type(self):
        return self.previous_type

    def set_previous_type(self, previous_type):
        self.previous_type = previous_type


    def get_state(self):
        ''' return cell index '''
        return self.state

    def set_state(self, state):
        ''' return cell index '''
        self.state = state


    def get_color(self):
        ''' return cell color '''
        return self.color

    def get_index(self):
        ''' return cell index '''
        return self.index

    def get_row_col(self):
        ''' return cell row and col as tupel '''
        return self.row, self.col  # index as tupel

    def set_index(self, index):
        ''' set index '''
        self.index = index

    def set_row_col(self, row_col):  # parameter as tupel
        ''' set cell row and col with parameter as tupel (row, col) '''
        self.row = row_col[0]
        self.col = row_col[1]

    def swap(self, other):
        ''' swap to cells '''
        self.__dict__, other.__dict__ = other.__dict__, self.__dict__

    def mutate_to(self, other):
        ''' returns mutated cell '''
        return other(self.row, self.col)

    def is_dark(self):
        ''' return cell color brithness as True|False '''
        return sqrt(0.299 * pow(int(self.color[1:3], 16), 2)
                    + 0.587 * pow(int(self.color[3:5], 16), 2)
                    + 0.114 * pow(int(self.color[5:7], 16), 2)) > 127

    def is_burnable(self):
        ''' return cell inflammability as True|False '''
        return self.burnable

    def __eq__(self, other):
        ''' return comparison using == on cell objects '''
        return self.__dict__ == other.__dict__

    def __add__(self, other):
        ''' called on cell add operation using +
            - add int if other is int, e.g. cell + 1
            - cell index otherwise, e.g.: cell + other (cell) '''
        self.index += other if isinstance(other, int) else other.index

    def __lt__(self, other):
        ''' return comparison using < on index '''
        return self.index < other.index

    def __le__(self, other):
        ''' return comparison using <= on index '''
        return self.index <= other.index

    def __ge__(self, other):
        ''' return comparison using >= on index '''
        return self.index >= other.index

    def __str__(self):
        ''' built-int str() method returns string representation '''
        #return f'{self.__class__.__name__}{self.get_row_col()} index:{self.index}'
        return f'{self.__class__.__name__}{self.get_row_col()} {self.attr()}'


    def __repr__(self):
        ''' built-int repr() method returns machine readable representation '''
        return '{:_<8}[{:02}/{:02}]_{:02}'.format(
            self.__class__.__name__, *self.get_row_col(), self.get_index())

    def __hash__(self):
        return hash(json.dumps(vars(self)))

    def attr(self):
        s = ''
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    s += str(json.dumps(i))
        return s


class Forest(Cell):
    ''' and kind of alive Forest
        index: age of Forest '''
    color = "#228B22"  # RGB (red green blue) > G = max (FF) > green 228B22
    burnable = True


class Water(Cell):
    ''' any kind of water, eg. sea, river, ...
        index: e.g. hardness ...  '''
    # no need to set burnable, False is inherited
    color = "#0000FF"  # RGB (red green blue) > B = max (FF) > blue


class Mountain(Cell):
    ''' any kind of rock ...
        index: depth, cleannes, flow, ...  '''
    # no need to set burnable, False is inherited
    color = "#888888"  # RGB (red green blue) > stone color


class Fence(Cell):
    ''' Metal fence ...'''
    color = "#FEE3D4"


class BrokenFence(Cell):
    ''' Metal broken fence ...'''
    color = "#FEE3D4"


class Path(Cell):
    ''' Metal fence ...'''
    color = "#FEE3D4"


class Visitor(Cell):
    ''' Visitor ...'''
    color = "#FEE3D4"


class Ranger(Cell):
    ''' Ranger ...'''
    color = "#FEE3D4"


class Swamp(Cell):
    ''' any kind of Swamp ...
        index: height -> dunes, ...  '''
    # no need to set burnable, False is inherited
    color = "#C2B280"  # RGB (red green blue) > Swamp color

class Grass(Cell):
    ''' any kind of Swamp ...
        index: height -> dunes, ...  '''
    color = "#228B22"  # RGB (red green blue) > Swamp color

class Plants(Cell):
    color = "#228B22"  # RGB (red green blue) > Swamp color


class Dirt(Cell):
    ''' any kind of Swamp ...
        index: height -> dunes, ...  '''
    color = "#964B00"  # RGB (red green blue) > Swamp color


''' to do:
    - define your own cells (has to inherit cell)
'''

class Trex(Cell):
    ''' walks on land and eats dinos
        index: size '''
    color = "#228B22"  # RGB (red green blue) > cyan color
class Parasaurolophus(Cell):
    ''' walks on land and eats dinos
        index: size '''
    color = "#228B22"  # RGB (red green blue) > cyan color

class Brachiosaurus(Cell):
    ''' walks on land and eats dinos
        index: size '''
    color = "#228B22"  # RGB (red green blue) > cyan color

class Trunk(Cell):
    ''' after Tree gets eaten there will be a trunk which grows back to an Tree'''
    color = "#228B22"

# test
if __name__ == '__main__':
    cells = 30  # use 30 x 30 cells
    cell_classes = Cell.__subclasses__()
    cell_names = [cell.__name__ for cell in cell_classes]
    print('all cells:', *cell_names)
    # create random cells
    random_cells = [[random.choice(cell_classes)(row, col)
                     for col in range(cells)]
                    for row in range(cells)]
    # swap cells
    cell_1 = random.choice(random.choice(random_cells))  # 2 dim
    cell_2 = random.choice(random.choice(random_cells))  # 2 dim
    cell_1 + 5  # magic method __add__
    cell_2 + 7  # magic method __add__
    print(f'get two cells: {cell_1!r} {cell_2!r}')
    cell_1.swap(cell_2)  # swaps also index
    print(f'and swap     : {cell_1!r} {cell_2!r}')
    # mutate to
    print(f'{cell_1!r}')
    # print cells
    print('\nrandom cells: Name [row/col] Index')
    for line in random_cells:
        for cell in line:
            print(f' {cell!r}', end='')  # use __repr__
        print()
    # dump random cells to csv
    file_path = '../csv_scene_files/random_cells.csv'
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in random_cells:
            cells = [cell.__class__.__name__ for cell in line]  # name only
            writer.writerow(cells)
