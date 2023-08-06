import time

from examples.example2 import generate_precompilation
from examples.old_time_tests.time_test_recursivity import get_input_events, get_queries, MIN_QUERIES, MAX_QUERIES, STEP


def calculate_for_n_queries_feedback(n, input_events, queries):
    precomp = generate_precompilation()

    in_events = input_events(n)
    queries = queries(n)

    feedback_value = None

    res = {}
    for i in range(n):
        query = queries[i]

        iteration_in_events = [in_events[i]]
        if feedback_value:
            iteration_in_events += feedback_value

        evaluation = precomp.perform_queries(
            queries=[query],
            input_events=iteration_in_events,
            use_feedback=True
        )

        feedback_value = query.generate_feedback(evaluation, timestamp_difference=i)

        res.update(evaluation)

    return res


if __name__ == '__main__':
    for n_queries in range(MIN_QUERIES, MAX_QUERIES, STEP):
        start = time.time()
        calculate_for_n_queries_feedback(n_queries, get_input_events, get_queries)
        end = time.time()

        print(
            '{}, {}'.format(
                n_queries, end - start
            )
        )
