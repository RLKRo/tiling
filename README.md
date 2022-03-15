# Intro

This repo contains a Python implementation of the [Dancing Links X algorithm](https://arxiv.org/abs/cs/0011047) and its application to the following problem:

Given a set of polyominoes described in the last two parameters decide whether it is possible to fit them on a board
described in the first parameter.

The first parameter is a tuple `(H, W)`. H is the height of the board,
W is the width of the board.

The second parameter describes rectangle figures. Each list object
is a tuple `((H, W), N)`. The pair describes the height and the width of
a single rectangle. The third element `N` is the number of figures of that type.

The third parameter describes L-shaped figures. Both arms of such figures are 1 cell wide. Each list object
is a tuple `((L, D), N)`. The pair describes the shape of
a single figure in a following way. Parameter `L` is the horizontal length of the figure.
Parameter `D` is the vertical length of the figure. The third element `N` is the number of figures of that type.

# Algorithm complexity

Let `M` be the area of the board, `N` be the number of figures and `L` be the characteristic area of those figures. 

Assuming each node requires `O(1)` memory the algorithm requires `O(N * M * L)` memory:
there are `N` figures, each has `O(M)` possible positions on the board, each position is described by `O(L)` nodes.

Time complexity is trickier. I am probably wrong but

The table has `NM` rows and `N+M` columns. Each row has `L` nodes. Therefore, each column has `LNM/(M+N)` nodes.
At each step we choose one of them and do `O(L)` operations. As each step covers `L` columns and there are `N+M` columns the algorithm takes 
`(M+N)/L` steps. Thus, the time complexity is `O((L^2 * MN/(M+N))^((M+N)/L))`.


# Usage

`$ python main.py "(3, 5)" "[((2, 2), 1)]" "[((3, 2), 1), ((2, 2), 2)]"`

`True`
