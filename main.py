from pathlib import Path
from argparse import ArgumentParser
from src.SAT_model import SAT
from src.solver import simulated_annealing, stochastic_hill_climbing, tabu_search


if __name__ == '__main__':
    parser = ArgumentParser(description='args')

    parser.add_argument('--input', default=Path('tests/Max-Sat_20_80.txt'),
                        type=Path, help='Input sample')
    parser.add_argument('--algorithm', default='sa', type=str,
                        choices=['shc', 'sa', 'ts'],
                        help='Algorithm to solve MAX-SAT\n' +
                        'SHC (Stochastic Hill Climbing)\n' +
                        'SA (Simulated Annealing)\n' +
                        'TS (Tabu Search')
    parser.add_argument('--iterations', default=10000, type=int,
                        help='Maximum iterations number for stochastic hill climbing or tabu search')
    parser.add_argument('--start-t', default=10, type=float,
                        help='Starting Temperature for simulated annealing')
    parser.add_argument('--stop-t', default=0.01, type=float,
                        help='Stoping Temperature for simulated annealing')
    parser.add_argument('--annealing-schedule', default=0.9999, type=float,
                        help='Annealing schedule for simulated annealing')
    parser.add_argument('--tabu-tenure', default=20, type=int,
                        help='Tabu tenure for tabu search')
    parser.add_argument('-v', action='store_true',
                        help='Verbose in /logs folder')
    parser.add_argument('-p', action='store_true', help='Show plot')

    args = parser.parse_args()

    mySat = SAT()
    mySat.initialize_model(args.input)

    if args.algorithm.lower() == 'shc':
        res = stochastic_hill_climbing(
            mySat, args.iterations, args.v, args.p)
    elif args.algorithm.lower() == 'sa':
        res = simulated_annealing(mySat, args.start_t, args.stop_t,
                                  args.annealing_schedule, args.v, args.p)
    elif args.algorithm.lower() == 'ts':
        res = tabu_search(mySat, args.iterations,
                          args.tabu_tenure, args.v, args.p)

    [print(f'{key}: {value}') for key, value in res.items()]
