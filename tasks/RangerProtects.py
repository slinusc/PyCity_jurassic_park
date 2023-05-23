''' task: RangerProtects
    Rangers  walks around on only Path
    fixes BrokenFence, kills all dinosaurs when he meets
    walks randomly around but only up and to the side
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
            neighbor = self.get_neighbor_cell_direction(cell, ["up", "left", "right"])  # get a random neighbor
            if isinstance(neighbor, Trex):  # meet a dinosaur
                neighbor = neighbor.mutate_to(Path)  # transform into Path
                new_trex_cell = self.get_cell_at_position(0, len(self.cells[0]) - 1) # get cell at top right corner
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
                self.update(cell)
                self.update(neighbor)
            elif isinstance(neighbor, BrokenFence):  # meet a BrokenFence
                neighbor = neighbor.mutate_to(Fence)  # transform into Fence
                self.update(neighbor)  # update the state of the neighbor


if __name__ == '__main__':  # test only
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)
    CELLS = 30
    RUNS = 1000

    def count_Dinos_Fences(cells):
        dinos = 0
        fences = 0
        for row in cells:
            for cell in row:
                if isinstance(cell, (Trex, Brachiosaurus, Parasaurolophus)):
                    dinos += 1
                elif isinstance(cell, Fence):
                    fences += 1
        return dinos, fences  # return as tuple

    # simulate RangerProtects
    cells = [[random.choice([Path(row, col), Ranger(row, col), Trex(row, col), Brachiosaurus(row, col), Parasaurolophus(row, col), BrokenFence(row, col)]) for col in range(CELLS)] for row in range(CELLS)]
    rangerProtects = RangerProtects(cells)
    print(f'simulate {RUNS} runs of {rangerProtects}')
    print(f' - starting with {count_Dinos_Fences(cells)[0]} Dinosaurs and {count_Dinos_Fences(cells)[1]} Fences')
    for run in range(RUNS):
        rangerProtects.do_task()
    dinos, fences = count_Dinos_Fences(cells)  # return tuple
    print(f' - ended with {dinos} Dinosaurs and {fences} Fences')