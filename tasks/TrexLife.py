''' task: Trex
    Trex walks around, cannot pass Mountain, water or Fence
    - when Trex meet Brachiosaurus, or Parasaurolophus they turn into Grass
'''

__description__ = 'Trex walks around and kills dinosaurs and makes babys'
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
            if isinstance(neighbor, (Parasaurolophus, Brachiosaurus)):
                cell.swap(neighbor)
                neighbor = neighbor.mutate_to(Grass)
                self.update(cell)
                self.update(neighbor)
            elif isinstance(neighbor, Trex):
                prob = random.random()
                if (prob < 0.1):
                    empty_cell = self.get_random_cell(Plants)
                    new_para = empty_cell.mutate_to(Parasaurolophus)
                    self.update(new_para)
            elif isinstance(neighbor, Swamp):
                cell = cell.mutate_to(Grass)
                self.update(cell)
            else:
                if not isinstance(neighbor, (Water, Mountain, Fence)):
                    cell.swap(neighbor)
                    cell.set_index(neighbor.get_index())
                    neighbor.set_index(0)
                    self.update(cell)
                    self.update(neighbor)



if __name__ == '__main__':
    print('''
    test TrexLife
    - Trex roams the world, eats Parasaurolophus and Brachiosaurus
    - When meeting another Trex, there's a chance to generate 5 new Trex
    - Trex will be stuck on Swamp, and die when its index reaches 50
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