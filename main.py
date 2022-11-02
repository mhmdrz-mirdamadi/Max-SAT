from SAT_model import SAT
from stochastic_hill_climbing import stochastic_hill_climbing


if __name__ == '__main__':
    mySat = SAT()
    mySat.initialize_model('Max-Sat_20_80.txt')
    print(stochastic_hill_climbing(mySat))
