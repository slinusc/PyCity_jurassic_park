
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
