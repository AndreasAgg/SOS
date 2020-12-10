#   The game can be played to the console   #


from random import randint
from time import sleep
import os
from timeit import default_timer as timer
from math import ceil

clear_con = lambda: os.system('cls')


class Player():
    def __init__(self,name='',letter='',score=0):
        self.name = name
        self.letter = letter
        self.score = score
    
    def addScore(self, s): self.score += s

    def show(self):
        print('Player:',self.name,'\nWins:')


def dimension():
    #  Asks the user for the dimensions of the board
    #  4 -> (4x4), 5 -> (5x5), ...

    while True:
        clear_con()
        n = input('Choose dimensions: (4 - 10) ')
        try:
            n = int(n)
            if n < 4 or n > 10: raise Exception
            break

        except:
            continue
    clear_con()
    return n


def printBoard(b):
    # Input: b -> list
    # Prints the board

    rows_num = '\t\t  '
    for _ in range(1,n+1):
        rows_num = rows_num + f'  {_} '
    print(rows_num)
    r = '\t\t  ' + (4*n + 1)*'-' + '\n\t\t1 '
    count = 0
    for _ in range(1,n**2+1):
        if _ % n == 1: count += 1
        r = r + f'| {b[_]} '
        if _ != n**2 and _ % n == 0: 
            r = r + f'| {_ - (n-1)*count}\n\t\t' + '  ' +(4*n + 1)*'-' + f'\n\t\t{_ - (n-1)*count + 1} '
    print(r + f'| {n}\n\t\t  ' + (4*n + 1)*'-')
    print(rows_num + '\n\n')


def position(coordinates):
    # Input: coordinates -> list
    # Returns a number corresponding to the chosen row (coordinates[0]) and column (coordinates[1])
    return 1 + n*(coordinates[0] - 1) + coordinates[1] - 1


def movePlayer(b,P,triads_before):
    # Inputs:
    # b -> list
    # P -> Player
    # triads_before -> int
    #
    # Fills the board with user's move.
    # Asks the user to enter 'S' or 'O'.
    # Asks the user if he/she if sure about the decision. (valid inputs: 'y', 'yes', 'no', 'n')
    # Updates the board according to user's decision.

    print(f'{P.name} your turn!')
    sure = False
    while not sure:
        P.letter = input('Please enter the letter you want to place ("S" or "O"). ')
        while P.letter.isdigit():
            clear_con()
            printBoard(b)
            P.letter = input('Please enter a letter ("S" or "O"). ')    
        
        P.letter = P.letter.upper()
        while P.letter != 'S' and P.letter != 'O':
            clear_con()
            printBoard(b)
            P.letter = input('Please enter one of the two letters ("S" or "O"). ')
            P.letter = P.letter.upper()
        u_sure = input('Are you sure? (yes or no) ')
        while u_sure.isdigit():
            clear_con()
            printBoard(b)
            u_sure = input('Are you sure?(yes or no) ')
        while u_sure.lower() != 'no' and  u_sure.lower() != 'yes' and u_sure.lower() != 'y' and u_sure.lower() != 'n':
            clear_con()
            printBoard(b)
            u_sure = input('Are you sure?(yes or no) ')
        if u_sure.lower() == 'no' or u_sure.lower() == 'n': sure = False
        else: sure = True
        
    run = True
    while run:
        coordinates = list()
        r = input('Enter the row of the square: ')
        while not r.isdigit():
            clear_con()
            printBoard(b)
            r = input('Enter the row of the square: ')
        r = int(r)
        while r < 1 or r > n:
            clear_con()
            printBoard(b)
            r = input('Enter the row of the square: ')
            while not r.isdigit():
                clear_con()
                printBoard(b)
                r = input('Enter the row of the square: ')
            r = int(r)
        c = input('Enter the column of the square: ')
        while not c.isdigit():
            clear_con()
            printBoard(b)
            c = input('Enter the column of the square: ')
        c = int(c)
        while c < 1 or c > n:
            clear_con()
            printBoard(b)
            c = input('Enter the column of the square: ')
            while not c.isdigit():
                c = input('Enter the column of the square: ')
            c = int(c)
        coordinates.extend([r,c])
        pos = position(coordinates)
        if isEmpty(b,pos):
            insertLetter(P.letter,pos)
            if newTriadExist(b,triads_before)[0]:
                P.score += newTriadExist(b,triads_before)[1]
            run = False
        else:
            run = True


