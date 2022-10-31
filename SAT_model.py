import numpy as np


class SAT:
    def __init__(self) -> None:
        self.var_num: int
        self.vars: np.ndarray
        self.clause_num: int
        self.clauses: np.ndarray
        self.clause_var_num: np.ndarray
        self.sat_clauses_num: int
        self.sat_clauses: list

    def initialize_model(self, input_file_name: str) -> None:
        with open(input_file_name) as fd:
            self.var_num, self.clause_num = map(
                int, fd.readline().split())

            self.clauses = np.zeros(
                (self.var_num+1, self.clause_num), dtype=int)

            self.clause_var_num = np.zeros(self.clause_num, dtype=int)

            for i in range(self.clause_num):
                for term in map(int, fd.readline().split()[:-1]):
                    self.clauses[abs(term), i] = term//abs(term)
                    self.clause_var_num[i] += 1

        self.sat_clauses = self.clause_num * [False]
        self.randomize_variables()

    def randomize_variables(self) -> None:
        self.vars = np.ones(self.var_num+1, dtype=int)
        negs = np.random.choice(self.var_num, size=np.random.random_integers(
            self.var_num), replace=False)
        self.vars[negs+1] = -1

    def calc_sat(self, variables: np.ndarray = None) -> int:
        if not variables:
            variables = self.vars
        tmp = np.dot(variables.reshape(1, -1), self.clauses)
        tmp += self.clause_var_num.reshape(1, -1)

        self.sat_clauses_num = 0
        for i, element in enumerate(tmp.reshape(-1)):
            self.sat_clauses[i] = (element != 0)
            self.sat_clauses_num += (element != 0)

        return self.sat_clauses_num

    def neighbors(self) -> np.ndarray:
        ngb = np.ndarray((self.var_num+1, self.var_num+1), dtype=int)
        ngb[0] = self.vars
        for i in range(1, self.var_num+1):
            ngb[i] = self.vars
            ngb[i][i] *= -1
        return ngb
