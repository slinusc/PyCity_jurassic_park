#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' surfaces loading from pre-defined scenarios stored in csv files '''

__description__ = 'load cells as scenes from csv files'
__version__ = '1.0.4'
__author__ = 'Stephan Metzler'
__email__ = 'metl@zhaw.ch'
__status__ = 'build your way to extraordinary'

import sys
import csv
import random
from os import listdir
from os.path import dirname, join
from datetime import datetime
import numpy as np

sys.path.append('../')  # search moduls in parent folder too
from cells import Cells as c

START_SCENE = 'IlesOfTrees.csv'  # load this scene on startup
CSV_FILE_PATH = "../csv_scene_files"  # path of csv files
CELLS = 30
ALL_CELLS = c.Cell.__subclasses__()


class Scenes:
    ''' load cells as scenes from csv files '''
    #cells = [[c.Cell() for col in range(CELLS)] for row in range(CELLS)]
    cells = np.full((CELLS, CELLS), c.Cell())
    path = join(dirname(__file__), CSV_FILE_PATH)  # path of csv files

    def __init__(self):
        ''' constructor '''
        files = listdir(self.path)  # csv files in folder
        self.scenes = list(filter(lambda f: f.endswith('.csv'), files))
        self.build_cells(START_SCENE)  # build cells from start scene

    def build_cells(self, file_name):
        ''' build cells from csv data '''
        row = col = 0
        file = join(self.path, file_name)  # file path
        data = list(csv.reader(open(file)))  # load data
        for line in data:  # for all lines in csv
            for cell_object in line:  # for all cells in csv line
                cell = vars(c)[cell_object](row, col)  # instance cell object
                self.cells[row][col] = cell  # put to list
                col += 1
            col = 0
            row += 1
        self.check_cells()  # check cell data
        return self.cells

    def get_cells(self):
        ''' return cells of scene '''
        return self.cells

    def get_random_cell(self):
        ''' return random cells '''
        return random.choice(random.choice(self.cells))  # 2 dim

    def get_blank_cells(self):
        ''' return blank cells '''
        self.cells = [[c.Hole(row, col)
                       for col in range(CELLS)] for row in range(CELLS)]
        return self.cells

    def check_cells(self):
        ''' ceck if all cell are of Cell instance '''
        for line in self.cells:  # for all rows
            for cell in line:  # for all cells in row
                assert isinstance(cell, c.Cell)  # assert stops on False

    def get_scenes(self):
        ''' return current scene '''
        return self.scenes

    def dump_to_csv(self):
        ''' dump cells to csv file '''
        now = datetime.now()  # current time stamp
        file_name = now.strftime('%Y%m%d-%H%M%S')  # file name
        file = join(self.path, file_name + '.csv')  # file path
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f)
            for line in self.cells:
                cell_name = [cell.__class__.__name__ for cell in line]  # name
                writer.writerow(cell_name)
        return file

        ''' built-int str() method to return a string representation '''
    def __str__(self):
        scene_name = ''
        for file in self.scenes:  # self.scenes is tuple
            scene_name += f'\n - {file}'
        return scene_name


if __name__ == '__main__':  # test only
    s = Scenes()  # get scene
    print(f'list csv Scences ... {s}')
    print(f'dump scene {s.dump_to_csv()}')  # dump > check folder
    for scene in s.scenes:  # all scenes
        s.build_cells(scene)  # buil scene
        cells = s.get_cells()  # get cells
        s.check_cells()  # check cells
        print(f'build {scene:30} with {len(cells) * len(cells[0])} cells')
