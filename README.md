# Max-SAT Solver

This is a Max-SAT Solver based on numpy to use the vectorization for efficiency.

## Algorithms

- Stochastic Hill Climbing
- Simulated Annealing
- Tabu Search

For set more options (logggin, plotting): `python3 main.py -h`

## Input Format

The first line contains two space-separated integers $n$, $m$ - number of variables and number of clauses.  
Next $m$ lines each contains space-separated integers ended with 0 representing clause $c_i$.  
Example:
`2 -4 5 6 -7 0` $\implies A_2 \land \neg A_4 \land A_5 \land A_6 \land \neg A_7$
