import numpy as np
import numpy.typing as npt
import logging


class Board:
    def __init__(self, height: int, width: int):
        self.area = height * width
        self.table: npt.NDArray[object] = np.empty(shape=(height, width), dtype=object)
        for i in range(height):
            for j in range(width):
                self.table[i][j] = f'{i}-{j}'


class Figure:
    """
    A 2D bool array. An element of the array is True if the figure includes the cell.
    """
    def __init__(self, array: npt.NDArray[bool]):
        self.array: npt.NDArray[bool] = array
        self.area = self.array.sum()

    def possible_positions(self, board: Board) -> list[list[str]]:
        """
        Finds all possible positions for a figure to be placed on a board
        :param board:
        :return: A list of lists of cell names.
        """
        axis0_dif = board.table.shape[0] - self.array.shape[0]
        axis1_dif = board.table.shape[1] - self.array.shape[1]
        if axis0_dif < 0 or axis1_dif < 0:
            return []
        answer = []
        for i in range(axis0_dif + 1):
            for j in range(axis1_dif + 1):
                array = np.pad(self.array, ((i, axis0_dif - i), (j, axis1_dif - j)))
                answer.append(list(np.extract(condition=array, arr=board.table)))
        return answer


class Rectangle(Figure):
    def __init__(self, height, width):
        array = np.full(shape=(height, width), fill_value=True)
        super(Rectangle, self).__init__(array)

    def possible_positions(self, board: Board) -> list[list[str]]:
        answer = super(Rectangle, self).possible_positions(board)
        self.array = np.rot90(self.array)
        answer.extend(super(Rectangle, self).possible_positions(board))
        return answer


class LShaped(Figure):
    def __init__(self, left_length, down_length):
        array = np.full(shape=(left_length, down_length), fill_value=False)
        for i in range(left_length):
            array[i][0] = True
        for j in range(down_length):
            array[0][j] = True
        logging.debug(str(array))
        super(LShaped, self).__init__(array)

    def possible_positions(self, board: Board) -> list[list[str]]:
        answer = []
        for _ in range(4):
            self.array = np.rot90(self.array)
            answer.extend(super(LShaped, self).possible_positions(board))
        return answer
