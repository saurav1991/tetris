######################################################################
#                                                                    #
# 	Text-based Tetris game in Python 3.	     
######################################################################
###########
#  Imports
###########
import os
from random import randint
import sys

###################
# Board and pieces 
####################
BOARD_SIZE = 20
board = [[ 0 for x in range(BOARD_SIZE) ] for y in range(BOARD_SIZE)]
pieces = [ [[1],[1],[1],[1]],
		   [[1, 0],[1, 0],[1, 1]], 
		   [[0, 1],[0, 1],[1, 1]], 
		   [[0, 1], [1, 1], [1, 0]],    
		   [[1, 1], [1, 1]], ]
currentPiece = []     # for current piece that is not yet placed.
currentPieceLocation = []  # location of current piece


#############################
#  Draw the board and pieces
##############################
def draw_screen(errorMsg):
	os.system('clear')
	print(" \t\tTetris Game\n\n\n\n ")
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			if(board[y][x] !=0):
				print(" ", "*", " ",end="")
			else:
				print("  _  ",end="")
		print(" \n ")
	print("Moves:\n   a: move piece left \n   d: move piece right\n   w: rotate piece counter clockwise\n   s: rotate piece clockwise\n  q: quit the game")
	if(errorMsg == False):
		print("Not a Valid Move, Try Again!")

###########################
#  Generate new pieces
###########################
def generate_piece():
	global currentPiece
	global currentPieceLocation
	currentPiece = []
	currentPieceLocation = []
	pieceType = randint(0,4)
	currentPiece = pieces[pieceType]
	x = int((BOARD_SIZE-len(pieces[pieceType][0]))/2)
	currentPieceLocation.append(x)
	currentPieceLocation.append(0)
	# Determine the location of the piece
	for x in range(currentPieceLocation[0], currentPieceLocation[0]+len(currentPiece)):
		for y in range(currentPieceLocation[1],currentPieceLocation[1]+len(currentPiece[0])):			
			if(currentPiece[x-currentPieceLocation[0]][y-currentPieceLocation[1]] != 0):	
				if(board[x][y]==1):
					print("Game Over!") #Game over if no place for a new piece
					sys.exit()
				else:
					board[x][y] = 8		#Denote cell occupied
			

######################################################
#  Re-drawing the board after translations of pieces
######################################################
def redraw_board():
	# Remove previous current piece from the previous location on the board.
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			if(board[y][x]==8):
				board[y][x] = 0
	
	# Draw the current piece at the new location.
	for x in range(currentPieceLocation[0], currentPieceLocation[0]+len(currentPiece)):
		for y in range(currentPieceLocation[1],currentPieceLocation[1]+len(currentPiece[0])):			
			if(currentPiece[x-currentPieceLocation[0]][y-currentPieceLocation[1]] != 0):	
				board[x][y] = 8


###########################################################################
#  For rotating direction of pieces (1 - clockwise, 2 - counter-clockwise)
###########################################################################
def rotate_piece(direction):  
	global currentPiece
	# Remove current shape from the board before creating a rotated piece 
	for x in range(BOARD_SIZE):			
		for y in range(BOARD_SIZE):
			if(board[y][x] == 8):
				board[y][x] = 0
	# Rotate piece
	if(direction == 1):
		currentPiece = [ [ currentPiece[y][x] for y in range(len(currentPiece)) ] for x in range(len(currentPiece[0]) - 1, -1, -1) ]
	else:
		currentPiece = [ [ currentPiece[y][x] for y in range(len(currentPiece)) ] for x in range(0, len(currentPiece[0]))]	



