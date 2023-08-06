import time

from examples.example1 import CoinQuery, CoinInputClause, generate_precompilation

MIN_QUERIES = 1
MAX_QUERIES = 1000
STEP = 1


def get_queries(number_queries):
    return {
        i: [CoinQuery('twoHeads', i)]
        for i in range(number_queries)
    }


def get_input_events(number_queries):
    return {
        i: [CoinInputClause('heads1', i, 0.5), CoinInputClause('heads2', i, 0.5)]
        for i in range(number_queries)
    }


def calculate_for_n_queries(n):
    precomp = generate_precompilation()

    queries_dict = get_queries(n)
    input_dict = get_input_events(n)

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
    for n_queries in range(MIN_QUERIES, MAX_QUERIES, STEP):
        start = time.time()
        calculate_for_n_queries(n_queries)
        end = time.time()

        print(
            '{}, {}'.format(
                n_queries, end - start
            )
        )
