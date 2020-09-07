import random 
import pprint


board = []


def make_lists(bo):

    for _ in range (0, 9):
        numbers  = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        bo.append(numbers)
    return bo


def solve(bo):

    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    numbers = list(range(1, 10))
    shuffledNumbers =[]
    random.shuffle(numbers)
    draw = numbers[:9]
    shuffledNumbers.append(draw)
    for i in shuffledNumbers[0]:
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def print_board(bo):

    for i in range(len(bo)):
        if i % 3 == 0 and i != 0 :
            print("- - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")  


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) # row, column

    return None


make_lists(board)
print("")
solve(board)
print("")
print_board(board)
print("")


# function to create random sudoku board - can determine how hard can it be to solve by changing range area
def make_holes_in_sudoku(bo):

    for _ in range(81):
        bo[random.randint(0, 8)][random.randint(0, 8)] = 0


make_holes_in_sudoku(board)

print_board(board)
