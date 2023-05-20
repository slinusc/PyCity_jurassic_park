''' task: TangerProteccts
    Rangers  walks around on only Path
    fixes BrokenFence, kills all dinosaurs when he meets
    walks ranodmly around
'''

__description__ = 'Ranger walks on Path and transforms dinosaurs into Path, fixes Gates'
__author__ = 'Obermühlner Adrian'

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

