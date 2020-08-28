import sys
import numpy as np
sys.setrecursionlimit(10**6)
import matplotlib.pyplot as plt


def in_board(pos_x, pos_y, size):
    truth_y = 0<= pos_x < size
    truth_x = 0<= pos_y < size
    return truth_x and truth_y

def queen_placer(pos, board):
    board[pos] = -1
    size = board.shape[0]
    pos_y, pos_x = pos
    diagonals = [(pos_y+i, pos_x+i) for i in range(-1*size, size+1) if in_board(pos_y + i, pos_x+i, size)] + [(pos_y-i, pos_x+i) for i in range(-1*size, size+1) if in_board(pos_y - i, pos_x+i, size)]
    for i in diagonals:
        board[i] = 1
    board[pos_y,:] = 1
    board[:,pos_x] =1
    board[pos] = -1
    return board


board = np.zeros((4,4))
queen_placer((1,1), board)


def solver_function(size, q_coordinates = [], blacklist = {}):
    if size == len(q_coordinates):
        return q_coordinates
    if blacklist == {}:
        blacklist = {row:[] for row in range(0, size)}
    board = np.zeros((size,size))
    for pos in q_coordinates:
        board = queen_placer(pos , board)
    row = len(q_coordinates)
    for index, element in enumerate(board[row,:]):
        if element == 0. and not index in blacklist[row]:
            col = index
            blacklist[row].append(index)
            break
    try:
        q_coordinates.append((row, col))
    except:
        if len(q_coordinates) > 0:
            q_coordinates.pop(-1)
        if len(q_coordinates) > 0:
            q_coordinates.pop(-1)
        blacklist[row] = []
        q_coordinates = solver_function(size, q_coordinates,  blacklist)
    if size == len(q_coordinates):
        return q_coordinates
    elif 0. in board[row+1,:]:
        q_coordinates = solver_function(size, q_coordinates,  blacklist)
        return q_coordinates
    else:
        if len(q_coordinates) > 0:
            q_coordinates.pop(-1)
        if len(q_coordinates) > 0:
            q_coordinates.pop(-1)
        blacklist[row] = []
        q_coordinates = solver_function(size, q_coordinates,  blacklist)
        return q_coordinates


for size in range(4,21):
    q_coordinates = solver_function(size, q_coordinates = [], blacklist = {})
    print(f'For board size = {size}x{size}. The solution is {str(q_coordinates)}')


import timeit, functools
times = []
for i in range(4, 21):
    t = timeit.Timer(functools.partial(solver_function, i))
    elapsed_time = t.timeit(10)/10
    times.append(elapsed_time)


x = list(range(4,21))
print('The running time for each n value in seconds:\n')
times_formated_list = []
for size, time in zip(range(4,21), times):
    time = "{:.2e}".format(time) + ' s'
    times_formated_list.append(time)
    print(f'For {size}x{size}, Time taken = {time}')
fig, ax = plt.subplots(figsize=(25,10))
plt.plot(x,times, label="Running Time")
for a, b, c in zip(x, times, times_formated_list): 
    plt.text(a, b, c)
plt.xlabel('Board Length')
plt.ylabel('Time in s') 
plt.title('Order of growth')
plt.legend(loc="upper left")


class ChessBoard:
    def __init__(self, size):
        board = np.zeros((size,size))
        board[1::2,0::2] = 1
        board[0::2,1::2] = 1
        self.board = board
        self.size = size

    def make_board(self):
        fig, ax = plt.subplots(figsize=(10,10))
        ax.imshow(self.board, cmap='binary')
        ticks = [i for i in range(0, self.size)]
        ax.set(xticks = ticks, yticks = ticks)
        self.ax = ax

    def display(self, q_coordinates):
        fontsize = 100 - self.size*4 if 100 - self.size*4 > 10 else 15
        self.make_board()
        ax = self.ax
        for i in q_coordinates:
            ax.text(i[1], i[0],'♕', fontsize=fontsize, ha='center', va='center', color='black' if (i[0] - i[1]) % 2 == 0 else 'white')
        return ax


for size in range(4,21):
    q_coordinates = solver_function(size, q_coordinates = [], blacklist = {})
    chessBoard = ChessBoard(size)
    ax = chessBoard.display(q_coordinates)
    print('\n', f'Solution to {size}x{size}', '\n')
    plt.show(ax)
    print('\n', ''.join(['-' for i in range(11)]), '\n')
   
