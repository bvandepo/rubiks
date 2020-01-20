#!/usr/bin/python3
'''
               ----------------
               | 0  | 1  | 2  |
               ----------------
               | 3  |YELL| 5  |
               ----------------
               | 6  | 7  | 8  |
               ----------------
-------------------------------------------------------------
| 9  | 10 | 11 | 18 | 19 | 20 | 27 | 28 | 29 | 36 | 37 | 38 |
-------------------------------------------------------------
| 12 |BLUE| 14 | 21 |RED | 23 | 30 |GREE| 32 | 39 |ORAN| 41 |
-------------------------------------------------------------
| 15 | 16 | 17 | 24 | 25 | 26 | 33 | 34 | 35 | 42 | 43 | 44 |
-------------------------------------------------------------
               ----------------
               | 45 | 46 | 47 |
               ----------------
               | 48 |WHIT| 50 |
               ----------------
               | 51 | 52 | 53 |
               ----------------
               
Moves notations:

FCW  : turn the whole tube CLOCKWISE when looking at the FRONT face
FCCW : turn the whole tube CONTER CLOCKWISE when looking at the FRONT face
UCW  : turn the whole tube CLOCKWISE when looking at the UPPER face
UCCW : turn the whole tube CONTER CLOCKWISE when looking at the UPPER face
MCW  : while holding the DOWN face, rotate the two upper layers CLOCKWISE
MCCW : while holding the DOWN face, rotate the two upper layers CLOCKWISE

'''

map_moveToCode = {'FCW':0,'FCCW':1,'UCW':2,'UCCW':3,'MCW':4,'MCCW':5}
map_codeToMove = ['FCW','FCCW','UCW','UCCW','MCW','MCCW']
#from IPython import embed
from rubik_solver import utils

def rotate_front_CCW(faces):
  '''Rotate the cube 90deg CCW around the front face'''
  new_faces = faces.copy()
  new_faces['U'] = faces['R']
  new_faces['R'] = faces['D']
  new_faces['D'] = faces['L']
  new_faces['L'] = faces['U']
  return new_faces
  
def rotate_front_CW(faces):
  '''Rotate the cube 90deg CW around the front face'''
  new_faces = faces.copy()
  new_faces['U'] = faces['L']
  new_faces['R'] = faces['U']
  new_faces['D'] = faces['R']
  new_faces['L'] = faces['D']
  return new_faces
  
def rotate_upper_CCW(faces):
  '''Rotate the cube 90deg CCW around the upper face'''
  new_faces = faces.copy()
  new_faces['F'] = faces['L']
  new_faces['L'] = faces['B']
  new_faces['B'] = faces['R']
  new_faces['R'] = faces['F']
  return new_faces
  
def rotate_upper_CW(faces):
  '''Rotate the cube 90deg CW around the upper face'''
  new_faces = faces.copy()
  new_faces['F'] = faces['R']
  new_faces['L'] = faces['F']
  new_faces['B'] = faces['L']
  new_faces['R'] = faces['B']
  return new_faces





def solve(cube):
  #call the solver
  sol_raw = utils.solve(cube, 'Kociemba')
  sol = []
  #initial orientation of the cube (can not be changed)
  faces = {'U':'Y',
           'L':'B',
           'F':'R',
           'R':'G',
           'B':'O',
           'D':'W'}
         
  #rename the face with the center color         
  #and decompose double rotation as two signle rotations
  for move in sol_raw:
    move_string = faces[move.face]
    if move.counterclockwise:
      move_string = move_string + "'"
    sol.append(move_string);
    if move.double:
      sol.append(move_string);
  #translate the solution into moves that the robot can execute
  moves = []
  for m in sol:
    f=m[0] # the face we want do be facing down
    print (faces)
    if faces['U'] == f:
      faces = rotate_front_CW(faces); moves.append('FCW')
      faces = rotate_front_CW(faces); moves.append('FCW')
    elif faces['L'] == f:
      faces = rotate_front_CCW(faces); moves.append('FCCW')
    elif faces['F'] == f:
      faces = rotate_upper_CCW(faces); moves.append('UCCW')
      faces = rotate_front_CW(faces); moves.append('FCW')
    elif faces['R'] == f:
      faces = rotate_front_CW(faces); moves.append('FCW')
    elif faces['B'] == f:
      faces = rotate_upper_CW(faces); moves.append('UCW')
      faces = rotate_front_CW(faces); moves.append('FCW')
    if "'" in m:
      faces = rotate_upper_CCW(faces); moves.append('MCCW')
    else:
      faces = rotate_upper_CW(faces); moves.append('MCW')
  print ("solved in {} moves".format(len(moves)))
  return moves

def main(args):
    #cube = 'wowgybwyogygybyoggrowbrgywrborwggybrbwororbwborgowryby'
    cube = 'yyyyyyyyyooobbbooobbbrrrbbbrrrgggrrrgggooogggwwwwwwwww'
    solve(cube)
    # ~ try:
       # ~ solve(cube)
    # ~ except:
       # ~ print ("Not able to solve")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

