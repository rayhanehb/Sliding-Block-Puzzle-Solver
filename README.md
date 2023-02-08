# Sliding-Block-Puzzle-Solver
Hua Rong Dao Pass Sliding Block Puzzle Solver
The puzzle board is four spaces wide and five spaces tall. We will consider the variants of this puzzle with ten pieces. There are four kinds of pieces:

One 2x2 piece.
Five 1x2 pieces. Each 1x2 piece can be horizontal or vertical.
Four 1x1 pieces.
Once we place the ten pieces on the board, two empty spaces should remain. The pieces are denoted in the following convention in the solver:

* 2x2 piece:
*                     11
                      11
                    
                   
* 2x1 (horizontal and vertical):
*                < >  ^
                      v
                  
* 1x1 pieces:  2
* empty spaces: .

Together the pieces can create multiple board conventions. For example the following:

                      ^11^
                      v11v
                      ^<>^
                      v22v
                      2..2
         
The goal is to move the pieces until the 2x2 piece is above the bottom opening (i.e. helping Cao Cao escape through the Hua Rong Dao/Pass). Pieces can move  horizontally or vertically only into an available space and are not allowed to rotate any piece or move it diagonally.

The program will read a textfile with a puzzle initialized using the above convention and return a textfile with step by step solutions. The **optimal** solution is achieved using using ** A* ** algorithm. The program also allows solver to use DFS algorithm to show the difference between the solutions. 

* hrd.py is the program
* testhrd.txt holds a sample input file. 
* testhrd_sol.txt shows how the solution is outputed
