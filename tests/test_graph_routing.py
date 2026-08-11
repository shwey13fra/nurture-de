"""Phase 11 — deterministic routing / retry-cap unit tests for the workflow graph.

    py -m unittest tests.test_graph_routing -v

These test the pure branch logic with NO API and NO model — especially the hard-capped retry
loop, which is the safety-critical invariant (an unbounded evaluator loop in a legal-deadline
domain is the wrong shape). The four end-to-end scenario paths are verified separately by running
src/graph.py (they cost API calls); this file pins the routing that must never regress.
"""

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

from graph import _route_intent, _route_profile, _route_evidence, _filters_from, MAX_RETRIES  # noqa: E402


class TestIntentRouting(unittest.TestCase):
    def test_medical(self):
        self.assertEqual(_route_intent({"intent": "medical"}), "medical")

    def test_informational(self):
        self.assertEqual(_route_intent({"intent": "informational"}), "informational")


class TestProfileRouting(unittest.TestCase):
    def test_complete(self):
        self.assertEqual(_route_profile({"complete": True}), "complete")

    def test_missing(self):
        self.assertEqual(_route_profile({"complete": False}), "missing")

    def test_absent_defaults_to_missing(self):
        self.assertEqual(_route_profile({}), "missing")


class TestEvidenceRetryCap(unittest.TestCase):
    def test_sufficient_proceeds(self):
        self.assertEqual(_route_evidence({"evidence_sufficient": True, "retry_count": 0}), "sufficient")

    def test_insufficient_first_try_loops(self):
        self.assertEqual(_route_evidence({"evidence_sufficient": False, "retry_count": 0}), "insufficient")

    def test_insufficient_second_try_loops(self):
        self.assertEqual(_route_evidence({"evidence_sufficient": False, "retry_count": 1}), "insufficient")

    def test_hard_cap_forces_exit_at_two(self):
        # THE invariant: at the cap the loop must exit even if evidence is still insufficient
        self.assertEqual(_route_evidence({"evidence_sufficient": False, "retry_count": MAX_RETRIES}),
                         "sufficient")

    def test_cannot_loop_beyond_cap(self):
        for rc in range(MAX_RETRIES, MAX_RETRIES + 5):
            self.assertEqual(_route_evidence({"evidence_sufficient": False, "retry_count": rc}),
                             "sufficient", f"loop escaped the cap at retry_count={rc}")

    def test_cap_is_two(self):
        self.assertEqual(MAX_RETRIES, 2)


class TestFilterMapping(unittest.TestCase):
    """The vocabulary bug that starved retrieval: employment_status 'employed' must map to the
    corpus user_type facet value 'employee', not pass through as 'employed'."""

    def test_employed_maps_to_employee(self):
        self.assertEqual(_filters_from({"employment_status": "employed"}), {"user_type": "employee"})

    def test_civil_servant_maps_through(self):
        self.assertEqual(_filters_from({"employment_status": "civil-servant"}),
                         {"user_type": "civil-servant"})

    def test_not_employed_adds_no_user_type_filter(self):
        self.assertEqual(_filters_from({"employment_status": "not-employed"}), {})

    def test_insurance_type_passes_through(self):
        self.assertEqual(_filters_from({"insurance_type": "statutory"}), {"insurance_type": "statutory"})

    def test_explicit_user_type_wins(self):
        self.assertEqual(_filters_from({"user_type": "student", "employment_status": "employed"}),
                         {"user_type": "student"})

    def test_empty_profile_no_filters(self):
        self.assertEqual(_filters_from({}), {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
