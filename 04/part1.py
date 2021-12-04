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
                board[i].append((int(value), False))  # False as all values are not identified at the start
        boards.append(board)
    return sequence, boards


def update_board(board, value):
    for i, line in enumerate(board):
        for j, (board_value, _) in enumerate(line):
            if board_value == value:
                board[i][j] = value, True


def is_winning_board(board):
    return has_winning_horizonal(board) or has_winning_vertical(board)


def has_winning_horizonal(board):
    for line in board:
        for i, (_, marked) in enumerate(line):
            if not marked:
                break
            if i == 4:
                return True
    return False


def has_winning_vertical(board):
    for column in range(5):
        for row in range(5):
            _, marked = board[row][column]
            if not marked:
                break
            if row == 4:
                return True
    return False


def get_total_unmarked_values(board):
    unmarked_values = [value for sublist in board for value, marked in sublist if not marked]
    return sum(unmarked_values)


def main():
    sequence, boards = read_data()

    for value in sequence:
        for board in boards:
            update_board(board, value)
            if is_winning_board(board):
                unmarked_total = get_total_unmarked_values(board)
                print(f"final value: {value}, unmarked total: {unmarked_total}, product: {value * unmarked_total}")
                return


main()
