#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' task: Visitor
    Visitor walks on Path only
    - when Visitor meet Brachiosaurus, Trex, or Parasaurolophus, they turn into Path
'''

__description__ = 'Visitor walks on Path and transforms dinosaurs into Path'
__author__ = 'Andres Mock'

import sys
import copy
sys.path.append('../')

from cells.Cells import *
from tasks.Task import Task

class RangerProtects(Task):
    ''' simulates ranger behavior '''
    def do_task(self, cell=None):
        ''' do the task > manipulate cells '''
        if cell is None:  # if not cell clicked by mouse
            cell = self.get_random_cell(Ranger)  # want a Visitor only to ..
        if isinstance(cell, Ranger):  # it's a Ranger
            neighbor = self.get_neighbor_cell_direction(cell, ["up", "left", "right","down"])  # get a random neighbor
            if isinstance(neighbor, (Brachiosaurus, Trex, Parasaurolophus)):  # meet a dinosaur
                neighbor = neighbor.mutate_to(Path)  # transform into Path
                self.update(neighbor)
            elif isinstance(neighbor, Path):
                cell.swap(neighbor)
                cell.set_index(neighbor.get_index())
                neighbor.set_index(0)
                self.update(cell)
                self.update(neighbor)
            elif isinstance(neighbor, BrokenFence):  # meet a BrokenFence
                neighbor = neighbor.mutate_to(Fence)  # transform into Fence
                self.update(neighbor)  # update the state of the neighbor

