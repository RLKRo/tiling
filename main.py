import table_class
import figure_classes
from ast import literal_eval
import sys


def add(
        params: list[tuple[tuple[int, int], int]],
        rows: list[list[str]],
        board: figure_classes.Board,
        info: str,
        cls
) -> int:
    """
    Adds all the possible position on a board for a figure of a class cls instantiated with parameters params to rows.
    A unique token for each figure is created using params, info and figure counter.
    :param params: Figure parameters
    :param rows: Rows of position names and figure names
    :param board:
    :param info: Figure identifier
    :param cls: Figure class
    :return: Total area of all the figures added
    """
    total_area = 0
    for shape in params:
        figure: figure_classes.Figure = cls(shape[0][0], shape[0][1])
        total_area += figure.area * shape[1]
        positions = figure.possible_positions(board)
        for number in range(shape[1]):
            for position in positions:
                position.append(f'{info}-{shape[0][0]}-{shape[0][1]}-{number}')
                rows.append(position)
                position.pop()
    return total_area


def main(
        board_params: tuple[int, int],
        rectangle_params: list[tuple[tuple[int, int], int]],
        l_shaped_params: list[tuple[tuple[int, int], int]]
) -> bool:
    """
    Solves the following problem: given a board and lists of rectangle and L-shaped figures decide whether it is
    possible to fit all the figures on the board.
    :param board_params: height and width of the board
    :param rectangle_params: a list of heights, widths of rectangles and a number of each
    :param l_shaped_params: a list of lengths of left-facing and down-facing arms of the L-shaped figure
     and a number of each
    :return: True if all the figures fit on the board.
    """
    board = figure_classes.Board(board_params[0], board_params[1])
    rows: list[list[str]] = []
    total_area: int = 0
    try:
        total_area +=\
            add(rectangle_params, rows, board, 'rectangle', figure_classes.Rectangle) + \
            add(l_shaped_params, rows, board, 'l_shaped', figure_classes.LShaped)
    except AssertionError as e:
        return False

    if total_area > board.area:
        return False

    assert board.area - total_area == add(          # Add 1x1 squares to get an exact cover problem
        params=[((1, 1), board.area - total_area)],
        rows=rows,
        board=board,
        info='additional_squares',
        cls=figure_classes.Rectangle
    )

    table = table_class.Table(board.table.flatten(), rows)

    return table.solve()


if __name__ == '__main__':
    print(main(literal_eval(sys.argv[1]), literal_eval(sys.argv[2]), literal_eval(sys.argv[3])))