def newTriadExist(b, num_of_triads_before):
    # Inputs:
    # b -> list
    # num_of_triads_before -> int
    #
    # Returns a tuple:
    # The first element is True if there is new triad (possible "SOS") it is False.
    # The second element is the number of new triads.

    num_of_triads_after = 0

    middle = [_ for _ in range(n + 2, n * (n - 1)) if _ % n != 0 and _ % n != 1]

    # For rows
    for j in range(n):
        for i in range(1, n - 1):
            if b[i + j * n] == 'S' and b[i + 1 + j * n] == 'O' and b[i + 2 + j * n] == 'S': num_of_triads_after += 1
    # For columns
    for j in range(n - 2):
        for i in range(1, n + 1):
            if b[i + j * n] == 'S' and b[i + j * n + n] == 'O' and b[
                i + j * n + 2 * n] == 'S': num_of_triads_after += 1
    # Diagonally
    for i in range(len(middle)):
        if b[middle[i]] == 'O':
            if b[middle[i] + n - 1] == 'S' and b[middle[i] - n + 1] == 'S': num_of_triads_after += 1
            if b[middle[i] + n + 1] == 'S' and b[middle[i] - n - 1] == 'S': num_of_triads_after += 1

    new_triads = num_of_triads_after - num_of_triads_before
    return num_of_triads_after > num_of_triads_before, new_triads


def moveComp(comp,b,triads_before,dif):
    # Inputs:
    # comp -> Player
    # b -> list
    # triads_before -> int
    # dif -> int
    #
    # Fills te board with the computer move and adds point(s) to the comp's score.
    # Computer move according to difficulty.
    #
    # If 'Easy', the move is random.
    #
    # If 'Medium', checks if there is a possible 'SOS' and there is, makes the appropriate move.
    # Priority:
    #  1. horizontal
    #  2. vertical
    #  3. diagonally

    print('...')
    sleep(1.5)
    possible_moves = [x for x in range(1,len(b)) if b[x] == ' ']
    index_move = randint(0,len(possible_moves) - 1)
    options = {1:'S',2:'O'}
    
    if dif.lower() == 'easy':
        s_o = options.get(randint(1,2))
        b[possible_moves[index_move]] = s_o

    elif dif.lower() == 'medium':
        move_done = False
        while not move_done:
               
            # Rows
            for j in range(n):
                for i in range(1,n-1):
                    if b[i + j*n] == 'S' and b[i + 1 + j*n] == 'O' and isEmpty(b, i + 2 + j*n):
                        b[i + 2 + j*n] = 'S'
                        move_done = True
                        break
                    if b[i + j*n + 2] == 'S' and b[i + 1 + j*n] == 'O' and isEmpty(b, i + j*n):
                        b[i + j*n] = 'S'
                        move_done = True
                        break
                    
                
                    if b[i + j*n] == 'S' and b[i + 2 + j*n] == 'S' and isEmpty(b, i + 1 + j*n):
                        b[i + 1 + j*n] = 'O'
                        move_done = True
                        break
                
                if move_done: break
            if move_done: break
            
                    
            # Columns
            for j in range(n-2):
                for i in range(1,n+1):
                    if b[i+j*n] == 'S' and b[i + j*n + n] == 'O' and isEmpty(b,i+j*n+2*n):
                        b[i + j*n + 2*n] = 'S'
                        move_done = True
                        break
                    if b[i + j*n + 2*n] == 'S' and b[i + j*n + n] == 'O' and isEmpty(b,i+j*n):
                        b[i + j*n] = 'S'
                        move_done = True
                        break
                
                
                    if b[i + j*n] == 'S' and b[i + j*n + 2*n] == 'S' and isEmpty(b,i + j*n + n):
                        b[i + j*n + n] = 'O'
                        move_done = True
                        break
                   
                if move_done: break
            if move_done: break
            
            middle = [_ for _ in range(n+2,2*n)]
            for _ in range((n-1)*(n-2)):
                middle.append(middle[-len(middle)]+n)
            
            # Diagonally        
            for i in range(len(middle)):
                
                if isEmpty(b, middle[i]):
                    if b[middle[i] - n - 1] == 'S' and b[middle[i] + n + 1] == 'S':
                        b[middle[i]] = 'O'
                        move_done = True
                        break
                    if b[middle[i] - n + 1] == 'S' and b[middle[i] + n - 1] == 'S':
                        b[middle[i]] = 'O'
                        move_done = True
                        break
                
                if b[middle[i]] == 'O':
                    if b[middle[i] + n - 1] == 'S' and b[middle[i] - n + 1] == ' ':
                        b[middle[i] - n + 1] = 'S'
                        move_done = True
                        break
                    if b[middle[i] + n - 1] == ' ' and b[middle[i] - n + 1] == 'S':
                        b[middle[i] + n - 1] = 'S'
                        move_done = True
                        break
                    if b[middle[i] + n + 1] == ' ' and b[middle[i] - n - 1] == 'S':
                        b[middle[i] + n + 1] = 'S'
                        move_done = True
                        break
                    if b[middle[i] + n + 1] == 'S' and b[middle[i] - n - 1] == ' ':
                        b[middle[i] - n - 1] = 'S'
                        move_done = True
                        break
                    
            if move_done: break
            else:
                s_o = options.get(randint(1,2))
                b[possible_moves[index_move]] = s_o
                move_done = True

    if newTriadExist(b,triads_before)[0]: comp.score += newTriadExist(b,triads_before)[1]


