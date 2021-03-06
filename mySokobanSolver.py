
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and results in a fail for the test of your code.
This is not negotiable! 


'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (10107321, 'Ho Fong', 'Law'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    X,Y = zip(*warehouse.walls) # pythonic version of the above
    x_size, y_size = 1+max(X), 1+max(Y)
    
    xSymbolList = []
    strPuzzle = [[" "] * x_size for y in range(y_size)]
    
    for (x,y) in warehouse.walls:
            strPuzzle[y][x] = "#"
            
    for x in range(warehouse.ncols):
        for y in range(warehouse.nrows):
            if not [x,y] in warehouse.walls and not [x,y] in warehouse.targets:
                if [x-1,y] in warehouse.walls or [x-1,y] in xSymbolList:
                    if [x,y-1] in warehouse.walls or [x,y-1] in xSymbolList:
                        xSymbolList.append([x,y]) 
                        break
                    if [x,y+1] in warehouse.walls or [x,y+1] in xSymbolList:
                        xSymbolList.append([x,y])  
                        break
                if [x+1,y] in warehouse.walls or [x+1,y] in xSymbolList:
                    if [x,y-1] in warehouse.walls or [x,y-1] in xSymbolList:
                        xSymbolList.append([x,y]) 
                        break
                    if [x,y+1] in warehouse.walls or [x,y+1] in xSymbolList:
                        xSymbolList.append([x,y])  
                        break
                    
    for (x,y) in xSymbolList:
            strPuzzle[y][x] = "X"
    
    return "\n".join(["".join(line) for line in strPuzzle])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    
    def __init__(self, warehouse):
        self.allow_taboo_push = True
        self.macro = True
        self.walls = warehouse.walls
        self.targets = warehouse.targets
        self.boxes = warehouse.boxes
        self.worker = warehouse.worker

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        
        listOfActions = []
        if self.macro:
            for sequence in solve_sokoban_macro(self):
                if check_elem_action_seq(self,sequence) == 'Impossible':
                    break
                elif check_elem_action_seq(self,sequence):
                    if self.allow_taboo_push:
                        listOfActions.append(sequence)
                    else:
                        #taboo check 
                else:
                    if self.allow_taboo_push:
                        listOfActions.append(sequence)
                    else:
                        #taboo check 
        else:
            for sequence in solve_sokoban_elem(self):
                if check_elem_action_seq(self,sequence) == 'Impossible':
                    break
                elif check_elem_action_seq(self,sequence):
                    if self.allow_taboo_push:
                        listOfActions.append(sequence)
                    else:
                        #taboo check 
                else:
                    if self.allow_taboo_push:
                        listOfActions.append(sequence)
                    else:
                        #taboo check 
        return listOfActions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    vaild = True
    for step in action_seq:
        x = warehouse.worker[0]
        y = warehouse.worker[1]
        if step == 'Left':
            if [x-1,y] in warehouse.boxes:
                if [x-2,y] in warehouse.boxes:
                    vaild = False
                    break
            elif [x-1,y] in warehouse.walls:
                vaild = False
                break
            else:
                x = x-1
        if step == 'Right':
            if [x+1,y] in warehouse.boxes:
                if [x+2,y] in warehouse.boxes:
                    vaild = False
                    break
            elif [x+1,y] in warehouse.walls:
                vaild = False
                break
            else:
                x = x+1
        if step == 'Up':
            if [x,y-1] in warehouse.boxes:
                if [x,y-2] in warehouse.boxes:
                    vaild = False
                    break
            elif [x,y-1] in warehouse.walls:
                vaild = False
                break
            else:
                y = y-1
        if step == 'Down':
            if [x,y+1] in warehouse.boxes:
                if [x,y+2] in warehouse.boxes:
                    vaild = False
                    break
            elif [x,y+1] in warehouse.walls:
                vaild = False
                break
            else:
                y = y-2
    if vaild:
        return warehouse.__str__()
    else:
        return "Impossible"
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    
    In this scenario, the cost of all (elementary) actions is one unit.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    
    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    
    The ith box is initially at position 'warehouse.boxes[i]'.
        
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