###########################################################################
#  Game-play (continues until 'q' or 'Q' is pressed, or the game is over!)
###########################################################################
def gamePlay():
	flag=0
	global currentPieceLocation
	global currentPiece
	ch = None
	isMoveValid = True
	while(ch != 'q' and ch != 'Q'):

		draw_screen(isMoveValid)		
		isMoveValid = True
		ch = input()
	#	draw_screen(isMoveValid)
		# Check if any row can be deleted
		for x in range(BOARD_SIZE):
			rowDelete = True
			for y in range(BOARD_SIZE):
				if(board[y][x] != 1):
					rowDelete = False
			# Move rows downwards
			if(rowDelete == True):
				for j in range(y-1,1,-1):
					for i in range(BOARD_SIZE):
						board[i][j] = board[i][j-1]
		redraw_board()


		if(ch == 'w' or ch == 's' ):
			if(ch == 's'):
				rotate_piece(1)			#Rotate clockwise
			else:
				rotate_piece(2)
			x = int((BOARD_SIZE-len(currentPiece[0]))/2)
			for x in range(currentPieceLocation[0], currentPieceLocation[0]+len(currentPiece)):
				for y in range(currentPieceLocation[1],currentPieceLocation[1]+len(currentPiece[0])):
					if(currentPiece[x-currentPieceLocation[0]][y-currentPieceLocation[1]] != 0):	
						board[x][y] = 8
			draw_screen(isMoveValid)
		
		# Move the current piece to the left
		if(ch == 'a'):
		#Check if it is possible
			flag = 0
			#Check for boundaries 		
			if(currentPieceLocation[0] == 0):
				flag=1
				
				
			#Check if it overlaps with other pieces
			for x in range(len(currentPiece)):
				for y in range(len(currentPiece[0])):
					if(currentPiece[x][y] != 0):
						if(board[currentPieceLocation[0]+x-1][currentPieceLocation[1]+y] == 1):
							flag = 1
			# Peform translation if possible
			if(flag == 0):			
				for x in range(len(currentPiece)):
					for y in range(len(currentPiece[0])):
						if(currentPiece[x][y] != 0):		
							board[currentPieceLocation[0]+x-1][currentPieceLocation[1]+y] = board[currentPieceLocation[0]+x][currentPieceLocation[1]+y]
				currentPieceLocation[0] -= 1	#Update location of piece as per the translation
				redraw_board()
			else:
				isMoveValid = False

		# Move the current piece to the right
		elif(ch == 'd'):
		# Check if moving right is possible
			flag = 0
			#Check for boundaries		
			if(currentPieceLocation[0] + len(currentPiece)== BOARD_SIZE):
				flag=1
				
			#Check if it overlaps with other pieces
			try:
				if(flag==0):
					for x in range(len(currentPiece), 0, -1):
						for y in range(len(currentPiece[0]), 0, -1):
							if(currentPiece[x-1][y-1] != 0):
								if(board[currentPieceLocation[0]+x][currentPieceLocation[1]+y-1] == 1):
									flag = 1
						
			except:
				flag=1

			# Peform translation if possible
			if(flag == 0):			
				for x in range(len(currentPiece)-1,0,-1):
					for y in range(len(currentPiece[0])-1,0,-1):
						if(currentPiece[x-1][y-1] != 0):				
							board[currentPieceLocation[0]+x+1][currentPieceLocation[1]+y] = board[currentPieceLocation[0]+x][currentPieceLocation[1]+y]
				currentPieceLocation[0] += 1 #Update location of piece as per the translation
				redraw_board()
			else:
				isMoveValid = False
			
		
	# The current piece moves down at every Valid Move
		if(isMoveValid == True or ch == '' or ch == ' ' ):
		
		            #Check if it is possible to move piece down
				flag=0
				#Check for boundaries
				if(currentPieceLocation[1] + len(currentPiece[0])== BOARD_SIZE):
					flag=1
			
				#check whether it will overlap with other pieces
				try:
					if(flag==0):
						for x in range(len(currentPiece), 0, -1):
							for y in range(len(currentPiece[0]), 0, -1):
								if(currentPiece[x-1][y-1] != 0):
									if(board[currentPieceLocation[0]+x-1][currentPieceLocation[1]+y] == 1):
										flag = 1
				except:
					flag = 1

				# Move the current piece a step down
				if(flag==0):
					for x in range(len(currentPiece),0,-1):
						for y in range(len(currentPiece[0]),0,-1):
							if(currentPiece[x-1][y-1] != 0):				
								board[currentPieceLocation[0]+x-1][currentPieceLocation[1]+y] = board[currentPieceLocation[0]+x-1][currentPieceLocation[1]+y-1]
					currentPieceLocation[1] += 1	
					redraw_board()

	    # Fix position of current piece(if it has gone all the way down)
		flag=0

		#Check for boundaries		
		if(currentPieceLocation[1] + len(currentPiece[0])== BOARD_SIZE):
			flag=1
			
		#check if going furhter down is possible
		try:
			if(flag==0):
				for x in range(len(currentPiece), 0, -1):
					for y in range(len(currentPiece[0]), 0, -1):
						if(currentPiece[x-1][y-1] != 0):
							if(board[currentPieceLocation[0]+x-1][currentPieceLocation[1]+y] == 1):
								flag = 1
		except:
			flag = 1

		# Fix the position of the current piece if going down no more possible					
		if(flag==1):
			
			for x in range(len(currentPiece)):
				for y in range(len(currentPiece[0])):
					if(board[currentPieceLocation[0]+x][currentPieceLocation[1]+y] == 8):
						board[currentPieceLocation[0]+x][currentPieceLocation[1]+y] = 1						
			generate_piece() # Generate the new piece once the current piece's location is fixed on the board 
	
# Start the game
generate_piece()
gamePlay()
