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
