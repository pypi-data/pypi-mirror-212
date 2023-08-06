import sys
import time

from examples.time_tests.time_test_dice_precomp import get_queries_dice, get_input_events_dice
from examples.time_tests.time_test_independent_iterative import calculate_for_n_queries_indep_iter

MIN_QUERIES = 1
MAX_QUERIES = 250
STEP = 1


if __name__ == '__main__':
    if len(sys.argv) == 2:
        max_queries = int(sys.argv[1])
    elif len(sys.argv) == 1:
        max_queries = MAX_QUERIES
    else:
        raise Exception("Unexptected number of command line arguments")

    for n_queries in range(MIN_QUERIES, max_queries, STEP):
        start = time.time()
        calculate_for_n_queries_indep_iter(
            filename='../example3.pl',
            n=n_queries,
            query_generator=get_queries_dice,
            events_generator=get_input_events_dice,
        )
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
