import time

from problog.logic import Term, Constant

from examples.example1 import CoinQuery, CoinInputClause, generate_precompilation
from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation, Query, InputClause


MIN_QUERIES = 1
MAX_QUERIES = 1000
STEP = 1


def get_queries(number_queries):
    return [
        CoinQuery('twoHeads', i)
        for i in range(number_queries)
    ]


def get_input_events(number_queries):
    input_events = []
    for i in range(number_queries):
        input_events.append(CoinInputClause('heads1', i, 0.5))
        input_events.append(CoinInputClause('heads2', i, 0.5))

    return input_events


def calculate_for_n_queries(n):
    precomp = generate_precompilation()

    return precomp.perform_queries(
        queries=get_queries(n),
        input_events=get_input_events(n),
    )


if __name__ == '__main__':
    for n_queries in range(MIN_QUERIES, MAX_QUERIES, STEP):
        start = time.time()
        calculate_for_n_queries(n_queries)
        end = time.time()

        print(
            '{}, {}'.format(
                n_queries, end - start
            )
        )
