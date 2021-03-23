# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:08:49 2021

This is a simple game of tic-tac-toe, featuring a human player and a computer
player. It operates via the command line. In its current version, the game 
is hard-coded to let the player go first, but that will be changed in a 
coming version. 

It starts by asking the player to make a move and displaying the board. 
The player will provide a row and a column, and the board will be updated.

The computer will then determine the 'ideal' play to make, by recursively trying
out each piece on the board and, assuming that both players play optimally,
finding the play which offers it the highest number of wins. It will then make
said play. 

The player and the computer will finish taking turns until one player wins,
or the board is full. 

Current issue: the computer player seems to be dumb, and frequently gets into
positions where even a reasonably savvy player can set up two possibilities for
victory at once. Bizarrely, this does not seem to be the case in the traditional
go-for-the-corner-and-hope-the-other-player-goes-for-the-center gambit.

The computer will take chances at immediate victory. This merits more checking, 
and will hopefully be fixed in the next version. 

Goals for next versions: 
    1. Improve player quality-of-life. Add restart option, add option to change 
       player order, etc. 
    2. Improve AI strategy. 
    3. Add GUI? 

"""

class tictactoe():
    def __init__(self,startup):
        self.startup = startup
        row = ['.','.','.']
        self.board = [row[:] for i in range(3)]
        #self.board = [[1,2,3],[4,5,6],[7,8,9]]
        if self.startup == 0 or self.startup == 'O': 
            self.comp_player_x = True # True is X
        else: 
            self.comp_player_x = False # False is O
        self.end = False # False
        self.winner = None
    def detect_win(self,*det_board): 
        if det_board: 
            check_board = det_board[0]
        else: 
            check_board = self.board
        for i in range(len(check_board)):
            if check_board[i] == ['X','X','X'] or check_board[i] == ['O','O','O']: 
                return check_board[i][0]
            #print('ayyyy')
            #print(check_board)
            colboard = [check_board[j][i] for j in range(3)]
            #print(colboard)
            if colboard == ['X','X','X'] or colboard == ['O','O','O']:
                return colboard[0]
        diag_one = [check_board[0][0], check_board[1][1],check_board[2][2]]
        diag_two = [check_board[0][2], check_board[1][1],check_board[2][0]]
        if diag_one == ['X','X','X'] or diag_two == ['X','X','X']:
            return 'X'
        if diag_one == ['O','O','O'] or diag_two == ['O','O','O']:
            return 'O'
        return None
    
    def detect_end(self,*det_board):
        if det_board:
            check_board = det_board[0]
        else: 
            check_board = self.board
        for row in check_board:
            for col in row: 
                if col not in ['O','X']:
                    return False
        return True
    
    def determine_stop(self): 
        winner = self.detect_win()
        end = self.detect_end()
        if winner != None: 
            return [True,winner]
        return [end,None]
    
#for recurs_getwin
# go through board, find first empty space

# play whoplays (x or o) on that space
# repeat process with opposite of whoplays
# continue alternating until a winner is found or the board is full
# restart from first recursion, using the next empty space. 

# if a square would win the game for X or O,  add 1 to the respective X/O score
# add the row and col to a list of immediate wins
# if a square would not win a game AND the board is full, add 1 to the tie score
# and add the row and col to a list of terminal ties

# after the last square of the board [ie, both row and col are 2], find the best
# move using the following priorities
# 1. Which squares immediately win
# 2. Which square prevents an immediate loss
# 3. Which square has the fewest future losses



# if no winner is found and the board is not full

    def recurs_getwin(self,proj_board,whoplays,*is_output):
        if not is_output: 
            output = False
        else: 
            output = True
        bestsquare = [0,0]
        squarelist = {}
        windict = {'X':0,'O':0,'.':0}
        immediatewins = []
        immediatelosses = []
        
        if self.detect_end(proj_board) or self.detect_win(proj_board): # see if the board is full
            return 0 # if so, return a number saying so

        
        if whoplays: 
            player_sym = "X"
            n_player_sym = 'O'
        else: 
            player_sym = "O"
            n_player_sym = 'X'
        
        for row in range(len(proj_board)):  # go through rows
            for col in range(len(proj_board[row])):  # go through columns
                #print((row,col))
                if proj_board[row][col] not in ['X','O']:  # if you find a blank space
                    work_board = [i[:] for i in proj_board] # create a duplicate board
                    work_board[row][col] = player_sym # make the select square the symbol
                    #print(work_board)
                    #print(proj_board)
                    is_win = self.detect_win(work_board) #see if that square wins the game
                    #print(self.detect_end(work_board))
                    if is_win:  # if so
                        immediatewins.append((row,col)) # add that to the list of immediate wins
                        windict[player_sym] += 1 #and add that to the wins for this configuration
                        squarelist[(row,col)] = {player_sym:1, n_player_sym:0, '.': 0}
                    elif not self.detect_end(work_board): # if this doesn't decide the game 
                        
                        nwhoplays = not whoplays # switch players
                        next_player = self.recurs_getwin(work_board,nwhoplays) #test with other player
                        #print(next_player)
                        other_ideal_play = next_player[0] # find what the other player will play
                        
                        other_ideal_windict = next_player[1] # find possible outcomes for other player
                        other_ideal_immediatewins = next_player[2] # see if the other player has any immediate wins in this position
                        
                        squarelist[(row,col)] = other_ideal_windict #get stats for the ideal play
                        immediatelosses.extend(other_ideal_immediatewins) #see if this config makes a loss
                        
                    else: # if the workboard, as it is, is full and no win will result: 
                        #windict['.'] += 1
                        squarelist[(row,col)] = {'X':0,'O':0,'.':1}
        #after finishing all possible squares
        
        
        firstone = squarelist[list(squarelist.keys())[0]]
        #print(firstone)
        #print(squarelist)
        fewest_losses = firstone[n_player_sym]
        
        
        for square_option in squarelist.keys():
            square_info = squarelist[square_option]
            if type(square_info) == str: 
                continue
            #print(square_info.keys())
            windict['X'] += square_info['X'] 
            windict['O'] += square_info['O']
            windict['.'] += square_info['.']
            if square_info[n_player_sym] <= fewest_losses: 
                bestsquare = square_option
                    
            if immediatewins!= []: 
                bestsquare = immediatewins[0]
            elif immediatelosses != []:
                bestsquare = immediatelosses[0]
        if output: 
            print(squarelist)
        return [bestsquare,windict,immediatewins]
    
    def get_player_input(self,row,col):
        if self.board[row][col] != '.':
            print('That square is taken! Try another one')
            return False
        elif self.comp_player_x:
            self.board[row][col] = 'O'
        else: 
            self.board[row][col] = 'X'
        #print('I am placing a value for you, buddy!')
        #self.display_board()
        return True
    def display_board(self): 
        for i in range(2): 
            print('%s|%s|%s' % tuple(str(self.board[i][k]) for k in range(3)))
            print('=+=+=')
        print('%s|%s|%s' % tuple(str(self.board[2][k]) for k in range(3)))
    def computer_move(self): 
        best_move = self.recurs_getwin(self.board,self.comp_player_x)
        row = best_move[0][0]
        col = best_move[0][1]
        #print('first one')
        #print(row)
        #print(col)
        #self.display_board()
        if self.comp_player_x == True:
            self.board[row][col] = 'X'
        else: 
            self.board[row][col] = 'O'
        #self.display_board()
        #print('Why?')
    def run_a_game(self): 
        print('Welcome to Tic Tac Toe!')
        stoppoint = self.determine_stop()
        player_goes_first = not self.comp_player_x
        startup = True
        while stoppoint[0] == False: 
            if player_goes_first: 
                row = 'a'
                col = 'b'
                pinput = False
                if startup:
                    self.display_board()
                    print('-------------------')
                    startup = False
                print('Make Your Move!')
                while pinput == False:
                    while row not in [0,1,2]: 
                        row = int(input("Type in your row: "))
                        if row not in [0,1,2]: 
                            print('Try that again. It has to be between 0 and 2')
                    while col not in [0,1,2]: 
                        col = int(input("Type in your column: "))
                        if col not in [0,1,2]: 
                            print('Try that again. It has to be between 0 and 2')
                    pinput = self.get_player_input(row,col)
                    if not pinput: 
                        row = 'a'
                        col = 'b'
            else:
                print('Computer is thinking...')
                if startup: 
                    startup = False
                self.computer_move()
            
            self.display_board()
            print('----------------')
            player_goes_first = not player_goes_first
            stoppoint = self.determine_stop()
            
        if stoppoint[1] != None:
            print(stoppoint[1] + " won!")
        else: 
            print('It\'s a tie!')
            
        
        
                
        
                        
                    
                        
                    
                    
                    

                        
                    
                
                
                
                
#rowwins = [[['O','O','O'],['.','.','.'],['.','.','.']],
#           [['.','.','.'],['X','X','X'],['.','.','.']],
#           [['.','.','.'],['.','.','.'],['X','X','X']]]

#colwins = [[['O','2','3'],['O','5','6'],['O','8','9']],
#           [['.','X','.'],['.','X','.'],['.','X','.']],
#           [['.','.','X'],['.','.','X'],['.','.','X']]]

#diagwins = [[['X','.','.'],['.','X','.'],['.','.','X']],
#            [['.','.','X'],['.','X','.'],['X','.','.']]]

myboard = tictactoe(1)
myboard.run_a_game()

#checkit = [[['.','.','.'],['.','.','.'],['.','.','.']]]
#for i in checkit: 
#    myboard.board = i
#    wincount = myboard.recurs_getwin(myboard.board,myboard.comp_player_x)
#    print(myboard.comp_player_x)
#    print(wincount)