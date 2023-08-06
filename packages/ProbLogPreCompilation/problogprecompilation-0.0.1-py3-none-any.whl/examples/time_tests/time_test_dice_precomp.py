import sys
import time

from examples.example1 import CoinQuery, CoinInputClause
from examples.time_tests.squirrel3 import squirrel3_choice, squirrel3_0to1
from examples.time_tests.time_test_independent_precomp import calculate_for_n_queries_indep_precomp

MIN_QUERIES = 1
MAX_QUERIES = 250
STEP = 1

DICE_WHICH_EVENT_SEED = 1
DICE_EVENT_LIKELYHOOD_SEED = 2


def get_queries_dice(number_queries):
    return {
        i: [CoinQuery('odd', i)]
        for i in range(number_queries)
    }


def get_random_event_dice(i):
    event = squirrel3_choice(i, ['one', 'two', 'three', 'four', 'five', 'six'], DICE_WHICH_EVENT_SEED)
    likelyhood = squirrel3_0to1(i, DICE_EVENT_LIKELYHOOD_SEED)

    return CoinInputClause(event, i, likelyhood)


def get_input_events_dice(number_queries):
    return {
        i: [get_random_event_dice(i)]
        for i in range(number_queries)
    }


if __name__ == '__main__':
    if len(sys.argv) == 2:
        max_queries = int(sys.argv[1])
    elif len(sys.argv) == 1:
        max_queries = MAX_QUERIES
    else:
        raise Exception("Unexptected number of command line arguments")

    for n_queries in range(MIN_QUERIES, max_queries, STEP):
        start = time.time()
        calculate_for_n_queries_indep_precomp(
            filename='../example3.pl',
            n=n_queries,
            query_generator=get_queries_dice,
            events_generator=get_input_events_dice,
            queries=[CoinQuery('odd', 0)],
            input_clauses=[
                CoinInputClause('one', 0, 0.0),
                CoinInputClause('two', 0, 0.0),
                CoinInputClause('three', 0, 0.0),
                CoinInputClause('four', 0, 0.0),
                CoinInputClause('five', 0, 0.0),
                CoinInputClause('six', 0, 0.0),
            ]
        )
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
