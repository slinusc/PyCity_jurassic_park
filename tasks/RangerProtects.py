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
            if isinstance(neighbor, Trex):  # meet a dinosaur
                neighbor = neighbor.mutate_to(Path)  # transform into Path
                new_trex_cell = self.get_cell_at_position(0, len(self.cells[0]) - 1)  # get cell at top right corner
                new_trex = new_trex_cell.mutate_to(Trex)
                self.update(new_trex)
                self.update(neighbor)
            elif isinstance(neighbor, Brachiosaurus):
                neighbor = neighbor.mutate_to(Path)
                new_brachio_cell = self.get_cell_at_position(0, 0)  # get cell at top left corner
                new_brachio = new_brachio_cell.mutate_to(Brachiosaurus)
                self.update(new_brachio)
                self.update(neighbor)
            elif isinstance(neighbor, Parasaurolophus):
                neighbor = neighbor.mutate_to(Path)
                new_para_cell = self.get_cell_at_position(len(self.cells) - 1, 0)  # get cell at bottom left corner
                new_para = new_para_cell.mutate_to(Parasaurolophus)
                self.update(new_para)
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

