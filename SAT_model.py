import numpy as np


class SAT:
    def __init__(self) -> None:
        self.variable_number: int
        self.clause_number: int
        self.variables: np.ndarray
        self.clauses: np.ndarray

    def initialize_model(self, input_file_name: str) -> None:
        with open(input_file_name) as fd:
            self.variable_number, self.clause_number = map(
                int, fd.readline().split())

            self.clauses = np.zeros(
                (self.variable_number+1, self.clause_number), dtype=int)

            for i in range(self.clause_number):
                for term in map(int, fd.readline().split()[:-1]):
                    self.clauses[abs(term), i] = term//abs(term)
