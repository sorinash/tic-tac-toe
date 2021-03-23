

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
