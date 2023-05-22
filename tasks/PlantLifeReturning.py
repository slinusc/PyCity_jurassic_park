''' task: PlantLifeReturning
    - Grass will turn into Plants with a likelyhood of 50%
    - Trunk will turn back into Forest after time
'''
__description__ = 'Grass turns into Plants and Trunk into Forest'
__author__ = 'Mike Gasser'



import sys
import random

sys.path.append('../')  # search modules in parent folder too

from cells.Cells import *
from tasks.Task import Task


class PlantLifeReturning(Task):
    ''' simulates forest regrow and plants grow '''

    def do_task(self, cell=None):
        ''' mutate grass cells to plants
            and trunk cells to forest '''
        if not cell:
            cell = self.get_random_cell()  # use any cell

        if isinstance(cell, Grass):
            prob = random.random()
            if (prob < 0.5):
                plants = cell.mutate_to(Plants)
                self.update(plants)
        elif isinstance(cell, Trunk):
            forest = cell.mutate_to(Forest)
            self.update(forest)

if __name__ == '__main__':  # test only
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)
    CELLS = 30
    RUNS = 1000

    def count_Forests(cells):
        forests = 0
        grow = 0
        for row in cells:
            for cell in row:
                if isinstance(cell, Forest):
                    forests += 1
                    grow += cell.get_index()
        return forests, grow  # return as tuple

    # simulate PlantLifeReturning
    plantLifeReturning = PlantLifeReturning(cells)
    print(f'simulate {RUNS} runs of {plantLifeReturning}')
    print(f' - starting with {count_Forests(cells)[0]} Forests')
    for run in range(RUNS):
        plantLifeReturning.do_task()
    forests, grow = count_Forests(cells)  # return tuple
    print(f' - produced {forests} Forests and {grow} grow index')