from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys

#====================================================================================

char_goal = '1'
char_single = '2'


class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation
        
       

        # if is_goal is false & is_single is false & orientation is not None then the piece is 1x2/2x1

    #use this function after using a is_empty function to check if movement is possible

        


    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)



class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()
        


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'
  

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()
    
    def find_empty_space(self):
        self.empty_space = []
        for i in range(self.height):
            for j in range(self.width):
                #print(self.grid[i][j])
                if self.grid[i][j]== '.':
                    self.empty_space.append([i,j])
        return self.empty_space

    def find_goal_piece(self):
        for piece in self.pieces: 
            if piece.is_goal:
                return piece

    def manhattan(self):
        piece = self.find_goal_piece()
        val =  abs(piece.coord_x - 1) + abs(piece.coord_y - 3)
        return val 
    
    def heuristic(self,g): 
        h = self.manhattan()
        f = h+g
        return f

    def __repr__(self) -> str: 
        grid_string = ''
        for line in self.grid:
            for char in line:  
                grid_string += char # add the character to the result
            grid_string += '\n' # add a new line at the end of each line
        grid_string = grid_string[:-1] # remove the last '\n'

        return grid_string

    def __hash__(self) -> int:
        return hash(self.__repr__()) # hash the string representation of the board


    
    '''create a function that converts board.grid to a string and then hash it'''




                    

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        self.id = hash(board)  # The id for breaking ties.
    
    def is_goal_state(self):
        #i think a state is the whole board not just a single piece
        self.goal_state = False
        #change this if grid numbering is diff
        piece = self.board.find_goal_piece() #we dont put self cuz we already have self.blahblahblah
        if piece.is_goal == True and piece.coord_x == 1 and piece.coord_y == 3:
            self.goal_state = True
        return self.goal_state 
    
    def state_successor(self,pos):
        piece = self.board.pieces[pos]
        empty_list = self.board.find_empty_space()
        successor_list = []
        # if y of horz pieces match, and empty is -1 away or +2 away (x dir) you can move
        # if x of vert pieces match and empty is -1 or +2 away (y dir) you can move
        # if empty piece is next to each other and +2 0r -1 away from 2x2 piece, you can move
        # if single piece is -1 or +1 away in both x and y direction, you can move
        #####
        # horz
        # you will probably have to have a whole loop here to loop through all the pieces
       # print(piece)
        if piece.orientation == 'h':
            b = piece.coord_x 
            a = piece.coord_y
            for i in range (2):
                if a == empty_list[i][0]:
                    if (b)-1 == empty_list[i][1]:
                        # dont move the piece before swapping cuz itll fuck up the coordinates
                        # here we know were about to make a swap so we need to make a copy
                        copy1 = deepcopy(self.board)
                        self.swap(copy1.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy1.grid,[a,b],[a,b+1])
                        self.move_piece(copy1.pieces[pos],'left')
                        #here we moved around the pieces and now have to generate a state
                        # g is the cost function which is depth and its parent_depth+1
                        # heuristic is f which is h meaning we have to call the manhattan distance function
                        #were gonna create a function to do all the calc for heuristic
                        f = copy1.heuristic(self.depth+1)
                        state1 = State(copy1, f, self.depth+1, self)
                        successor_list.append(state1)
                        
                    if (b)+2 == empty_list[i][1]:
                        copy2 = deepcopy(self.board)
                        self.swap(copy2.grid,[a,b+1],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy2.grid,[a,b],[a,b+1])
                        self.move_piece(copy2.pieces[pos],'right')
                        f = copy2.heuristic(self.depth+1)
                        state2 = State(copy2, f, self.depth+1, self)
                        successor_list.append(state2)
                        
                    #move horizontally up and down:
                if b == empty_list[i][1] and b +1 == empty_list[1-i][1]:
                    if (a)-1 == empty_list[i][0] and a -1 == empty_list[i-1][0]:
                        copy3 = deepcopy(self.board)
                        self.swap(copy3.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy3.grid,[a,b+1],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy3.pieces[pos],'up')
                        f = copy3.heuristic(self.depth+1)
                        state3 = State(copy3, f, self.depth+1, self)
                        successor_list.append(state3)
                        
                    if a+1 == empty_list[i][0] and a +1 == empty_list[i-1][0]:
                        copy4 = deepcopy(self.board)
                        self.swap(copy4.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy4.grid,[a,b+1],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy4.pieces[pos],'down')
                        f = copy4.heuristic(self.depth+1)
                        state4 = State(copy4, f, self.depth+1, self)
                        successor_list.append(state4)
                        
            return successor_list

        elif piece.orientation == 'v':
            b = piece.coord_x 
            a = piece.coord_y
            #(a,b)
            for i in range (2):
                if b == empty_list[i][1]:
                    if (a)-1 == empty_list[i][0]:
                        copy1 = deepcopy(self.board)
                      
                        self.swap(copy1.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy1.grid,[a,b],[a+1,b])
                        self.move_piece(copy1.pieces[pos],'up')
                        f = copy1.heuristic(self.depth+1)
                        state1 = State(copy1, f, self.depth+1, self)
                        successor_list.append(state1)

                    if (a)+2 == empty_list[i][0]:
                        copy2 = deepcopy(self.board)
                        self.swap(copy2.grid,[a+1,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy2.grid,[a,b],[a+1,b])
                        self.move_piece(copy2.pieces[pos],'down')
                        f = copy2.heuristic(self.depth+1)
                        state2 = State(copy2, f, self.depth+1, self)
                        successor_list.append(state2)
                #left and right:
                if a == empty_list[i][0] and a+1 == empty_list[1-i][0]:
                    if b-1 == empty_list[i][1] and b-1 == empty_list[1-i][1]:
                        copy3 = deepcopy(self.board)
                        self.swap(copy3.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy3.grid,[a+1,b],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy3.pieces[pos],'left')
                        f = copy3.heuristic(self.depth+1)
                        state3 = State(copy3, f, self.depth+1, self)
                        successor_list.append(state3)
                    if b+1 == empty_list[i][1] and b+1 == empty_list[1-i][1]:
                        copy4 = deepcopy(self.board)
                        self.swap(copy4.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy4.grid,[a+1,b],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy4.pieces[pos],'right')
                        f = copy4.heuristic(self.depth+1)
                        state4 = State(copy4, f, self.depth+1, self)
                        successor_list.append(state4)
            return successor_list

        elif piece.is_goal :
            b = piece.coord_x 
            a = piece.coord_y
            for i in range (2):
                #can move horizontally
                if piece.coord_y == empty_list[i][0] and piece.coord_y+1 == empty_list[1-i][0]:
                    if (piece.coord_x)-1 == empty_list[i][1] and piece.coord_x -1 == empty_list[1-i][1]:
                        copy1 = deepcopy(self.board)
                        self.swap(copy1.grid,[a,b+1],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy1.grid,[a+1,b+1],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy1.pieces[pos],'left')
                        f = copy1.heuristic(self.depth+1)
                        state1 = State(copy1, f, self.depth+1, self)
                        successor_list.append(state1)

                    if (piece.coord_x)+2 == empty_list[i][1] and piece.coord_x +2 == empty_list[1-i][1]:
                        copy2 = deepcopy(self.board)
                        self.swap(copy2.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy2.grid,[a+1,b],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy2.pieces[pos],'right')
                        f = copy2.heuristic(self.depth+1)
                        state2 = State(copy2, f, self.depth+1, self)
                        successor_list.append(state2)

                #can move vertically
                if piece.coord_x == empty_list[i][1] and piece.coord_x +1 == empty_list[1-i][1]:
                    if (piece.coord_y)-1 == empty_list[i][0] and piece.coord_y -1 == empty_list[i-1][0]:
                        copy3 = deepcopy(self.board)
                        self.swap(copy3.grid,[a+1,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy3.grid,[a+1,b+1],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy3.pieces[pos],'up')
                        f = copy3.heuristic(self.depth+1)
                        state3 = State(copy3, f, self.depth+1, self)
                        successor_list.append(state3)

                    if (piece.coord_y)+2 == empty_list[i][0] and piece.coord_y +2 == empty_list[i-1][0]:
                        copy4 = deepcopy(self.board)
                        self.swap(copy4.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.swap(copy4.grid,[a,b+1],[empty_list[1-i][0],empty_list[1-i][1]])
                        self.move_piece(copy4.pieces[pos],'down')
                        f = copy4.heuristic(self.depth+1)
                        state4 = State(copy4, f, self.depth+1, self)
                        successor_list.append(state4)
            return successor_list

        elif piece.is_single: 
            b = piece.coord_x 
            a = piece.coord_y
            for i in range (2):
                #can move vertically
                if b == empty_list[i][1]:
                    if (a)-1 == empty_list[i][0]:
                        copy1 = deepcopy(self.board)
                        self.swap(copy1.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.move_piece(copy1.pieces[pos],'up')
                        f = copy1.heuristic(self.depth+1)
                        state1 = State(copy1, f, self.depth+1, self)
                        successor_list.append(state1)

                    if (a)+1 == empty_list[i][0]:
                        copy2 = deepcopy(self.board)
                        self.swap(copy2.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.move_piece(copy2.pieces[pos],'down')
                        f = copy2.heuristic(self.depth+1)
                        state2 = State(copy2, f, self.depth+1, self)
                        successor_list.append(state2)

                #can move horizontally
                if a == empty_list[i][0]:
                    if (b)-1 == empty_list[i][1]:
                        copy3 = deepcopy(self.board)
                        self.swap(copy3.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.move_piece(copy3.pieces[pos],'left')
                        f = copy3.heuristic(self.depth+1)
                        state3 = State(copy3, f, self.depth+1, self)
                        successor_list.append(state3)

                    if (b)+1 == empty_list[i][1]:
                        copy4 = deepcopy(self.board)
                        self.swap(copy4.grid,[a,b],[empty_list[i][0],empty_list[i][1]])
                        self.move_piece(copy4.pieces[pos],'right')
                        f = copy4.heuristic(self.depth+1)
                        state4 = State(copy4, f, self.depth+1, self)
                        successor_list.append(state4)

            return successor_list
    
       

    def move_piece(self,piece,new_loc):
        if new_loc == "right": 
            piece.coord_x +=1
        elif new_loc == "left":
            piece.coord_x -= 1
        elif new_loc == "down":
            piece.coord_y +=1
        elif new_loc == "up":
            piece.coord_y -= 1

    def swap(self,list, coord1, coord2):
        # coord 1/2 : list
        a1 = coord1[0]
        a2 = coord1[1]
        b1 = coord2[0]
        b2 = coord2[1]
        list[a1][a2], list[b1][b2] = list[b1][b2], list[a1][a2]

def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):

            if ch == '^': # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<': # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if g_found == False:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)
    
    return board

#write to file
'''given a board structured as a list, the function will write an output file with each index of the 
list being a line of text in the file. the board is structured as [[a,b,c],[d,e,f],[g,h,i]]'''
def write_to_file(state, filename):
    # open the file for writing
    with open(filename, 'w') as file:
        # for each row in the board
        for boards in state:
            for row in boards.board.grid:
                # convert the row to a string
                row_str = ''.join(row)
                # write the row to the file
                file.write(row_str + '\n')
            file.write('\n')


  #function for dfs 
'''given an initial state return the first solution (goal_state) found using
    DFS with pruning. succeessor nodes are determined using the state_successor function. this function
    takes in a state so w'''

def dfs(initial_state):
    #initializing the frontier and explored list
    frontier = []
    explored = set()
    #adding the initial state to the frontier
    frontier.append(initial_state)
    #while the frontier is not empty
    while frontier:
        #pop the first element in the frontier
        state = frontier.pop(0)
        #if the state is the goal state return the state
        if state.is_goal_state():
            path = []
            temp = state
            print(state)
            while temp.parent != None:
                '''backtrack through the parent of each state and add it to the path'''
                path.append(temp)
                temp = temp.parent
            path.append(temp)
            path = path[::-1]
            return path
            
        #if the state is not in the explored list
        if hash(state.board) not in explored:
            #add the state to the explored list
            explored.add(hash(state.board))
            #loop through each piece on the board and get their state_successor
            for pos in range(len(initial_state.board.pieces)):
                #get the state_successor for each piece
                successors = state.state_successor(pos)
                

                #add the successors to the frontier
                frontier = successors + frontier
      
               
    return None

'''given an initial state return the first solution (goal_state) found using A* with pruning. succeessor nodes are determined using the state_successor function. 
the heuristic function is used to determine the f value of each state.'''
def astar(initial_state):
    #initializing the frontier and explored list
    frontier = []
    explored = set()
    #adding the initial state to the frontier
    frontier.append(initial_state)
    #while the frontier is not empty
    while frontier:
        #sort the frontier based on the f value
        frontier.sort(key=lambda x: x.f)
        #pop the first element in the frontier
        state = frontier.pop(0)
        #if the state is the goal state return the state
        if state.is_goal_state():
            state.board.display()
            path = []
            temp = state
            print(state)
            while temp.parent != None:
                '''backtrack through the parent of each state and add it to the path'''
                path.append(temp)
                temp = temp.parent
            path.append(temp)
            path = path[::-1]
            return path
            
        #if the state is not in the explored list
        if hash(state.board) not in explored:
            #add the state to the explored list
            explored.add(hash(state.board))
            #state.board.display()
            #print("--------")
            #loop through each piece on the board and get their state_successor
            for pos in range(len(initial_state.board.pieces)):
                #get the state_successor for each piece
                successors = state.state_successor(pos)
                

                #add the successors to the frontier
                frontier = successors + frontier
      
               
    return None

def get_solution(state):
    path = []
    temp = state
    print(state)
    while temp.parent != None:
        '''backtrack through the parent of each state and add it to the path'''
        path.insert(0, temp)
        temp = temp.parent
    path.insert(0, temp)
    for i in path:
        i.board.display()
        print("--------")
    return path
    
 

if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board = read_from_file(args.inputfile)
    initial_state = State(board, 0, 0, None)
     #run the desired search algorithm
    if args.algo == 'astar':
        path = astar(initial_state)
        print(len(path))
    elif args.algo == 'dfs':
       path= dfs(initial_state)
       print(len(path))

    write_to_file(path, args.outputfile)
    