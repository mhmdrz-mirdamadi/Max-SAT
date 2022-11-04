from pathlib import Path
from os import listdir
import numpy as np
import matplotlib.pyplot as plt
from src.SAT_model import SAT


def return_dict(model: SAT) -> dict:
    return {
        'SAT Clauses Number': model.sat_clauses_num,
        'Variables': [True if var == 1 else False for var in model.vars[1:]],
        'unSAT Clauses': [i+1 for i, clause in enumerate(model.sat_clauses) if not clause]
    }


def stochastic_hill_climbing(model: SAT, max_iterations=10000,
                             verbose=False, plot=False) -> dict:
    probs = np.zeros(model.var_num+1, dtype=float)
    current_fitness = model.fitness()
    best_so_far = return_dict(model)

    if verbose:
        log_str = ''

    if plot:
        history = []

    for _ in range(max_iterations):
        if current_fitness == model.clause_num:
            break

        neighbors = model.neighbors()[1:]

        for i, neighbor in enumerate(neighbors, 1):
            probs[i] = model.fitness(neighbor)

        if verbose:
            log_str += f'Neighbors: {list(map(int, probs))}, '

        probs /= np.sum(probs)
        chose_neighbor = np.random.choice(
            range(1, model.var_num+1), p=probs[1:]) - 1
        model.vars = neighbors[chose_neighbor]

        current_fitness = model.fitness()

        if current_fitness > best_so_far['SAT Clauses Number']:
            best_so_far = return_dict(model)

        if verbose:
            log_str += f'SAT: {current_fitness}\n'

        if plot:
            history.append(current_fitness)

    if verbose:
        Path('logs').mkdir(parents=True, exist_ok=True)
        with open(Path(f'logs/log{len(listdir("logs"))}.log'), 'w') as log:
            log.write('Algorithm: Stochastic Hill Climbing\n')
            log.write(f'Maximum Iterations: {max_iterations}\n\n')
            log.write(log_str)

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(range(max_iterations), history, c='red', linewidth=0.5)
        plt.xlabel('Iteration')
        plt.ylabel('SAT Clauses')
        plt.show()

    return best_so_far


def simulated_annealing(model: SAT, start_temp=10, stop_temp=0.01,
                        annealing_schedule=0.9999, verbose=False, plot=False) -> dict:
    current_fitness = model.fitness()
    best_so_far = return_dict(model)
    current_temp = start_temp

    if verbose:
        log_str = ''

    if plot:
        sat_history = []
        temp_history = []

    while current_temp > stop_temp:
        if verbose:
            log_str += f'Temperature: {current_temp:<8.5f}   '
            log_str += f'SAT: {current_fitness:<4}   '

        if plot:
            sat_history.append(current_fitness)
            temp_history.append(current_temp)

        if current_fitness == model.clause_num:
            break

        index = np.random.choice(range(1, model.var_num+1))
        next_sat = model.neighbors()[index]
        delta_e = model.fitness(next_sat) - current_fitness

        if verbose:
            log_str += f'Delta E: {delta_e:>2}   Probability: '

        if delta_e > 0:
            prob = 1.0
        else:
            prob = np.exp(delta_e/current_temp)

        choose = np.random.choice([True, False], p=[prob, 1-prob])

        if verbose:
            log_str += f'{prob:<4.2f}   Chosen: {choose}\n'

        if choose:
            model.vars = next_sat
            current_fitness += delta_e
            best_so_far = return_dict(model)
        else:
            model.fitness()

        current_temp *= annealing_schedule

    if verbose:
        Path('logs').mkdir(parents=True, exist_ok=True)
        with open(Path(f'logs/log{len(listdir("logs"))}.log'), 'w') as log:
            log.write('Algorithm: Simulated Annealing\n')
            log.write(f'Starting Temperature: {start_temp}\n')
            log.write(f'Stoping Temperature: {stop_temp}\n')
            log.write(f'Annealing Schedule: {annealing_schedule}\n\n')
            log.write(log_str)

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(temp_history, sat_history, c='red', linewidth=0.5)
        plt.axis([max(temp_history), min(temp_history),
                 min(sat_history), max(sat_history)])
        plt.xlabel('Temperature')
        plt.ylabel('SAT Clauses')
        plt.show()

    return best_so_far


def tabu_search(model: SAT, max_iterations=10000, tabu_tenure=20,
                verbose=False, plot=False) -> dict:
    current_fitness = model.fitness()
    best_so_far = return_dict(model)
    tabu_list = np.zeros(model.var_num+1, dtype=int)

    if verbose:
        log_str = ''

    if plot:
        history = []

    for _ in range(max_iterations):
        if current_fitness == model.clause_num:
            break

        neighbors = model.neighbors()[1:]
        best_fitness = 0
        best_neighbor = 0
        for i, neighbor in enumerate(neighbors, 1):
            if tabu_list[i] > 0:
                continue
            if (neighbor_fitnes := model.fitness(neighbor)) > best_fitness:
                best_fitness = neighbor_fitnes
                best_neighbor = i

        model.vars = neighbors[best_neighbor-1]

        tabu_list -= 1
        tabu_list[best_neighbor] = tabu_tenure

        current_fitness = model.fitness()

        if current_fitness > best_so_far['SAT Clauses Number']:
            best_so_far = return_dict(model)

        if verbose:
            log_str += f'SAT: {current_fitness}\n'

        if plot:
            history.append(current_fitness)

    if verbose:
        Path('logs').mkdir(parents=True, exist_ok=True)
        with open(Path(f'logs/log{len(listdir("logs"))}.log'), 'w') as log:
            log.write('Algorithm: Tabu Search\n')
            log.write(f'Maximum Iterations: {max_iterations}\n')
            log.write(f'Tabu Tenure: {tabu_tenure}\n\n')
            log.write(log_str)

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(range(max_iterations), history, c='red', linewidth=0.5)
        plt.xlabel('Iteration')
        plt.ylabel('SAT Clauses')
        plt.show()

    return best_so_far
