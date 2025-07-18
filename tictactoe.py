"""
Tic Tac Toe Player
"""

import math

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action: cell already taken")

    from copy import deepcopy
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []

    # Rows and columns
    for i in range(3):
        lines.append(board[i])  # row
        lines.append([board[0][i], board[1][i], board[2][i]])  # column

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line.count(X) == 3:
            return X
        if line.count(O) == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(state):
        if terminal(state):
            return utility(state), None
        v = -math.inf
        best_action = None
        for action in actions(state):
            min_v, _ = min_value(result(state, action))
            if min_v > v:
                v = min_v
                best_action = action
                if v == 1:
                    break  # pruning opportunity
        return v, best_action

    def min_value(state):
        if terminal(state):
            return utility(state), None
        v = math.inf
        best_action = None
        for action in actions(state):
            max_v, _ = max_value(result(state, action))
            if max_v < v:
                v = max_v
                best_action = action
                if v == -1:
                    break  # pruning opportunity
        return v, best_action

    current_player = player(board)
    if terminal(board):
        return None

    if current_player == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)

    return action
