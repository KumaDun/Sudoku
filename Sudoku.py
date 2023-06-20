import copy

def sudoku_cells():
    cells = []
    for i in range(9):
        for j in range(9):
            cells.append((i, j))
    return cells


def sudoku_arcs():
    arcs = set()
    # Add arcs for each row
    for row in range(9):
        for col in range(9):
            for col_ in range(col + 1, 9):
                arcs.add(((row, col), (row, col_)))
                arcs.add(((row, col_), (row, col)))

    # Add arcs for each column
    for col in range(9):
        for row in range(9):
            for row_ in range(row + 1, 9):
                arcs.add(((row, col), (row_, col)))
                arcs.add(((row_, col), (row, col)))

    # Add arcs for 3x3 block
    same_block = set()
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            for i in range(row, row + 3):
                for j in range(col, col + 3):
                    same_block.add((i, j))
                    for elem1 in same_block:
                        for elem2 in same_block:
                            if elem1 != elem2:
                                arcs.add((elem1, elem2))
                                arcs.add((elem2, elem1))
            same_block = set()

    return arcs


def read_board(path):
    board = dict()
    f = open(path, "r")
    myList = f.readlines()
    for i in range(len(myList)):
        for j in range(len(myList[i])):
            if myList[i][j] == '*':
                board[(i, j)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            elif myList[i][j] != '\n':
                board[(i, j)] = {int(myList[i][j]), }
            else:
                continue
    return board


class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    # VISITED_ARCS = set()

    def __init__(self, board):
        self.board = board
        self.ARCS = Sudoku.ARCS.copy()
        self.visited_arcs = set()

    def get_values(self, cell):
        return self.board[cell]

    def copy(self):
        board_copied = copy.deepcopy(self.board)
        visited_arcs_copied = self.visited_arcs.copy()
        sudoku_copied = Sudoku(board_copied)
        sudoku_copied.infer_ac3()
        return sudoku_copied

    def move(self, cell, val):
        self.board[cell] = {val, }
        self.add_back_arc(cell)

    def successors(self):
        unsolved_cells = sorted(self.unsolved_cells(),
                                key=lambda elem: len(self.board[elem]))
        most_constrained_cell = unsolved_cells[0]
        for val in self.board[most_constrained_cell]:
            new_sudoku = self.copy()
            new_sudoku.move(most_constrained_cell, val)
            yield most_constrained_cell, val, new_sudoku

    def remove_inconsistent_values(self, cell1, cell2):
        self.visited_arcs.add((cell1, cell2))
        if len(self.board[cell2]) == 1:
            for elem in self.board[cell1]:
                if elem in self.board[cell2]:
                    self.board[cell1].remove(elem)
                    return True
        return False

    def infer_ac3(self):
        while len(self.ARCS) != 0:
            curr = self.ARCS.pop()
            # print("Curr ", curr)
            isRemoved = self.remove_inconsistent_values(curr[0], curr[1])
            if isRemoved:
                if len(self.board[curr[0]]) > 0:
                    self.add_back_arc(curr[0])
                else:
                    # print("wrong path")
                    # print(curr[0], self.board[curr[0]])
                    return False
        return True

    def infer_improved(self):
        bloc_heads = [(0, 0), (0, 3), (0, 6), (3, 0),
                      (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        row_heads = [(i, 0) for i in range(9)]
        col_heads = [(0, i) for i in range(9)]

        while True:
            before = self.unsolved_num()

            if not self.infer_ac3():
                return -1

            for bloc_head in bloc_heads:
                bloc = [bloc_head] + self.neighbors(bloc_head, "bloc")
                for val in range(9):
                    only_cell_block = self.unique_val_cell(bloc, val)
                    if only_cell_block is not None:
                        self.move(only_cell_block, val)
            for row_head in row_heads:
                row = [row_head] + self.neighbors(row_head, "row")
                for val in range(9):
                    only_cell_row = self.unique_val_cell(row, val)
                    if only_cell_row is not None:
                        self.move(only_cell_row, val)
            for col_head in col_heads:
                col = [col_head] + self.neighbors(col_head, "col")
                for val in range(9):
                    only_cell_col = self.unique_val_cell(col, val)
                    if only_cell_col is not None:
                        self.move(only_cell_col, val)

            after = self.unsolved_num()
            if after == 0:
                return 1
            if before <= after:
                return 0

    def unique_val_cell(self, cells, val):
        last_found = None
        count = 0
        for cell in cells:
            if val in self.board[cell]:
                count += 1
                last_found = cell
        if count == 1:
            return last_found

    def add_back_arc(self, modified_cell):
        added_back = []
        for arc in self.visited_arcs:
            if arc[1] == modified_cell:
                self.ARCS.add((arc[0], arc[1]))
                added_back.append((arc[0], arc[1]))
        for arc in added_back:
            self.visited_arcs.remove(arc)
        return added_back

    @staticmethod
    def neighbors(cell, method):
        neighbor_block = []
        neighbor_row = []
        neighbor_col = []
        if method == "bloc":
            for i in range(cell[0], cell[0] + 3):
                for j in range(cell[1], cell[1] + 3):
                    if (i, j) != cell:
                        neighbor_block.append((i, j))
            return neighbor_block
        if method == "row":
            for i in range(9):
                if i != cell[1]:
                    neighbor_row.append((cell[0], i))
            return neighbor_row
        if method == "col":
            for i in range(9):
                if i != cell[0]:
                    neighbor_col.append((i, cell[1]))
            return neighbor_col

    def unsolved_num(self):
        count = 0
        for cell in Sudoku.CELLS:
            if len(self.board[cell]) > 1:
                count += 1
        return count

    def infer_with_guessing(self):
        is_solved = self.infer_improved()
        if is_solved == 1:
            return
        elif is_solved == -1:
            return
        else:
            solved_board = next(self.dfs())
        self.board = solved_board

    def dfs(self):
        for cell, val, new_sudoku in self.successors():
            is_valid = new_sudoku.infer_improved()
            if is_valid == 1:
                yield new_sudoku.board
            elif is_valid == -1:
                continue
            else:
                for solved_board in new_sudoku.dfs():
                    yield solved_board

    def unsolved_cells(self):
        unsolved_cells = []
        for cell in Sudoku.CELLS:
            if len(self.board[cell]) != 1:
                unsolved_cells.append(cell)
        return unsolved_cells

    def is_solved(self):
        for cell in Sudoku.CELLS:
            if len(self.board[cell]) != 1:
                return False
        return True

    def __str__(self):
        for cell in Sudoku.CELLS:
            print(cell, ": ", self.board[cell])
        return " "
