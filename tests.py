import node_classes
import pytest
import table_class


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
