import sys
import random
import copy
sys.path.append('../')  # search modules in parent folder too

from cells.Cells import *
from tasks.Task import Task
from scenes.Scenes import Scenes

class TrexLife(Task):
    ''' simulates Trex life '''

    def do_task(self, cell=None):
        ''' manipulate cells based on Trex behavior '''
        if cell is None:
            cell = self.get_random_cell(Trex)

        if isinstance(cell, Trex):
            cell + 1  # Increase the index by 1 for each move
            if cell.get_index() >= 50:
                cell = cell.mutate_to(Dirt)  # Trex dies and turns into dirt
                self.update(cell)

            neighbor = self.get_neighbor_cell(cell)
            if isinstance(neighbor, (Water, Mountain, Sand)):
                if isinstance(neighbor, Sand):
                    cell = cell.mutate_to(Sand)  # Trex stuck in sand
                    self.update(cell)

            elif isinstance(neighbor, (Parasaurolophus, Brachiosaurus)):
                neighbor = neighbor.mutate_to(Dirt)  # Trex eats the dinosaur, and it turns into dirt
                cell.swap(neighbor)
                self.update(neighbor)

            elif isinstance(neighbor, Trex):
                prob = random.random()
                if prob < 0.1:  # 1/10 chance of creating 5 new Trex
                    for _ in range(5):
                        empty_neighbor = self.get_neighbor_cell(cell, lambda c: isinstance(c, Dirt))
                        if empty_neighbor:
                            new_trex = empty_neighbor.mutate_to(Trex)
                            self.update(new_trex)
                else:
                    cell.swap(neighbor)
                    self.update(neighbor)

            else:  # Trex moves to a different cell
                cell.swap(neighbor)
                self.update(neighbor)


if __name__ == '__main__':  # test only
    print('''
    test TrexLife
    - Trex moves around, eats Parasaurolophus and Brachiosaurus
    - When Trex meets another Trex, there's a 1/10 chance of creating 5 new Trex
    - Trex gets stuck in Sand and can't move on Water or Mountain
    - Trex dies after reaching an index of 50
    ''')

    CELLS = 30  # scene with 900 cells
    STEPS = 10  # do the task 10 times
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    cells = Cell.__subclasses__()
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)

    # generate random cells
    cells = [[random.choice(cells)(row, col)
              for col in range(CELLS)]
             for row in range(CELLS)]
    print('# random cells:', len(cells) * len(cells[0]))

    # simulate TrexLife
    trexLife = TrexLife(cells)  # get task
    trex = trexLife.get_random_cell(Trex)  # get a Trex
    row, col = trex.get_row_col()  # get row and col
    for i in range(STEPS):
        cell = copy.copy(trex)  # copy to cell
        trexLife.do_task(trex)  # do task
        if not cell == cells[row][col]:  # on changed cell
            print(f'{trexLife} on {cell!r} effects {trex!r} and {cells[row][col]!r}')