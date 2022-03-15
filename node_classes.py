from typing import TypeVar

Self = TypeVar("Self", bound="Node")


class Node:
    """
    A class representing the nodes of a double-linked four-way circular list.
    """
    def __init__(self, name: str = ''):
        self.left: Self = self
        self.right: Self = self
        self.up: Self = self
        self.down: Self = self
        self.column: Column = None
        self.name: str = name

    @staticmethod
    def _opposite_direction(direction: str) -> str:
        if direction == 'up':
            return 'down'
        if direction == 'down':
            return 'up'
        if direction == 'left':
            return 'right'
        if direction == 'right':
            return 'left'

    def insert(self, node1: Self, direction1: str, node2: Self, direction2: str):
        """
        Inserts a node between the two. As a result uncovers the node if covered.
        :param node1:
        :param direction1: The direction of the first node relative to self
        :param node2:
        :param direction2: The direction of the second node relative to self
        :return: None
        """
        assert Node._opposite_direction(direction1) == direction2
        assert node1.__getattribute__(direction2) == node2
        assert node2.__getattribute__(direction1) == node1

        self.__setattr__(direction1, node1)
        self.__setattr__(direction2, node2)
        node1.__setattr__(direction2, self)
        node2.__setattr__(direction1, self)

        if direction1 == 'up' or direction2 == 'up':
            assert node1.column == node2.column
            self.column = node1.column
            self.column.size += 1

    def insert_after(self, other: Self):
        """
        Inserts the current node after another node.
        :param other: A node to be inserted after
        :return: None
        """
        self.insert(other, 'left', other.right, 'right')

    def insert_above(self, other: Self):
        """
        Inserts the current node above another node.
        :param other: A node to be inserted above
        :return: None
        """
        self.insert(other, 'down', other.up, 'up')

    def cover_horizontal(self):
        """
        Removes the node from its row.
        :return: None
        """
        self.right.left = self.left
        self.left.right = self.right

    def cover_vertical(self):
        """
        Removes the mode from its column.
        :return: None
        """
        self.up.down = self.down
        self.down.up = self.up
        self.column.size -= 1


class Column(Node):
    """
    A class representing the columns of a table.
    """
    def __init__(self, name: str = ''):
        Node.__init__(self, name)
        self.column = self
        self.size: int = 0

    def cover(self):
        """
        Removes the column from the header list.
        For every row of the column removes an element of that row from every other column.
        :return: None
        """
        self.cover_horizontal()
        for node in NodeIterator(self, 'down'):
            for row_element in NodeIterator(node, 'right'):
                row_element.cover_vertical()

    def uncover(self):
        """
        Reverts the effects of column_class.Column.cover.
        :return: None
        """
        for node in NodeIterator(self, 'up'):
            for row_element in NodeIterator(node, 'left'):
                row_element.insert(row_element.up, 'up', row_element.down, 'down')
        self.insert(self.left, 'left', self.right, 'right')


class NodeIterator:
    """
    An iterator over the nodes. Excludes the start node by default.
    """
    def __init__(self, start_node: Node, direction: str, including: bool = False):
        self.start_node = start_node
        self.current_node = start_node
        self.direction = direction
        self.including = including

    def __iter__(self):
        return self

    def __next__(self) -> Node:
        if self.including:
            self.including = False
            return self.current_node
        self.current_node = self.current_node.__getattribute__(self.direction)
        if self.current_node == self.start_node:
            raise StopIteration
        else:
            return self.current_node
