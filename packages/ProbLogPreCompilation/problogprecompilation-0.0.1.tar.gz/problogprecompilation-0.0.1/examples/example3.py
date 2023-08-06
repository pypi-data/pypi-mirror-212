from problog.logic import Term, Constant

from examples.example1 import generate_precompilation, CoinInputClause, CoinQuery
from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation, Query, InputClause


EXAMPLE3_QUERIES = [
    # Timestamp 0
    CoinQuery('even', 0),
    CoinQuery('odd', 0),
    # Timestamp 1
    CoinQuery('even', 1),
    CoinQuery('odd', 1),
    # Timestamp 2
    CoinQuery('even', 2),
    CoinQuery('odd', 2),
    # Timestamp 3
    CoinQuery('even', 3),
    CoinQuery('odd', 3),
    # Timestamp 4
    CoinQuery('even', 4),
    CoinQuery('odd', 4),
    # Timestamp 5
    CoinQuery('even', 5),
    CoinQuery('odd', 5),
    # Timestamp 6
    CoinQuery('even', 6),
    CoinQuery('odd', 6),
    # Timestamp 7
    CoinQuery('even', 7),
    CoinQuery('odd', 7),
    # Timestamp 8
    CoinQuery('even', 8),
    CoinQuery('odd', 8),
]

EXAMPLE3_INPUT_EVENTS = [
    # Timestamp 0
    CoinInputClause('one', 0, 0.4),
    # Timestamp 1
    CoinInputClause('two', 1, 0.1),
    # Timestamp 2
    CoinInputClause('three', 2, 0.4),
    # Timestamp 3
    CoinInputClause('four', 3, 0.7),
    # Timestamp 4
    CoinInputClause('five', 4, 0.5),
    # Timestamp 5
    CoinInputClause('six', 5, 0.7),
    # Timestamp 6
    CoinInputClause('four', 6, 0.7),
    CoinInputClause('two', 6, 0.3),
    # Timestamp 7
    CoinInputClause('six', 7, 0.5),
    CoinInputClause('one', 7, 0.4),
    # Timestamp 8
]


if __name__ == '__main__':
    precomp = generate_precompilation(
        filename='example3.pl',
        input_clauses=[
            CoinInputClause('one', 0),
            CoinInputClause('two', 0),
            CoinInputClause('three', 0),
            CoinInputClause('four', 0),
            CoinInputClause('five', 0),
            CoinInputClause('six', 0),
        ],
        queries=[
            CoinQuery('odd', 0),
            CoinQuery('even', 0)
        ]
    )

    results = precomp.perform_queries(
        queries=EXAMPLE3_QUERIES,
        input_events=EXAMPLE3_INPUT_EVENTS,
    )

    for k, v in results.items():
        print('{} -> {}'.format(k, v))
