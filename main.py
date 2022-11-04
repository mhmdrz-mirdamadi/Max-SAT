from pathlib import Path
from argparse import ArgumentParser
from SAT_model import SAT
from solver import simulated_annealing, stochastic_hill_climbing


if __name__ == '__main__':
    parser = ArgumentParser(description='args')

    parser.add_argument('-i', '--input', default=Path('tests/Max-Sat_20_80.txt'),
                        type=Path, help='Input sample')
    parser.add_argument('-a', '--algorithm', default='sa', type=str,
                        help='Algorithm to solve MAX-SAT')
    parser.add_argument('--iterations', default=10000, type=int,
                        help='Maximum iterations number for stochastic hill climbing')
    parser.add_argument('--start-t', default=10, type=float,
                        help='Starting Temperature for simulated annealing')
    parser.add_argument('--stop-t', default=0.01, type=float,
                        help='Stoping Temperature for simulated annealing')
    parser.add_argument('--annealing-schedule', default=0.9999, type=float,
                        help='Annealing schedule for simulated annealing')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-p', '--plot', action='store_true')

    args = parser.parse_args()

    mySat = SAT()
    mySat.initialize_model(args.input)

    if args.algorithm.lower() == 'shc':
        res = stochastic_hill_climbing(
            mySat, args.iterations, args.verbose, args.plot)
    elif args.algorithm.lower() == 'sa':
        res = simulated_annealing(mySat, args.start_t, args.stop_t,
                                  args.annealing_schedule, args.verbose, args.plot)
    else:
        raise 'Invalid algorithm argument'

    [print(f'{key}: {value}') for key, value in res.items()]
