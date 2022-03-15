import node_classes
from typing import Optional
import logging


class Table:
    """
    A class representing a boolean table in a form of a double-linked four-way list.
    The table is used in the Algorithm X.
    """
    def __init__(self, column_names: list[str], rows: list[list[str]]):
        """
        Creates a table with columns specified in column_names and rows.
        :param column_names: A list of column names to be inserted in a table
        :param rows: A list of lists of column names. Each object represents a list of columns which the row crosses.
        """
        self.header: node_classes.Node = node_classes.Node('header')
        self.column_map: dict[str, node_classes.Node] = {}
        column_names.sort()
        for name in column_names:
            column = node_classes.Column(name)
            column.insert_after(self.header.left)
            self.column_map[name] = column
        for row in rows:
            row.sort()
            last_inserted = None
            for column_name in row:
                node = node_classes.Node()
                node.insert_above(self.column_map[column_name])
                if last_inserted is not None:
                    node.insert_after(last_inserted)
                last_inserted = node

    def next_column(self) -> node_classes.Column:
        """
        Selects the next column to cover as a column with the minimal size.
        :return: The selected column.
        """
        size = None
        min_column = None
        for column in node_classes.NodeIterator(self.header, 'right'):
            if size is None or size > column.size:
                size = column.size
                min_column = column
        return min_column

    def solve(self, level: int = 0) -> bool:
        """
        Finds a subset of rows that is an exact cover of the columns using the DLX algorithm.
        :return: True if such subset was found
        """
        logging.debug(level * '    ' + f'In a solver at level {level}.')
        if self.header.right == self.header:
            logging.info(level * '    ' + f'All columns covered. Returning from level {level}.')
            return True
        column = self.next_column()
        logging.debug(level * '    ' + f'Next column is {column.name}')
        if column.size == 0:
            logging.debug(level * '    ' + f'Column cannot be covered. Returning from level {level}.')
            return False
        column.cover()
        logging.debug(level * '    ' + f'Column covered. Size {column.size}')
        for row in node_classes.NodeIterator(column, 'down'):
            logging.debug(level * '    ' + 'The chosen row also covers:')
            for row_element in node_classes.NodeIterator(row, 'right'):
                row_element.column.cover()
                logging.debug(level * '    ' + row_element.column.name)
            logging.debug(level * '    ' + 'End of list')
            result = self.solve(level + 1)
            for row_element in node_classes.NodeIterator(row, 'left'):
                row_element.column.uncover()
            if result:
                logging.info(level * '    ' + f'Solution found. Returning from level {level}.')
                column.uncover()
                return True
        column.uncover()
        logging.debug(level * '    ' + f'Solution not found. Returning from level {level}.')
        return False
