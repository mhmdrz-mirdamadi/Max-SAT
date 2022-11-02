import numpy as np
from SAT_model import SAT


def stochastic_hill_climbing(model: SAT) -> dict:
    probs = np.zeros(model.var_num+1, dtype=float)

    while True:
        current_sat = model.calc_sat()
        if current_sat == model.clause_num:
            break
        no_better_neighbor = True
        neighbors = model.neighbors()[1:]
        for i, neighbor in enumerate(neighbors, 1):
            probs[i] = model.calc_sat(neighbor)
            if round(probs[i]) > current_sat:
                no_better_neighbor = False
        if no_better_neighbor:
            break
        probs /= np.sum(probs)
        model.vars = neighbors[np.random.choice(
            range(1, model.var_num+1), p=probs[1:]) - 1]

    return {
        'SAT Clauses Number': model.sat_clauses_num,
        'Variables': [True if var == 1 else False for var in model.vars[1:]],
        'unSAT Clauses': [i for i, clause in enumerate(model.sat_clauses) if not clause]
    }
