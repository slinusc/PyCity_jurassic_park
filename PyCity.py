#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' trivial SimCity approach:
    Be the hero of your very own landscape as you design and create a
    beautiful, bustling metropolis in PyCity.
    Every decision is yours as your city gets larger and more intricate.
    Make smart choices to keep your citizens happy, your skyline growing
    and protect your environment sustainable.
    Build your way to extraordinary.                            @ea.com '''

__description__ = 'main PyCity application'
__version__ = '1.0.8'
__date__ = '11.05.2023'
__author__ = 'Stephan Metzler'
__email__ = 'metl@zhaw.ch'
__status__ = 'build your way to extraordinary'

import os
import importlib
import random
import time
import copy
import pickle
import tkinter as tk
from tkinter.messagebox import showinfo, showwarning
import cells.Cells as c
import scenes.Scenes as s
from tasks import *
from tasks import Task
from utils.Decorator import log, exception, Elapse
from utils.StatusBar import StatusBar


''' change this settings on demand '''
CELLS = 30  # grid > cells x cells >> make sure you use cpmpatable csv files
CELL_SIZE = 20  # display size of cell rectangle
INFO = 250  # offest for Info Cnavas
STATUS = 20  # height of status bar
TIMER = 50  # time in msec to updates tasks
START_TASKS = 'ParasaurolophusLife', 'BrachiosaurusLife', 'PlantLifeReturning', 'VisitorWalksAround', 'TrexLife', 'FenceLife', 'RangerProtects'
FONT = ("Consolas", int(CELL_SIZE / 2))  # fonnt for text in window
LABEL_COLOR = 'blue'  # used for label title
LABEL_CELL_INFO = 'red'  # mouse hover cell info
LABEL_ENABLE = 'black'  # used on enabled tasks
LABEL_DISABLE = 'grey'  # used on disabled tasks

''' leave this related setting '''
SIZE = CELLS * CELL_SIZE
WIDTH = SIZE + INFO  # with is grid  size and info size
HEIGHT = SIZE + STATUS  # height is grid size
ALL_CELLS = c.Cell.__subclasses__()  # all cell objects
START_SCENE = s.START_SCENE[:-4]  # IlesOfTrees > this scene is loaded on start
if os.name == "posix":
    ICON = '@icon/pyCity.xbm'  # folder icon
else:
    ICON = 'icon/pyCity.ico'  # folder icon
HOWTO = 'info/howto.txt'  # folder
KEY = 'info/keys.txt'  # folder
IMAGE = 'pics'  # folder
IMAGE_EXT = '.png'  # image extension
LIMIT = 20  # limits name for display


class PyCity(tk.Tk):
    ''' trivial SimCity approach '''
    displayed_cells = [[()  # empty 2dim list of tuple ...
                        for col in range(CELLS)]  # as tupel (rectangle, text)
                       for row in range(CELLS)]  # of displayed cells
    scene = s.Scenes()  # get a Scenes instance
    scenes = 'Scene', scene.get_scenes()  # type is tupel
    all_tasks = [task.__name__ for task in Task.Task.__subclasses__()]
    tasks = 'Task', all_tasks  # tuple
    task_labels = []  # list of task labels
    events = 'Event', ['step', 'start', 'stop']  # type is tupel
    controls = 'Control', ['all tasks', 'blank', 'info', 'no tasks', 'random cells',
                           'picture (toggle)', 'scene dump', 'toggle task']  # type is tupel
    cells = scene.get_cells()  # reference to cells
    cell_labels = []  # list of cell labels
    task_on_cell = None  # do all enabled tasks on cell
    toggle_task = 0  # toggle through tasks
    show_img = True  # show cell image
    cell = None  # selected cell
    clone = None  # cell to clone
    loop = False  # loop cycle
    start = time.time()

    @exception  # writes exception to err file
    def __init__(self, info=False):  # info popups text message
        ''' constructor '''
        super().__init__()  # call Tk Constructor
        self.title("PyCity " + __version__)  # set window title
        self.minsize(WIDTH, HEIGHT)  # set window size
        self.wm_iconbitmap(ICON)  # set icon
        self.main = tk.Canvas(self, width=WIDTH, height=HEIGHT)  # main, with
        self.grid = tk.Canvas(self.main, width=SIZE, height=SIZE)  # ... grid
        self.info = tk.Canvas(self.main, width=INFO, height=SIZE)  # ... info
        self.main.create_window(0, 0, anchor=tk.NW, window=self.grid)
        self.main.create_window(SIZE, 0, anchor=tk.NW, window=self.info)
        self.grid.bind("<Button-1>", self.left_mouse_click)  # left mouse click
        self.grid.bind("<Button-2>", self.right_mouse_click)  # on Mac
        self.grid.bind("<Button-3>", self.right_mouse_click)  # on Windows
        self.grid.bind("<B1-Motion>", self.mouse_move)  # mouse move
        self.grid.bind("<Motion>", self.cell_info)  # print cell on mouse hover
        self.grid.bind("<ButtonRelease-1>", self.mouse_release)  # mouse up
        self.bind("<Key>", self.on_key)  # bind keys > key event calls on_key()
        # load existing gif image files in dict
        self.images = {img[:-4]: tk.PhotoImage(file=os.path.join(IMAGE, img))
                       for img in os.listdir(IMAGE) if img.endswith(IMAGE_EXT)}
        self.init_menus()  # init menus
        self.init_cells()  # init cells
        self.init_labels()  # init labels
        self.status = StatusBar(self.main, 'yellow', 'black')  # status bar
        self.main.pack(expand=True, fill=tk.BOTH)  # pack Tk application
        if info:  # pop-up info text (this is the info from custructor)
            with open(HOWTO, 'r') as f:
                showinfo('Welcome to PyCity', f.read())  # open showinfo box

    @exception  # writes exception to err file
    def init_menus(self):
        ''' init windows menus '''
        menu_bar = tk.Menu(self)  # menu bar
        # add dynamic menu for scenes, tasks and events
        for items in [self.scenes, self.tasks, self.events, self.controls]:
            menu = tk.Menu(self, tearoff=False)  # create menu
            label = items[0]  # lable it
            for item in items[1]:  # add for each item
                command = lambda label=label, item=item: \
                    self.menu_event(label, item)  # dynamic method to call
                menu.add_command(label=item, command=command)  # add method
            menu_bar.add_cascade(label=label, menu=menu)  # add to menu
        menu_bar.add_cascade(label="About", command=self.about)  # exit menu
        menu_bar.add_cascade(label="EXIT", command=self.quit)  # exit menu
        self.config(menu=menu_bar)  # add menubar

    @exception  # writes exception to err file
    def init_cells(self):
        ''' map cells to labels '''
        x = y = 0  # starting pixels
        offset = int(CELL_SIZE / 2)  # image offset
        for row in range(CELLS):  # for all rows
            for col in range(CELLS):  # for all cols
                cell = self.cells[row][col]  # get cell
                name = cell.__class__.__name__  # cell name
                index = self.get_cell_index(cell)  # get cell index
                color = 'black' if cell.is_dark() else 'white'  # get color
                rectangle = self.grid.create_rectangle(  # add rectangle
                    x, y, x + CELL_SIZE, y + CELL_SIZE,
                    fill=cell.color, width=0)
                text = self.grid.create_text(  # add cell lable to grid
                    x + offset, y + offset, font=FONT, text=index, fill=color)
                if (name in self.images.keys()):  # display gif image if exists
                    img = self.grid.create_image(
                        x + offset, y + offset, image=self.images[name])
                else:  # use 'Blank' immage
                    img = self.grid.create_image(
                        x + offset, y + offset, image=self.images['Blank'])
                self.displayed_cells[row][col] = rectangle, text, img  # add
                if cell.col % CELLS == CELLS - 1:  # calc. new pixel position
                    x = 0
                    y += CELL_SIZE
                else:
                    x += CELL_SIZE

    @exception  # writes exception to err file
    def init_labels(self):
        ''' init info labels: title, scene, tasks, cells  '''
        fg = LABEL_COLOR  # foreground text color
        # scene
        tk.Label(self.info, text=self.scenes[0], fg=fg, font='bold'). \
            grid(column=0, columnspan=2, row=0, sticky='w')  # scenes titel
        self.scene_label = tk.Label(self.info, text=START_SCENE[:LIMIT],
                                    fg=LABEL_ENABLE)  # active scene
        self.scene_label.grid(column=0, columnspan=2, row=1,
                              sticky='w', padx=10)  # add grid
        # tasks
        tk.Label(self.info, text='Tasks', fg=fg, font='bold'). \
            grid(column=0, columnspan=2, row=2, sticky='w')  # task titel label
        row = 3  # start on row 5
        for task in self.tasks[1]:  # add label for each task
            task_lbl = tk.Label(self.info, text=task[:LIMIT],
                                fg=LABEL_DISABLE
                                if task not in START_TASKS
                                else LABEL_ENABLE)
            task_lbl.grid(column=0, columnspan=2, row=row, sticky='w', padx=10)
            task_count_lbl = tk.Label(self.info, text='0', fg=fg)  # count
            task_count_lbl.grid(column=2, row=row, sticky='e')  # add
            self.task_labels.append([task_lbl,  # task name label
                                     task_count_lbl,  # tast count label
                                     task in START_TASKS])  # True|False
            row += 1
        # cells
        tk.Label(self.info, text='Cells', fg=fg, font='bold'). \
            grid(column=0, row=row)  # cell titel label
        label = tk.Label(self.info, text='',
                         fg=LABEL_CELL_INFO, justify='right')  # elapsed time label
        label.grid(column=2, columnspan=3, row=row)  # add to grid
        self.cell_labels.append([label, 'info'])  # put to lable list
        row += 1
        for cell_object in ALL_CELLS:  # for all cells
            cell = cell_object(-1, -1)  # instance cell
            name = cell_object.__name__  # get name of cell
            bg_color = cell.color  # get color of cell
            fg_color = 'black' if cell.is_dark() else 'white'
            img = self.images[name if (name in self.images.keys())
            else 'Blank']
            tk.Label(self.info, image=img). \
                grid(column=0, row=row)  # cell label
            tk.Label(self.info, text=name, width=10, fg=fg_color,  # labels for
                     bg=bg_color).grid(column=1, row=row, sticky='w')  # cells
            count = self.count_cells(name)  # sum and perc. as formatted str
            label = tk.Label(self.info, text=count, fg=fg)  # cell info label
            label.grid(column=2, row=row)  # add to grid
            self.cell_labels.append([label, name])  # put to lable list
            row += 1

    @exception  # writes exception to err file
    def menu_event(self, menu, event):
        ''' on menu event: menu=[Scene, Task, Event] enent=menu_event '''
        if menu == "Scene":  # load csv file and display scene
            self.scene_label.config(text=event[:-4][:LIMIT], fg=LABEL_ENABLE)
            self.scene.build_cells(event)  # build scene
            self.update_cells()  # update all cells
            self.update_labels()  # update labels
        elif menu == "Task":  # toggle tasks
            for label in self.task_labels:  # [task, info, True | False]
                if event[:LIMIT] == label[0].cget("text")[:LIMIT]:  # task name
                    label[2] = not label[2]  # toggle True|False
                    label[0].config(fg=LABEL_ENABLE
                    if label[2]
                    else LABEL_DISABLE)  # toggle color
        elif menu == "Event":  # call event [step, start, stop]
            self.loop = event == 'start'
            self.do_tasks()
        elif menu == "Control":  # call control
            self.on_key(None, event)

    def get_cell_clicked(self, event):
        ''' return cell on mouse clicked '''
        x, y = event.x, event.y  # pixel cordinates
        if not 0 < x < SIZE or not 0 < y < SIZE:
            return  # out of grid
        row_ = int((y + CELL_SIZE) / CELL_SIZE - 1)  # row [1 2 3 .. 29]
        cell_nr = CELLS * row_ + int((x + CELL_SIZE) / CELL_SIZE - 1)  # number
        row = int(cell_nr / CELLS)  # row [0 .. 29]
        col = cell_nr % CELLS  # col [0 .. 29]
        try:
            return self.cells[row][col]  # cell
        except IndexError:
            pass  # return None on IndexError

    def left_mouse_click(self, event):
        ''' cell left mouse click event '''

        def debug_print():
            task = '/'.join([
                label[0].cget("text")
                for label in self.task_labels if label[2]])
            if task:
                print(f'do {task} on {self.task_on_cell!r}', flush=True)

        cell = self.get_cell_clicked(event)  # get the cell
        self.task_on_cell = cell  # update selected cell
        self.loop = False  # disable loop mode
        debug_print()  # debug only
        self.do_tasks()  # do the task

    def right_mouse_click(self, event):
        ''' cell right mouse click event - toggle cell '''
        cell = self.get_cell_clicked(event)  # get the cell
        index = ALL_CELLS.index(cell.__class__)  # get index cell list
        next_index = index + 1 if index < len(ALL_CELLS) - 1 else 0
        new = ALL_CELLS[next_index]()
        new.set_row_col(cell.get_row_col())  # apply row, col
        self.cells[new.row][new.col] = new  # add cloned cell
        self.update_cell(new)  # update grid (UI)
        del cell  # dump cell

    def mouse_move(self, event):
        ''' cell mouse move event - clone cell '''
        cell = self.get_cell_clicked(event)  # get the cell
        if not cell:  # no cell (IndexError)
            return  # just return
        elif not self.clone:  # no cell to clone set
            self.clone = cell  # set cell to clone
        else:
            self.cell = cell  # remember cell
            if not cell == self.clone:  # same cell -> no need to clone
                new = copy.copy(self.clone)  # copy cell
                new.set_row_col(cell.get_row_col())  # apply row, col
                self.cells[new.row][new.col] = new  # add cloned cell
                self.update_cell(new)  # update cell (UI)
                del cell  # dump cell

    def mouse_release(self, event):
        ''' reset cells '''
        self.cell = None
        self.clone = None

    @exception  # writes exception to err file
    def do_tasks(self):
        ''' call enabled tasks '''

        @log  # writes to to log file if cell instance changes
        def call_task(task, cell):
            ''' decorated task '''
            task.do_task(cell)  # do task

        # binary serialisation of cell object as list
        cells_before_task = [[pickle.dumps(cell) for cell in row] for row in self.cells]
        for label in self.task_labels:  # for all task labels
            task = label[0].cget("text")  # get task name
            if label[2]:  # task enabeld
                module = 'tasks.' + task  # compose module to load
                task_class = getattr(importlib.import_module(module), task)
                task_instance = task_class(self.cells)  # instance task
                call_task(task_instance, self.task_on_cell)  # do the task
                label[1].config(text=task_instance.counter)  # update count
        # binary serialisation of cell object as list
        cells_after_task = [[pickle.dumps(cell) for cell in row] for row in self.cells]
        for row_of_cells in self.cells:
            for cell in row_of_cells:
                row, col = cell.get_row_col()
                if cells_before_task[row][col] == cells_after_task[row][col]:
                    continue
                self.update_cell(self.cells[row][col])  # update cell
                self.update_labels()

        self.task_on_cell = None  # reset
        elapsed_time = int(time.time() - self.start)
        m, s = divmod(elapsed_time, 60)  # min, sec
        h, m = divmod(m, 60)  # hour, min
        self.cell_labels[0][0].config(text=f'{h:d}:{m:02d}:{s:02d}')  # lable it
        if self.loop:  # timed loop
            self.after(TIMER, self.do_tasks)  # call on scheduled timer

    def on_key(self, event, key=None):
        ''' keyboard key event or control menu '''
        if not key:  # keyboard event
            key = event.keysym  # get key
        else:
            key = key.lower()[0]  # control menu
        if key == 'space':  # on 'space' key
            self.loop = False  # diasble infinity timed loop
            self.do_tasks()  # do all enabled tasks (step by step)
        elif key == 'Return':  # on 'Return' key
            self.loop = True  # enable infinity timed loop
            self.do_tasks()  # do all enabled tasks
        elif key.lower() == 'a':  # enable all tasks
            for task in self.task_labels:  # for all tasks
                task[2] = True  # enable
                task[0].config(fg=LABEL_ENABLE)  # show as enabled
        elif key.lower() == 'b':  # generate blank cells
            self.cells = self.scene.get_blank_cells()  # get blank cells
            self.update_cells()  # update cells
            self.update_labels()  # update labels
        elif key.lower() == 'c':  # about dialog
            self.about()
        elif key.lower() == 'i':  # pop-up info text
            with open(HOWTO, 'r') as f:
                showinfo('Welcome to PyCity', f.read())  # open showinfo box
        elif key.lower() == 'n':  # disble all tasks
            for task in self.task_labels:  # for all tasks
                task[2] = False  # diable
                task[0].config(fg=LABEL_DISABLE)  # show as diasbled
        elif key.lower() == 'p':  # toggle cell image
            self.show_img = not self.show_img
            self.update_cells()  # update cells
        elif key.lower() == 'r':  # generate scene with random cells
            self.cells = [[random.choice(ALL_CELLS)(row, col)
                           for col in range(CELLS)]
                          for row in range(CELLS)]
            self.update_cells()  # update cells
            self.update_labels()  # update labels
            self.scene_label.config(text='random', fg=LABEL_ENABLE)  # update
        elif key.lower() == 's':  # dump cells as scene to csv
            self.scene.dump_to_csv()
        elif key.lower() == 't':  # toggle tasks
            i = 0
            for task in self.task_labels:  # [task, info, True | False]
                if i == self.toggle_task:
                    task[2] = True  # enable
                    task[0].config(fg=LABEL_ENABLE)  # show as enabled
                else:
                    task[2] = False  # disable
                    task[0].config(fg=LABEL_DISABLE)  # show as enabled
                i += 1
            if self.toggle_task < len(self.task_labels) - 1:
                self.toggle_task += 1  # increment ...
            else:
                self.toggle_task = 0  # or reset
        else:
            with open(KEY, 'r') as f:
                showwarning('implemented key', f.read())  # open showinfo box

    def count_cells(self, cell_name):
        ''' returns the sum and percentatge of cell by name '''
        count = 0
        for row in self.cells:  # for all rows
            for cell in row:  # for all cols
                if cell.__class__.__name__ == cell_name:  # on same cell names
                    count += 1  # increase sum
        percentage = count / (CELLS * CELLS) * 100  # one decimal
        return '{:>03} - {:04.1f}%'.format(count, percentage)

    def get_cell_index(self, cell):
        ''' return the cell index as label text '''
        index = cell.get_index()  # get cell index
        if index == 0:
            text = ''
        elif index > 99:
            text = '+'
        elif index < -99:
            text = '-'
        else:
            text = str(index)
        return text

    def cell_info(self, event):
        cell = self.get_cell_clicked(event)  # get the cell
        if cell is None:
            self.status.set('hover cell for info')
        else:
            self.status.set(f'{cell}')

    def update_cells(self):  # update all cells
        for row in self.cells:  # for all cells
            for cell in row:
                self.update_cell(cell)  # udate cell

    def update_cell(self, cell):
        ''' update grid: cell color & cell index '''
        name = cell.__class__.__name__  # cell name
        rect, label, img = self.displayed_cells[cell.row][cell.col]  # get cell
        self.grid.itemconfigure(rect, fill=cell.get_color())  # update color
        text = self.get_cell_index(cell)  # get cell index
        color = 'black' if cell.is_dark() else 'white'
        self.grid.itemconfigure(label, text=text, fill=color)  # update label
        if self.show_img and name in self.images.keys():  # display gif image
            self.grid.itemconfigure(img, image=self.images[name])
        else:
            self.grid.itemconfigure(img, image=self.images['Blank'])

    def update_labels(self):
        for cell in self.cell_labels[1:]:  # update count of cell labels
            count = self.count_cells(cell[1])  # sum of same cell
            cell[0].config(text=count)  # update cell label sum

    def print_cells(self):
        ''' debug only: console output of cells '''
        print('cells:', sum(len(row) for row in self.cells))
        for row in self.cells:
            for cell in row:
                print(f' {cell!r}', end='')  # use __repr__
            print()

    def about(self):
        collaboration = ''
        for task in self.all_tasks:
            modul = importlib.import_module("tasks." + task)
            collaboration += task
            collaboration += '\n' + modul.__description__
            collaboration += '\nby: ' + modul.__author__
            collaboration += '\n\n'
        showinfo('implemented tasks', collaboration)  # open showinfo box


if __name__ == '__main__':  # start PyCity Application
    pyCity = PyCity()  # create instance, True displays Howto Info Box
    pyCity.bind("<Escape>", lambda x: pyCity.destroy())  # esc key ends PyCity
    pyCity.mainloop()  # start main loop

    # import profile
    # profile.run('pyCity.mainloop()')  # with profiler
