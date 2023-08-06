import random
import time

from examples.example2 import FeedbackClause, FeedbackQuery, generate_precompilation
from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation


MIN_QUERIES = 1
MAX_QUERIES = 1000
STEP = 1


def get_queries(number_queries):
    return [
        FeedbackQuery('atTime', i)
        for i in range(number_queries)
    ]


def get_input_events(number_queries):
    input_events = []
    for i in range(number_queries):
        if random.choice([True, False]):
            input_events.append(FeedbackClause('increase', i, random.random()))
        else:
            input_events.append(FeedbackClause('decrease', i, random.random()))

    return input_events


def calculate_for_n_queries(n):
    precomp = generate_precompilation()

    return precomp.perform_queries(
        queries=get_queries(n),
        input_events=get_input_events(n),
        use_feedback=True
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