def isEmpty(b,pos):
    # Inputs:
    # b -> list
    # pos -> int
    #
    # Returns True if the position pos on the board is empty, else returns False
    return b[pos] == ' '


def insertLetter(lettr,pos):
    # Inputs:
    # lettr -> int
    # pos -> int
    #
    # Inserts the letter lettr onto position pos
    board[pos] = lettr


def boardIsFull(b):
    # Inputs:
    # b -> list
    return b.count(' ') == 1 # Returns True if the board is full, else returns False



def winner(P1,P2):
    # Inputs:
    # P1 -> Player
    # P2 -> Player
    #
    # Prints the name of the winner. If there is no winner, print 'Tie Game'

    if P1.score > P2.score: print(f'{P1.name} you are the winner!!!')
    elif P1.score < P2.score: print(f'{P2.name} you are the winner!!!')
    else: print('Tie Game')


def score_print(p1,p2):
    # Inputs:
    # p1 -> Player
    # p2 -> Player
    #
    # Prints the score
    print(f'-----Score-----\n{p1.name}: {p1.score}\n{p2.name}: {p2.score}\n')


def difficulty_dicision():
    # Returns 1 or 2.
    # Asks the user to enter 1 or 2 to decide the difficulty.

    while True:
        print('Choose the difficulty of the game.\n')
        dif_dicision = input('1. Easy\n2. Medium\nEnter 1 or 2.\n\n')
        if dif_dicision.isdigit():
            try:
                dif_dicision = int(dif_dicision)
                if dif_dicision < 1 or dif_dicision > 2: raise Exception
                break
            except:
                clear_con()
                continue

    return dif_dicision


n = dimension()
board = [' ' for _ in range(n ** 2 + 1)]


if __name__ == '__main__':
    # This is the main function of the program

    difficulty = {1:'Easy',2:'Medium'}
    p = Player()
    comp = Player()
    p.name = input('Player, enter your name: ')
    while p.name.isdigit():
        p.name = input('Player, enter your name: ') 
    p.name = p.name.title()
    comp.name = 'CPU'
    clear_con()
    dif = difficulty_dicision()
    clear_con()
    printBoard(board)    
    game_on = True
    triads_before = 0   
    while game_on:
        movePlayer(board,p,triads_before)
        clear_con()
        printBoard(board)
        triads_before = p.score + comp.score
        score_print(p,comp)
        if boardIsFull(board): break
        moveComp(comp,board,triads_before,difficulty.get(dif).lower())
        clear_con()
        printBoard(board)
        triads_before = p.score + comp.score
        score_print(p,comp)
        if boardIsFull(board): game_on = False
    winner(p,comp)
    sleep(3)
    

print(f'You were playing {ceil(timer() - start + 1)} seconds')
