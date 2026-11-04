"""Actual optional-backend parity tests; absence of LangGraph is never a pass."""

import importlib.util
import unittest

from ants_kgmaer.experiments.runner import prepare_session
from ants_kgmaer.models.mock import MockAdapter
import test_dynamic_history


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "LangGraph dependency unavailable; optional runtime remains unverified")
class LangGraphIntegrationTests(unittest.TestCase):
    setUp = test_dynamic_history.DynamicHistoryTests.setUp

    def make_session(self):
        return prepare_session(MockAdapter(), self.repo, self.store, self.ids[2], self.config, None)

    def test_native_and_langgraph_have_identical_results(self):
        native, graph = self.make_session(), self.make_session()
        self.assertEqual(native.execute("agent", "native"), graph.execute("agent", "langgraph"))

    def test_restored_two_rounds_do_not_start_another_retrieval(self):
        native, graph = self.make_session(), self.make_session()
        for session in (native, graph):
            session.rounds = 2
            session.budget.calls = 2
        left, right = native.execute("agent", "native"), graph.execute("agent", "langgraph")
        self.assertEqual(left, right)
        self.assertEqual(right["retrieval_rounds"], 2)
        self.assertEqual(right["usage"]["calls"], 3)

    def test_restored_finalize_goes_directly_to_classification(self):
        native, graph = self.make_session(), self.make_session()
        for session in (native, graph):
            session.retrieval_done = True
            session.rounds = 1
            session.budget.calls = 1
        left, right = native.execute("agent", "native"), graph.execute("agent", "langgraph")
        self.assertEqual(left, right)
        self.assertEqual(right["usage"]["calls"], 2)


if __name__ == "__main__":
    unittest.main()
