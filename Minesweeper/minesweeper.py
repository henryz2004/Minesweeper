import random


class MineField:

    def __init__(self, size):
        """
        Initializes an empty minefield

        :param size: tuple(int, int) - defines the dimensions of the minefield in rows x cols
        """

        self.field = [[0] * size[1] for _ in range(size[0])]
        self.dim = size

    def clear(self):

        self.field = [[0] * self.dim[1] for _ in range(self.dim[0])]

    def place_mines(self, mines, restrictions=None):
        """
        Places a number of mines on the field, dictated by :param mines: and denoted by -1

        :param mines: int - number of mines to place
        :return: None
        """

        restrictions = restrictions if restrictions else []

        assert mines < self.dim[0] * self.dim[1] - len(restrictions), "Attempting to place more mines than spots available"

        # First generate a nested list of available indices where mines can be placed
        locs = [
            (r, c) for c in range(self.dim[1]) for r in range(self.dim[0]) if [r, c]  not in restrictions
        ]

        for i in range(mines):

            # Pick a loc, place a mine, delete from locs
            loc = random.choice(locs)

            self.field[loc[0]][loc[1]] = -1

            locs.remove(loc)

    def place_hints(self):
        """
        PLaces the numbers that show the number of nearby mines

        :return: None
        """

        # Pad self.field
        padded = self.field[:]
        padded.insert(0, [0]*self.dim[1])
        padded.append([0]*self.dim[1])
        padded = [[0] + r + [0] for r in padded]

        for r in range(self.dim[0]):
            for c in range(self.dim[1]):

                if padded[r+1][c+1] != -1:
                    row_sums = [row[c:c+3].count(-1) for row in padded[r:r+3]]
                    block_sum = sum(row_sums)

                    self.field[r][c] = block_sum

    def get_at_pos(self, r, c):

        return self.field[r][c]

    def get_mines(self):

        mines = []
        for r in range(self.dim[0]):
            for c in range(self.dim[1]):
                if self.get_at_pos(r, c) == -1:
                    mines.append((r, c))

        return mines

    def in_bounds(self, r, c):

        return 0 <= r < self.dim[0] and 0 <= c < self.dim[1]

    def uncover_from(self, r, c):

        visited_cells = []

        to_visit = []
        to_visit.append((r, c))

        while len(to_visit) > 0:

            current_cell = to_visit.pop()

            if 0 <= current_cell[0] < self.dim[0] \
                    and 0 <= current_cell[1] < self.dim[1] \
                    and self.get_at_pos(*current_cell) != -1 \
                    and current_cell not in visited_cells:

                visited_cells.append(current_cell)

                if self.get_at_pos(*current_cell) == 0:
                    to_visit.append((current_cell[0] - 1, current_cell[1]))
                    to_visit.append((current_cell[0] + 1, current_cell[1]))
                    to_visit.append((current_cell[0], current_cell[1] - 1))
                    to_visit.append((current_cell[0], current_cell[1] + 1))
                    to_visit.append((current_cell[0] - 1, current_cell[1] - 1))
                    to_visit.append((current_cell[0] + 1, current_cell[1] + 1))
                    to_visit.append((current_cell[0] + 1, current_cell[1] - 1))
                    to_visit.append((current_cell[0] - 1, current_cell[1] + 1))

        if len(visited_cells) == 0:
            return -1

        else:
            return visited_cells

    def __repr__(self):

        return "\n".join("\t".join(str(c) for c in r) for r in self.field)