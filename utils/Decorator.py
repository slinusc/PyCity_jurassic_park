#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' PyCity decorators: log & exception write to files '''

__description__ = 'PyCity Decorators'
__version__ = '1.0.4'
__author__ = 'Stephan Metzler'
__email__ = 'metl@zhaw.ch'
__status__ = 'build your way to extraordinary'

import os
import sys
import random
import copy
import time
import numpy as np
from functools import wraps
import logging
import inspect
sys.path.append('../')  # search moduls in parent folder too
from cells.Cells import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'pyCity_log.log')  # log file
ERR_FILE = os.path.join(BASE_DIR, 'pyCity_err.log')  # error file


class Elapse():
    ''' elapse is aused as staic class variable '''
    elapse = time.time()  # static clas variable -> Elapse.elapse


def log(func):  # log to file
    ''' log decorator '''
    def wrapper(*args, **kwargs):
        ''' inner wrapper '''
        _stack = inspect.stack()[1]  # get function stack
        task = _stack[0].f_locals['task_instance']  # calling task
        cells = task.cells  # get the calls before doing the task
        cells_before_task = np.copy(cells)  # copy before doing the task
        ret = func(*args, **kwargs)  # call the function -> do the job
        changes = []
        changed_cells = np.not_equal(cells, cells_before_task)  # compair
        for index, changed in np.ndenumerate(changed_cells):  # changed cells
            if changed:
                row, col = index
                changes.append((cells_before_task[row][col], cells[row][col]))
        if changes:
            now = time.time()  # actual time
            elapse = now - Elapse.elapse  # calculate elapse time
            Elapse.elapse = now  # save actual time in static class variable
            task_name = task.__class__.__name__   # task name
            changed_cells = ''
            for change in changes:  # compose message for log file
                changed_cells += f"{change[0]!r} to {change[1]!r}\n{' ':43}"
            msg = f'{task_name[:14]:15} elapses {elapse:.3f} sec '
            msg += f'changes: {changed_cells[:-44]}\n'  # message
            with open(LOG_FILE, 'a') as f:  # write to file
                f.write(msg)
        return ret
    return wrapper


def create_logger():
    ''' creates a logging object and returns it '''
    logger = logging.getLogger("PyCity")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(ERR_FILE)  # create the logging file handler
    fmt = '\n%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # add handler to logger object
    return logger


def exception(function):
    ''' decorator that wraps the passed in function and logs
        exceptions should one occur '''
    @wraps(function)
    def wrapper(*args, **kwargs):
        ''' inner wrapper '''
        try:
            return function(*args, **kwargs)
        except Exception as e:
            err = str(function).split(' ', 3)[1]  # log the exception
            create_logger().exception(err)
            msg = f'ERROR calling {err}\n\t{e}\n'
            msg += f'see error file\n\t-{ERR_FILE}'
            print(msg)
            sys.exit()  # abort application on exception
    return wrapper


if __name__ == '__main__':  # test only

    sys.path.append('../')  # search moduls in parent folder too
    from cells import Cells as c
    import tasks
    from tasks import *

    cells = 30  # use 30 x 30 cells
    cell_classes = c.Cell.__subclasses__()

    random_cells = [[random.choice(cell_classes)(row, col)  # create cells
                     for col in range(cells)]
                    for row in range(cells)]

    class Dummy():
        ''' dummy test class '''

        def foo(self, error=False):
            ''' dummy foo method '''
            @log
            @exception
            def call_task(task, cell):
                ''' call the task and pass cell '''
                return task.do_task(cell),
            task_instance = tasks.FireBlaze.FireBlaze(random_cells)  # create
            cell = task_instance.get_random_cell(Tree)  # get a tree
            # change on index 3: Fire > Chark > Tree > Fire > ..
            row, col = cell.get_row_col()  # get cell row and col ..
            for i in range(15):  # .. cell will change
                call_task(task_instance,  # to simultate @exception
                          '' if error else task_instance.cells[row][col])

    Dummy().foo()  # see log file
    Dummy().foo(error=True)  # to simulate @exception
