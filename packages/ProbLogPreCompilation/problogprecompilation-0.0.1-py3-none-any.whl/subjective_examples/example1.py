from problog import get_evaluatable
from problog.logic import Term, Constant
from problog.program import PrologString
from SLProbLog.SLProbLog import BetaSemiring, from_sl_opinion, BetaDistribution
import mpmath

from examples.example1 import CoinInputClause, generate_precompilation, QUERIES
from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation, Query, InputClause
from problog.logic import Term, Constant

from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation, Query, InputClause


class MyBetaSemiring(BetaSemiring):
    def parse(self, w):
        s_w = str(w)

        if s_w.startswith('w'):
            start = s_w.find('(') + 1
            end = s_w.find(')')
            return from_sl_opinion([mpmath.mpf(x) for x in w[start:end].replace(" ", "").split(',')])
        elif s_w.startswith('b'):
            return super().parse(w)
        else:
            raise Exception('The format of {} is not allowed for defining the uncertainty of a clause'.format(s_w))


class SubjectiveCoinInputClause(CoinInputClause):
    semiring = MyBetaSemiring()


INPUT_EVENTS = [
    # Timestamp 0
    SubjectiveCoinInputClause('heads1', 0, Term('b', 0.4, 0.2)),
    SubjectiveCoinInputClause('heads2', 0, Term('b', 0.7, 0.2)),
    # Timestamp 1
    SubjectiveCoinInputClause('heads1', 1, Term('b', 0.1, 0.2)),
    SubjectiveCoinInputClause('heads2', 1, Term('b', 0.1, 0.2)),
    # Timestamp 2
    SubjectiveCoinInputClause('heads1', 2, Term('b', 0.4, 0.2)),
    # Timestamp 3
    SubjectiveCoinInputClause('heads2', 3, Term('b', 0.7, 0.2)),
    # Timestamp 4
]


if __name__ == '__main__':
    semiring = MyBetaSemiring()

    precomp = generate_precompilation(
        filename='../examples/example1.pl',
        input_clauses=[SubjectiveCoinInputClause('heads1', 0), SubjectiveCoinInputClause('heads2', 0)],
        semiring=semiring
    )

    results = precomp.perform_queries(
        queries=QUERIES,
        input_events=INPUT_EVENTS,
        modify_out_probability=lambda v: semiring.parse(v).to_sl_opinion()
    )

    for k, v in results.items():
        print('{} -> {}'.format(k, v))

    # print()
    # print()


# if __name__ == '__main__':
#     with open('../examples/example1.pl', 'r') as f:
#         problog_code = ''.join([l for l in f])
#
#     problog_code += '''
#     b(0.4, 0.2)::heads1(0).
#     b(0.7, 0.2)::heads2(0).
#     b(0.1, 0.2)::heads1(1).
#     b(0.1, 0.2)::heads2(1).
#     b(0.4, 0.2)::heads1(2).
#     b(0.7, 0.2)::heads2(3).
#
#     query(twoHeads(0)).
#     query(someHeads(0)).
#     query(aHead(0,1)).
#     query(aHead(0,2)).
#
#     query(twoHeads(1)).
#     query(someHeads(1)).
#
#     query(twoHeads(2)).
#     query(someHeads(2)).
#
#     query(twoHeads(3)).
#     query(someHeads(3)).
#
#     query(twoHeads(4)).
#     query(someHeads(4)).
#     '''
#
#     prolog_string = PrologString(problog_code)
#
#     semiring = MyBetaSemiring()
#
#     knowledge = get_evaluatable(semiring=semiring).create_from(prolog_string, semiring=semiring)
#
#     for k, v in knowledge.evaluate(semiring=semiring).items():
#         print('{} -> {}'.format(k, semiring.parse(v).to_sl_opinion()))
#         # print('{} -> {}'.format(k, v))
