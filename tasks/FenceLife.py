
''' task: FenceLife
    - Will break randomly
    - Broken Fence gets fixed randomly or by Rangers
'''


__description__ = 'Fences turn into BrokenFences randomly, broken fences randomly get fixed'
__author__ = 'Obermühlner Adrian'

import sys
import random

sys.path.append('../')  # search modules in parent folder too

from cells.Cells import *
from tasks.Task import Task


class FenceLife(Task):
    ''' simulates fence decay '''

    def do_task(self, cell=None):
        ''' mutate Fence to BrokenFence with 10% probability '''
        if not cell:
            cell = self.get_random_cell()  # use any cell

        if isinstance(cell, Fence):
            prob = random.random()
            if (prob < 0.1):  # 10% chance to break
                broken_fence = cell.mutate_to(BrokenFence)
                self.update(broken_fence)
        elif isinstance(cell, BrokenFence):
            fence = cell.mutate_to(Fence)
            self.update(fence)


if __name__ == '__main__':  # test only
    task = [task.__name__ for task in Task.__subclasses__()]
    print('task: ', *task)
    all_cells = [cell.__name__ for cell in Cell.__subclasses__()]
    print('cells:', *all_cells)
    CELLS = 30
    RUNS = 1000

    def count_Fences(cells):
        fences = 0
        broken_fences = 0
        for row in cells:
            for cell in row:
                if isinstance(cell, Fence):
                    fences += 1
                elif isinstance(cell, BrokenFence):
                    broken_fences += 1
        return fences, broken_fences  # return as tuple

    # simulate FenceLife
    cells = [[random.choice([Fence(row, col), BrokenFence(row, col)]) for col in range(CELLS)] for row in range(CELLS)]
    fenceLife = FenceLife(cells)
    print(f'simulate {RUNS} runs of {fenceLife}')
    print(f' - starting with {count_Fences(cells)[0]} Fences and {count_Fences(cells)[1]} Broken Fences')
    for run in range(RUNS):
        fenceLife.do_task()
    fences, broken_fences = count_Fences(cells)  # return tuple
    print(f' - ended with {fences} Fences and {broken_fences} Broken Fences')