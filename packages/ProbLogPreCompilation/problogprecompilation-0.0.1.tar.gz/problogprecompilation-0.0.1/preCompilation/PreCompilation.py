import re
import sys

from problog import get_evaluatable
from problog.evaluator import SemiringSymbolic
from problog.logic import Constant, Term
from problog.program import PrologString


class PreCompilation(object):
    def __init__(self, precomp_args, model, evaluatable_name=None, semiring=None):
        self.precomp_input = [e.for_mock_model() for e in precomp_args.input_clauses]

        model = model + '\n' + '\n'.join(self.precomp_input)

        self.semiring = semiring

        self.precompilations = {}
        for query in precomp_args.queries:
            compiled_model = self._compile_model_with(model, query, evaluatable_name, semiring)

            nodes = self._get_nodes_for(compiled_model)

            default_probs = self._get_default_probs(compiled_model, nodes)

            self.precompilations[query.identifier] = {
                'model': compiled_model,
                'nodes': nodes,
                'default_probs': default_probs,
                'base_timestamp': query.timestamp
            }

    @staticmethod
    def _compile_model_with(model, query, evaluatable_name, semiring):
        prolog_string = PrologString(query.create_from_model(model))

        # return get_evaluatable(name='ddnnf').create_from(prolog_string, semiring=SemiringSymbolic())
        return get_evaluatable(name=evaluatable_name, semiring=semiring).create_from(prolog_string, semiring=semiring)

    def perform_queries(self, queries, input_events=(), use_feedback=False, modify_out_probability=None,
                        explanation=None):
        res = {}

        input_events = list(input_events)

        for query in queries:
            precompilation = self.precompilations.get(query.identifier)

            if not precompilation:
                raise Exception('One of the provided queries has not been precompiled')

            timestamp_difference = query.timestamp - precompilation['base_timestamp']

            knowledge = precompilation['model']

            self._update_knowledge_with(
                knowledge, input_events, precompilation['nodes'],
                precompilation['default_probs'], timestamp_difference
            )

            evaluation = knowledge.evaluate(semiring=self.semiring, explain=explanation)

            # Fix the evaluation to have the correct output timestamps
            fixed_evaluation = {}
            for k, v in evaluation.items():
                # new_k = Term(k.functor, k.args[0], Constant(k.args[1].functor + timestamp_difference))
                new_k = query.update_result_timestamp(k, timestamp_difference)

                if modify_out_probability:
                    v = modify_out_probability(v)

                fixed_evaluation[new_k] = v

            res.update(fixed_evaluation)

            if use_feedback:
                input_events += query.generate_feedback(evaluation, timestamp_difference)

        return res

    def _update_knowledge_with(self, knowledge, input_events, nodes, default_probs, timestamp_difference):
        marked_probabilities = {
            e.to_problog_with(
                timestamp=e.timestamp - timestamp_difference,
                probability=e.zero_probability()
            ).replace(' ', ''): e.generate_probability()
            for e in input_events
        }

        for p in self.precomp_input:
            node = nodes.get(p)

            if node:
                probability = self._find_probability(marked_probabilities, p)

                if probability:
                    knowledge._weights[node] = probability
                else:
                    knowledge._weights[node] = default_probs.get(node, Constant(0.0))

    @staticmethod
    def _find_probability(marked_probabilities, precomp_input_event):
        parsed_precomp_input_event = precomp_input_event.replace(' ', '')

        return marked_probabilities.get(parsed_precomp_input_event, None)

    def _get_nodes_for(self, knowledge, in_dict='named'):
        parsed_knowledge = {
            str(name): node
            for name, node in knowledge._names[in_dict].items()
        }

        return {
            i: parsed_knowledge[i.split('::')[1].strip()[:-1].replace(' ', '')]
            for i in self.precomp_input
            if i.split('::')[1].strip()[:-1].replace(' ', '') in parsed_knowledge
        }

    @classmethod
    def _get_default_probs(cls, knowledge, nodes):
        return {
            node: knowledge._weights[node]
            for node in nodes.values()
        }


class PreCompilationArguments(object):
    def __init__(self, input_clauses, queries, warnings=True):
        if warnings:
            for c in input_clauses:
                if not isinstance(c, InputClause):
                    print(
                        '{}, of class {}, is not a subclass of InputClause. This may cause problems if not all the '
                        'abstract methods are implemented. Pass warnings=False to disable this warning.'.format(
                            c, type(c)
                        ),
                        file=sys.stderr
                    )

            for q in queries:
                if not isinstance(q, Query):
                    print(
                        '{}, of class {}, is not a subclass of Query. This may cause problems if not all the '
                        'abstract methods are implemented. Pass warnings=False to disable this warning.'.format(
                            q, type(q)
                        ),
                        file=sys.stderr
                    )

        self.input_clauses = input_clauses
        self.queries = queries


class InputClause(object):
    semiring = None

    def __init__(self, identifier, timestamp, probability=None):
        self.identifier = identifier
        self.timestamp = timestamp

        if probability is None:
            probability = self.zero_probability()
        self.probability = probability

    @classmethod
    def zero_probability(cls):
        if cls.semiring is None:
            return 0.0

        return cls.semiring.parse(cls.semiring.zero())

    def get_clause_format(self):
        raise NotImplementedError(
            'This method should return the format that this clause needs to have in the form of a string.'
            '"{identifier}", "{timestamp}" and "{probability}" should be used as placeholders on the places where'
            'they will need to go. e.g. "{probability}::{identifier}({timestamp}).'
        )

    def to_problog(self):
        return self.to_problog_with()

    def to_problog_with(self, identifier=None, timestamp=None, probability=None):
        if identifier is None:
            identifier = self.identifier
        if timestamp is None:
            timestamp = self.timestamp
        if probability is None:
            probability = self.probability

        return self.get_clause_format().format(
            identifier=identifier,
            timestamp=timestamp,
            probability=probability
        )

    def for_mock_model(self):
        raise NotImplementedError(
            'This method should return a ProbLog string defining the clause for the mock model. The probability '
            'returned by this method will be used as the default probability for each case. A default probability of '
            '0 is recommended, as then you will only need to pass the events that you want to actually happen.'
        )

    def generate_probability(self):
        return Constant(self.probability)

    def __str__(self):
        return self.to_problog()

    def __repr__(self):
        return self.to_problog()


class Query(object):
    def __init__(self, identifier, timestamp):
        self._identifier = identifier
        self.timestamp = timestamp

    @property
    def identifier(self):
        return self._identifier

    def get_query_format(self):
        raise NotImplementedError(
            'This method should return the format that this query needs to have in the form of a string.'
            '"{identifier}" and "{timestamp}" should be used as placeholders on the places where'
            'they will need to go. e.g. "query({identifier}({timestamp})).'
        )

    def to_problog(self):
        return self.to_problog_with()

    def to_problog_with(self, identifier=None, timestamp=None):
        if identifier is None:
            identifier = self._identifier
        if timestamp is None:
            timestamp = self.timestamp

        return self.get_query_format().format(
            identifier=identifier,
            timestamp=timestamp
        )

    def create_from_model(self, model):
        return model + self.to_problog()

    def update_result_timestamp(self, result, timestamp_difference):
        raise NotImplementedError(
            'This method should return a new term with the same values and format as result but updating the timestamp'
            'with the provided difference.'
        )

    def generate_feedback(self, evaluation, timestamp_difference):
        raise NotImplementedError(
            'This method should return a list of objects inheriting from InputClause. This list should contain the '
            'clauses that need to be used as a feedback. These should be created from the results found in evaluation. '
            'Only required if feedback is being used (will not be called otherwise).'
        )
