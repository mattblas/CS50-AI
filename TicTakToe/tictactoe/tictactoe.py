"""
Tic Tac Toe Player
"""

import copy, random, math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


board = initial_state()


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = []
    y_count = []
    for i in board:
        x_count.append(i.count('X'))
        y_count.append(i.count('O'))
    if sum(x_count) + sum(y_count) >= 9:
        return ('the game is already over')
    elif sum(x_count) > sum(y_count):
        return (O)
    elif sum(x_count) <= sum(y_count):
        return (X)
    else:
        raise Exception('Something wrong with def player')


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                actions.add((row, cell))
    if len(actions) == 0:
        return ('the game is already over')
    elif len(actions) > 0:
        return (actions)
    else:
        raise Exception('Something wrong with def actrions')


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        print(action)
        raise Exception('Not a valid move')

    new_board_state = copy.deepcopy(board)
    new_board_state[action[0]][action[1]] = player(board)
    return new_board_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for combination in winning_combinations:
        if all(board[x][y] == X for x, y in combination):
            return X
        elif all(board[x][y] == O for x, y in combination):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    x_count = []
    y_count = []
    for i in board:
        x_count.append(i.count('X'))
        y_count.append(i.count('O'))
    if winner(board) == 'X' or winner(board) == 'O' or sum(x_count) + sum(y_count) >= 9:
        return True
    elif winner(board) == None or sum(x_count) + sum(y_count) < 9:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if len(actions(board)) == 9:
        return(random.randint(0,2), random.randint(0,2))

    if player(board) == X:                              
        v = float('-inf')
        for action in actions(board):                   # check the highest value  
            if min_value(result(board, action)) > v:    # among all actions of the
                v = min_value(result(board, action))    # opposing player
                max_action = action
    elif player(board) == O:
        v = float('inf')
        for action in actions(board):
            if max_value(result(board, action)) < v:
                v = max_value(result(board, action))
                max_action = action
    
    return max_action


def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
