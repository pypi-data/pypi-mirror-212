import sys
import time

from examples.example1 import CoinQuery, CoinInputClause, generate_precompilation, DEFAULT_INPUT_CLAUSES
from examples.time_tests.squirrel3 import squirrel3_0to1

MIN_QUERIES = 1
MAX_QUERIES = 250
STEP = 1

HEADS1_SEED = 1
HEADS2_SEED = 2


def get_queries_indep(number_queries):
    return {
        i: [CoinQuery('twoHeads', i)]
        for i in range(number_queries)
    }


def get_input_events_indep(number_queries):
    return {
        i: [
            # Using squirrel3 to generate random floats between 0 and 1. squirrel3 provides a consistent value
            # throughout different executions and devices independently of call order, thus allowing for easy comparison
            CoinInputClause('heads1', i, squirrel3_0to1(i, seed=HEADS1_SEED)),
            CoinInputClause('heads2', i, squirrel3_0to1(i, seed=HEADS1_SEED))
        ]
        for i in range(number_queries)
    }


def calculate_for_n_queries_indep_precomp(filename, n, query_generator=get_queries_indep,
                                          events_generator=get_input_events_indep,
                                          queries=(CoinQuery('twoHeads', 0), ), input_clauses=DEFAULT_INPUT_CLAUSES):
    precomp = generate_precompilation(filename=filename, queries=queries, input_clauses=input_clauses)

    queries_dict = query_generator(n)
    input_dict = events_generator(n)

    res = {}
    for i in range(n):
        res.update(
            precomp.perform_queries(
                queries=queries_dict[i],
                input_events=input_dict[i]
            )
        )

    return res


if __name__ == '__main__':
    if len(sys.argv) == 2:
        max_queries = int(sys.argv[1])
    elif len(sys.argv) == 1:
        max_queries = MAX_QUERIES
    else:
        raise Exception("Unexptected number of command line arguments")

    for n_queries in range(MIN_QUERIES, max_queries, STEP):
        start = time.time()
        calculate_for_n_queries_indep_precomp('../example1.pl', n_queries)
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
