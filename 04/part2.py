# Reads the source file
#  - first line is read as a list of integers, this is the sequence of numbers calls
#  - subsequent lines are chunked into groups of 5 for the bingo boards
#    They are parsed as integer values, paired with a boolean (this will indicate if they are marked or not during
#    the game.
def read_data():
    lines = [line.strip() for line in open('input.txt', 'r').readlines()]

    sequence = [int(value) for value in lines[0].split(",")]
    boards = []

    chunks = [lines[i:i + 5] for i in range(2, len(lines), 6)]
    for chunk in chunks:
        board = []
        for i, line in enumerate(chunk):
            board.append([])
            for j, value in enumerate([value for value in line.strip().split(" ") if not value == '']):
                board[i].append((int(value), False))  # False as all values are not marked at the start
        boards.append(board)
    return sequence, boards


# Looks at all values on a board, if the specified value is found then it is marked as True
def update_board(board, value):
    for i, line in enumerate(board):
        for j, (board_value, _) in enumerate(line):
            if board_value == value:
                board[i][j] = value, True


# Checks for horizontal or vertical winning lines, return True if any are found
def is_winning_board(board):
    return has_winning_horizontal(board) or has_winning_vertical(board)


# Checks for any horizontal line where all the values are marked as True
def has_winning_horizontal(board):
    for line in board:
        for i, (_, marked) in enumerate(line):
            if not marked:
                break
            if i == 4:
                print_board_status(f"Horizontal row", board)
                return True
    return False


# Checks for any vertical line where all the values are marked as True
def has_winning_vertical(board):
    for column in range(5):
        for row in range(5):
            _, marked = board[row][column]
            if not marked:
                break
            if row == 4:
                print()
                print_board_status(f"Vertical column {column}", board)
                return True
    return False


# Flattens the liosts and filters marked values, then sums all the values
def get_total_unmarked_values(board):
    unmarked_values = [value for sublist in board for value, marked in sublist if not marked]
    return sum(unmarked_values)


# Pretty prints the current state of the board
def print_board_status(comment, board):
    print(comment)
    [print(f'{["X" if marked else "O" for _, marked in line]} -- {line}') for line in board]
    print()


def main():
    sequence, boards = read_data()

    for value in sequence:
        remaining_boards = []
        for board in boards:
            update_board(board, value)
            if not is_winning_board(board):
                remaining_boards.append(board)

        # If after playing all boards we have none left we know the last board of the list was the last to win.
        if len(remaining_boards) == 0:
            final_board = boards[len(boards) - 1]
            unmarked_total = get_total_unmarked_values(final_board)
            print_board_status("Final solved board", final_board)
            print(f"final value: {value}, unmarked total: {unmarked_total}, product: {value * unmarked_total}")
            return
        boards = remaining_boards


main()
