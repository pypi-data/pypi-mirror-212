import sys
import time

from examples.example1 import CoinQuery, CoinInputClause
from examples.time_tests.squirrel3 import squirrel3_choice, squirrel3_0to1
from examples.time_tests.time_test_dice_precomp import get_queries_dice
from examples.time_tests.time_test_independent_precomp import calculate_for_n_queries_indep_precomp

MIN_QUERIES = 1
MAX_QUERIES = 250
STEP = 1

DICE_ONE_SEED = 1
DICE_TWO_SEED = 2
DICE_THREE_SEED = 3
DICE_FOUR_SEED = 4
DICE_FIVE_SEED = 5
DICE_SIX_SEED = 6


def get_input_events_all_dice(number_queries):
    return {
        i: [
            CoinInputClause('one', i, squirrel3_0to1(i, DICE_ONE_SEED)),
            CoinInputClause('two', i, squirrel3_0to1(i, DICE_TWO_SEED)),
            CoinInputClause('three', i, squirrel3_0to1(i, DICE_THREE_SEED)),
            CoinInputClause('four', i, squirrel3_0to1(i, DICE_FOUR_SEED)),
            CoinInputClause('five', i, squirrel3_0to1(i, DICE_FIVE_SEED)),
            CoinInputClause('six', i, squirrel3_0to1(i, DICE_SIX_SEED)),
        ]
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
            events_generator=get_input_events_all_dice,
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
