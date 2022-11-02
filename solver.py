from pathlib import Path
from os import listdir
import numpy as np
from SAT_model import SAT


def return_dict(model: SAT) -> dict:
    return {
        'SAT Clauses Number': model.sat_clauses_num,
        'Variables': [True if var == 1 else False for var in model.vars[1:]],
        'unSAT Clauses': [i+1 for i, clause in enumerate(model.sat_clauses) if not clause]
    }


def stochastic_hill_climbing(model: SAT, max_iterations=1000, verbose=False, plot=False) -> dict:
    probs = np.zeros(model.var_num+1, dtype=float)
    current_sat = model.calc_sat()
    best_so_far = return_dict(model)
    if verbose:
        log_str = ''

    for _ in range(max_iterations):
        if current_sat == model.clause_num:
            break

        neighbors = model.neighbors()[1:]

        for i, neighbor in enumerate(neighbors, 1):
            probs[i] = model.calc_sat(neighbor)

        if verbose:
            log_str += f'Neighbors: {list(map(int, probs))}, '

        probs /= np.sum(probs)
        chose_neighbor = np.random.choice(
            range(1, model.var_num+1), p=probs[1:]) - 1
        model.vars = neighbors[chose_neighbor]

        current_sat = model.calc_sat()

        if current_sat > best_so_far['SAT Clauses Number']:
            best_so_far = return_dict(model)

        if verbose:
            log_str += f'SAT: {current_sat}\n'

    if verbose:
        Path('logs').mkdir(parents=True, exist_ok=True)
        with open(Path(f'logs/log{len(listdir("logs"))}.log'), 'w') as log:
            log.write(log_str)

    if plot:
        pass

    return best_so_far