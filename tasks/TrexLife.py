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
                neighbor = neighbor.mutate_to(Dirt)
                self.update(cell)
                self.update(neighbor)
            elif isinstance(neighbor, Trex):
                if random.random() < 0.4:
                    for _ in range(5):
                        empty_cell = self.get_random_cell(Dirt)
                        new_trex = empty_cell.mutate_to(Trex)
                        self.update(new_trex)
            elif isinstance(neighbor, Swamp):
                cell = cell.mutate_to(Dirt)
                self.update(cell)
            else:
                if not isinstance(neighbor, (Water, Mountain)):
                    previous_state = neighbor.get_state()  # save previous state
                    cell.swap(neighbor)
                    neighbor.set_state(previous_state)  # restore previous state
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