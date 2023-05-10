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
                cell + neighbor.get_index()
                neighbor = neighbor.mutate_to(Dirt)
                cell + 1
                self.update(cell)
                self.update(neighbor)
            elif isinstance(neighbor, Trex):
                if random.random() < 0.2:
                    for _ in range(5):
                        empty_cell = self.get_random_cell(Dirt)
                        new_trex = empty_cell.mutate_to(Trex)
                        self.update(new_trex)
            elif isinstance(neighbor, (Dirt, Plants, Tree)):
                cell.swap(neighbor)
                cell.set_index(neighbor.get_index())
                neighbor.set_index(0)
                cell + 1
                self.update(cell)
                self.update(neighbor)
            elif isinstance(neighbor, Sand):
                cell.swap(neighbor)
                cell.set_index(neighbor.get_index())
                neighbor.set_index(0)
                self.update(cell)
                self.update(neighbor)

            if cell.get_index() >= 100:
                cell = cell.mutate_to(Dirt)
                self.update(cell)


if __name__ == '__main__':
    print('''
    test TrexLife
    - Trex roams the world, eats Parasaurolophus and Brachiosaurus
    - When meeting another Trex, there's a chance to generate 5 new Trex
    - Trex will be stuck on Sand, and die when its index reaches 50
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