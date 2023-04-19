InfProg2 - P05 - PyCity

Develop a simulation application that contains a surface of 30x30 fields.
Each field contains a typical city structure: empty land, water, residential
house, business house, empty street, street with car, land with person, etc.
When the application runs, the field is updated once per update interval,
e.g. 0.1 sec

1 add your own fields:
  - within cells.Cells.py
  - must use Cell as superclass
  - describe the index argument and increase / decrease
  - add your own attributes to define your field, e.g. burnable (see Tree)
  - you might want to delete existing cells if not used, e.g. Sand
    - also delete tasks that use this cell
    - also delete scene csv file that define this cell
  - leave the cell Hole (used to get a blank scene)    

2 program the tasks: 4 out of 5
  - tasks.DynamicEconomy
  - tasks.GrowingPopulation
  - tasks.MovingCar
  - tasks.PublicSafty
  - tasks.VirusCondanimation

  - program the method def do_task(self, cell=None)
    - cell is specified on mouse click only, None otherwise
      manipulate cell (do so within do_task method)
      - use self.get_random_cell()
      - or  self.get_random_cell(Hole) to get a specific cell      
  - manipulate cell(s) step by step (on each cycle)
  - call update(cell) if instance of cell changes (see FishFight) 
  - no return

  - you might want do delete the existing tasks:
    - FireBlaze: your burnable cells will catch fire and 
                 turn into chark and recover as tree after
                 specified age index
    - JungleReturning: destroys step by step all your cells
                       and trees start growing instead. 

3 add your own tasks: min 2
  - use a separate file for each Task class
    - has to be in the folder tasks  
    - use Task as superclass
    - must implement the method: def do_task(self, cell)

4 validate syntax and verify code quality 
  - pylama, lint within Spyder
  - Superflake-linter on https://160.85.252.148:9092
    - code quality must not 100% match all rules
    - linter rules hard


  