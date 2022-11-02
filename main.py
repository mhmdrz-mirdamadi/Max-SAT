from SAT_model import SAT
from solver import stochastic_hill_climbing


if __name__ == '__main__':
    mySat = SAT()
    mySat.initialize_model('tests/Max-Sat_20_80.txt')
    res = stochastic_hill_climbing(mySat, verbose=True)
    [print(f'{key}: {value}') for key, value in res.items()]
