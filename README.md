## CSP Solver

These `python` modules use generalized arc-consistency to create an all-purpose constraint satisfaction problem solver. This repository also include some sample use-cases of the solver[^1].

---

### N-Queens Solver

This `python` script uses the `CSP` module to solve the generalization of the classic [8 Queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle), and can be invoked using the following command.

```
python3 nqueens.py <input_file>
```

#### Input Format

`<input_file>` is a plaint text file. The first line contains a number that indicates the value of `n`, the dimension of the problem. For the classic 8 Queens puzzle, this would be `8`. The following `n` lines contain exactly one character each, which must have one of the following values:

1. An integer representing the **0-indexed** position of any queens present in the initial configuration of the chess board
2. `-` to indicate that there are no queens in corresponding row

To solve a 4 Queens variation of this puzzle, where the initial configuration has a queen in the first column of the third row, you would create the following input file:

```
4
-
-
0
-
```

[^1]: For now its only the N Queens example; a battleship solitaire solver will be added soon.