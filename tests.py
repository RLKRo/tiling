import node_classes
import pytest
import table_class
import figure_classes
import main
import numpy as np
import logging


class TestNodeClasses:
    @pytest.fixture
    def prepare_nodes(self):
        node1: node_classes.Node = node_classes.Node('1')
        node2: node_classes.Node = node_classes.Node('2')
        node3: node_classes.Node = node_classes.Node('3')
        return node1, node2, node3

    def test_insert_horizontal_1(self, prepare_nodes):
        node1, node2, node3 = prepare_nodes
        node2.insert(node1, 'left', node1, 'right')
        node3.insert(node2, 'left', node1, 'right')

        assert node1.left == node3
        assert node1.right == node2
        assert node2.left == node1
        assert node2.right == node3
        assert node3.left == node2
        assert node3.right == node1

    def test_insert_horizontal_2(self, prepare_nodes):
        node1, node2, node3 = prepare_nodes
        assert node1.left == node1
        assert node2.left == node2
        assert node3.left == node3
        node2.insert(node1, 'left', node1, 'right')
        node3.insert(node2, 'right', node1, 'left')

        assert node1.left == node2
        assert node1.right == node3
        assert node2.left == node3
        assert node2.right == node1
        assert node3.left == node1
        assert node3.right == node2
        node3.cover_horizontal()
        assert node1.right == node2

    def test_columns_1(self, prepare_nodes):
        node1, node2, node3 = prepare_nodes
        column = node_classes.Column()
        node1.insert(column, 'up', column, 'down')
        assert column.size == 1
        assert column.down == node1
        node2.insert(column, 'up', node1, 'down')
        assert column.size == 2
        assert column.down == node2
        assert column.up == node1
        node3.insert(node2, 'up', node1, 'down')
        assert column.size == 3
        assert node2.down == node3
        node1.cover_vertical()
        assert column.size == 2
        assert column.up == node3
        node1.insert(node3, 'up', column, 'down')
        assert column.size == 3
        assert column.up == node1

    def test_columns_2(self, prepare_nodes):
        node1, node2, node3 = prepare_nodes
        column1 = node_classes.Column('C1')
        column2 = node_classes.Column('C2')
        column2.insert_after(column1)
        assert column2.left == column1
        assert column1.size == column2.size == 0
        node1.insert_above(column1)
        node2.insert_above(column1)
        node3.insert_above(column2)
        node3.insert_after(node1)
        assert column1.down.right.left.right.up == column2
        assert column1.size == 2
        assert column2.size == 1
        column1.cover()
        assert column2.size == 0
        assert column1.size == 2
        assert column2.up == column2
        column1.uncover()
        assert column2.size == 1
        column2.cover()
        assert column1.size == 1
        assert column1.up == column1.down == node2


class TestTable:
    def test_main(self):
        table = table_class.Table(
            ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            [
                ['C', 'E', 'F'],
                ['A', 'D', 'G'],
                ['B', 'C', 'F'],
                ['A', 'D'],
                ['B', 'G'],
                ['D', 'E', 'G']
            ]
        )
        # table.print_table()
        assert table.header.right.down.left.column.name == 'G'
        assert table.header.right.up.right.column.name == 'D'
        result = table.solve()
        assert result

    def test_1(self):
        table = table_class.Table(
            ['A', 'B', 'C'],
            [
                ['A', 'B'],
                ['B', 'C']
            ]
        )
        assert not table.solve()

    def test_2(self):
        table = table_class.Table(
            ['A'],
            []
        )
        assert not table.solve()


class TestFigures:
    def test_figure(self):
        figure = figure_classes.Figure(np.array([[True, True], [True, False]]))
        assert figure.area == 3
        board = figure_classes.Board(3, 3)
        logging.debug(str(board.table))
        assert board.table[0][0] == '0-0'
        positions = figure.possible_positions(board)
        assert len(positions) == 4
        assert positions[0] == ['0-0', '0-1', '1-0']
        logging.debug(str(positions))

    def test_rectangle(self):
        rectangle = figure_classes.Rectangle(2, 3)
        assert rectangle.area == 6
        board = figure_classes.Board(3, 3)
        positions = rectangle.possible_positions(board)
        assert len(positions) == 4
        logging.debug(str(positions))

    def test_l_shaped(self):
        l_shaped = figure_classes.LShaped(2, 3)
        assert l_shaped.area == 4
        board = figure_classes.Board(3, 3)
        positions = l_shaped.possible_positions(board)
        assert len(positions) == 8
        logging.debug(str(positions))

        l_shaped = figure_classes.LShaped(1, 4)
        with pytest.raises(AssertionError):
            positions = l_shaped.possible_positions(board)


class TestMain:
    def test_main(self):
        assert main.main(
            board_params=(3, 5),
            rectangle_params=[((2, 2), 1)],
            l_shaped_params=[((3, 2), 1), ((2, 2), 2)]
        )

    def test_set_1(self):
        assert main.main((3, 3), [], [])
        assert not main.main((3, 3), [((4, 4), 1)], [])
        assert not main.main((3, 3), [], [((1, 4), 1)])
        assert main.main((4, 4,), [((2, 2), 4)], [])
        assert not main.main((4, 4), [((2, 2), 5)], [])

    def test_set_2(self):
        assert not main.main((3, 3), [((2, 3), 1)], [((2, 2), 1)])
        assert not main.main((3, 4), [((2, 2), 2)], [((2, 2), 1)])
        assert not main.main((3, 4), [((2, 2), 2)], [((2, 3), 1)])
        assert main.main((5, 4), [((3, 3), 1), ((2, 2), 1)], [((2, 4), 1)])
        assert main.main((5, 4), [((3, 3), 1), ((2, 2), 1)], [((4, 2), 1)])
