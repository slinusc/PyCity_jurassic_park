''' task: Trex
    Trex walks around, cannot pass Water or Fence
    - when Trex meet Brachiosaurus, or Parasaurolophus they turn into Grass
    - when Trex meets Ranger he will die and a new one will spawn
'''

__description__ = 'Trex walks around and kills dinosaurs'
__author__ = 'Linus Stuhlmann'

import sys
import random
import copy
sys.path.append('../')  # search modules in parent folder too

from cells.Cells import *
from tasks.Task import Task
from scenes.Scenes import Scenes

class TrexLife(Task):
    def do_task(self, cell=None):
        if cell is None:
            cell = self.get_random_cell(Trex)
        if isinstance(cell, Trex):
            neighbor = self.get_neighbor_cell(cell)
            other_neighbor = self.get_neighbor_cell(cell)
            next_cell = self.get_neighbor_cell(neighbor)
            if isinstance(neighbor, BrokenFence) and isinstance(other_neighbor, (Grass, Plants, Forest, Trunk)):
                if isinstance(next_cell, Path):
                    cell.swap(next_cell)
                    next_cell = next_cell.mutate_to(Grass)
                    self.update(cell)
                    self.update(next_cell)
            elif isinstance(neighbor, BrokenFence) and isinstance(other_neighbor, Path):
                if isinstance(next_cell, (Plants, Forest, Grass)):
                    cell.swap(next_cell)
                    next_cell = next_cell.mutate_to(Path)
                    self.update(cell)
                    self.update(next_cell)
            elif isinstance(neighbor, Brachiosaurus):
                neighbor = neighbor.mutate_to(Grass)
                new_brachio_cell = self.get_cell_at_position(0, 0)  # get cell at top left corner
                new_brachio = new_brachio_cell.mutate_to(Brachiosaurus)
                self.update(new_brachio)
                self.update(neighbor)
            elif isinstance(neighbor, Parasaurolophus):
                neighbor = neighbor.mutate_to(Grass)
                new_para_cell = self.get_cell_at_position(len(self.cells) - 1, 0)  # get cell at bottom left corner
                new_para = new_para_cell.mutate_to(Parasaurolophus)
                self.update(new_para)
                self.update(neighbor)
            elif isinstance(neighbor, Visitor):
                neighbor = neighbor.mutate_to(Path)
                self.update(neighbor)
            elif isinstance(neighbor, Ranger):
                cell = cell.mutate_to(Path)
                new_trex_cell = self.get_cell_at_position(0, len(self.cells[0]) - 1)  # get cell at top right corner
                new_trex = new_trex_cell.mutate_to(Trex)
                self.update(new_trex)
                self.update(cell)
            else:
                if not isinstance(neighbor, (Water, Fence, BrokenFence)):
                    cell.swap(neighbor)
                    self.update(cell)
                    self.update(neighbor)


if __name__ == '__main__':
    print('''
    test TrexLife
    - Trex roams the world, eats Parasaurolophus and Brachiosaurus
    - Trex gets killed by Rangers when meeting them
    ''')
    CELLS = 30
    RUNS = 1000

    cells = [[random.choice(Cell.__subclasses__())(row, col)
              for col in range(CELLS)]
             for row in range(CELLS)]

    trex_life = TrexLife(cells)
    print(f'simulate {RUNS} runs of {trex_life}')

    for run in range(RUNS):
        trex_life.do_task()