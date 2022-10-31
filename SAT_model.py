import numpy as np


class SAT:
    def __init__(self) -> None:
        self.var_num: int
        self.clause_num: int
        self.vars: np.ndarray
        self.clauses: np.ndarray
        self.clause_var_num: np.ndarray

    def initialize_model(self, input_file_name: str) -> None:
        with open(input_file_name) as fd:
            self.var_num, self.clause_num = map(
                int, fd.readline().split())

            self.clauses = np.zeros(
                (self.var_num+1, self.clause_num), dtype=int)

            self.clause_var_num = np.zeros((1, self.clause_num), dtype=int)

            for i in range(self.clause_num):
                for term in map(int, fd.readline().split()[:-1]):
                    self.clauses[abs(term), i] = term//abs(term)
                    self.clause_var_num[:, i] += 1

        self.randomize_variables()

    def randomize_variables(self) -> None:
        self.vars = np.ones((1, self.var_num+1), dtype=int)
        negs = np.random.choice(self.var_num, size=np.random.random_integers(
            self.var_num), replace=False)
        self.vars[:, negs] = -1
