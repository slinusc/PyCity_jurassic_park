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
 #           elif isinstance(neighbor, Trex):
  #              for _ in range(2):
   #                 empty_cell = self.get_random_cell(Dirt)
  #                  new_trex = empty_cell.mutate_to(Trex)
   #                 self.update(new_trex)
            elif isinstance(neighbor, Swamp):
                cell = cell.mutate_to(Grass)
                self.update(cell)
            else:
                if not isinstance(neighbor, (Water, Mountain, Fence)):
                    cell.set_previous_type(type(neighbor))  # save neighbor's type
                    cell.swap(neighbor)
                    if cell.get_previous_type() is not None:
                        neighbor.mutate_to(cell.get_previous_type())  # restore neighbor's previous type
                    else:
                        neighbor.mutate_to(Grass)  # replace with your default cell type

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