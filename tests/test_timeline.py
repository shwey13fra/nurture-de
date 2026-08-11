"""Phase 9 — unit tests for the deterministic Mutterschutz timeline tool.

    py -m unittest tests.test_timeline -v
    (or)  .venv/Scripts/python.exe -m unittest tests.test_timeline -v

Real assertions, not smoke checks. EVERY expected date below is hand-calculated and written
as a literal — never asserted against what the function returns. The whole point of this phase
is that Python (not a language model) applies the legal date arithmetic, so the tests must pin
the arithmetic independently.

Ground truth (verified against the corpus, chunk_ids in the asserts):
  - protection starts 6 weeks (42 days) before the expected date of birth
  - protection normally ends 8 weeks (56 days) after birth
  - born BEFORE the expected date (not premature): the after-period is lengthened by exactly
    the days the child came early, so the total stays 14 weeks
  - born AFTER the expected date: the full 8 weeks after the actual birth still apply
  - premature / multiple / disability-diagnosed-within-8-weeks: 12 weeks (84 days) after birth
  - Elterngeld: apply after birth, within the first 3 months of life (max 3 months retroactive)
"""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from tools.timeline import calculate_timeline, add_months  # noqa: E402

# chunk_ids the dates must trace back to (hand-known from the corpus, not imported from the module)
START_CHUNK = "fam_mutterschutz__wie-lange-besteht-der-mutterschutz-vor-und-nach-der-geburt__ac481a5a"
MULTIPLE_CHUNK = "fam_mutterschutz__welche-regelungen-gelten-wenn-ich-zwillinge-oder-weitere-meh__e7d7850e"
DISABILITY_CHUNK = "fam_mutterschutz__welche-regelungen-gelten-fuer-die-mutterschutzfrist-bei-eine__cef1fbda"
ELTERNGELD_CHUNK = "fam_elterngeld_antrag__wie-kann-ich-elterngeld-beantragen__ab9bc2fa"
BEAMTIN_CHUNK = "fam_mutterschutz__welche-regelungen-fuer-den-mutterschutz-gelten-fuer-beamtinn__eb325d8b"

TODAY = date(2026, 8, 11)          # fixed clock so every test is deterministic
CHUNK_IDS_IN_RESULT = lambda r: {x["source_chunk"] for x in r["rules_applied"]}


class TestAddMonths(unittest.TestCase):
    """Month arithmetic must clamp to the last valid day (used for the Elterngeld window)."""

    def test_clamps_to_leap_feb(self):
        self.assertEqual(add_months(date(2027, 11, 30), 3), date(2028, 2, 29))  # 2028 is a leap year

    def test_clamps_to_nonleap_feb(self):
        self.assertEqual(add_months(date(2028, 11, 30), 3), date(2029, 2, 28))

    def test_clamps_jan31_plus_one(self):
        self.assertEqual(add_months(date(2027, 1, 31), 1), date(2027, 2, 28))

    def test_plain_add(self):
        self.assertEqual(add_months(date(2027, 3, 15), 3), date(2027, 6, 15))


class TestStandardPlanning(unittest.TestCase):
    """A single pregnancy, employed, no birth yet: dates anchored on the expected date."""

    def setUp(self):
        self.r = calculate_timeline("2027-03-15", "employed", today=TODAY)

    def test_expected_birth_echoed(self):
        self.assertEqual(self.r["expected_birth"], "2027-03-15")

    def test_no_actual_birth_in_planning(self):
        self.assertIsNone(self.r["actual_birth"])

    def test_protection_starts_6_weeks_before(self):
        self.assertEqual(self.r["protection_starts"], "2027-02-01")   # 2027-03-15 minus 42 days

    def test_protection_ends_8_weeks_after(self):
        self.assertEqual(self.r["protection_ends"], "2027-05-10")     # 2027-03-15 plus 56 days

    def test_elterngeld_within_3_months(self):
        self.assertEqual(self.r["elterngeld_apply_by"], "2027-06-15")  # add_months(due, 3)


class TestBirthOnExpectedDate(unittest.TestCase):
    def test_ends_8_weeks_after_actual(self):
        r = calculate_timeline("2027-03-15", "employed",
                               actual_birth_date="2027-03-15", today=date(2027, 3, 15))
        self.assertEqual(r["protection_starts"], "2027-02-01")
        self.assertEqual(r["protection_ends"], "2027-05-10")          # birth + 56 days
        self.assertEqual(r["actual_birth"], "2027-03-15")


class TestBirthTwoWeeksEarly(unittest.TestCase):
    """Not premature: the after-period is lengthened by exactly the days come early."""

    def setUp(self):
        self.r = calculate_timeline("2027-03-15", "employed",
                                    actual_birth_date="2027-03-01", today=date(2027, 3, 5))

    def test_protection_ends(self):
        # born 14 days early -> after-period = 56 + 14 = 70 days from birth -> 2027-03-01 + 70
        self.assertEqual(self.r["protection_ends"], "2027-05-10")

    def test_after_period_extended_by_exactly_those_days(self):
        ends = date.fromisoformat(self.r["protection_ends"])
        birth = date.fromisoformat(self.r["actual_birth"])
        self.assertEqual((ends - birth).days, 70)                    # 8 weeks + 14 days


class TestBirthTwoWeeksLate(unittest.TestCase):
    def setUp(self):
        self.r = calculate_timeline("2027-03-15", "employed",
                                    actual_birth_date="2027-03-29", today=date(2027, 4, 1))

    def test_full_8_weeks_after_actual(self):
        self.assertEqual(self.r["protection_ends"], "2027-05-24")    # 2027-03-29 + 56 days

    def test_after_period_is_exactly_56_days(self):
        ends = date.fromisoformat(self.r["protection_ends"])
        birth = date.fromisoformat(self.r["actual_birth"])
        self.assertEqual((ends - birth).days, 56)


class TestMultipleBirth(unittest.TestCase):
    def test_planning_12_weeks(self):
        r = calculate_timeline("2027-03-15", "employed", multiple_birth=True, today=TODAY)
        self.assertEqual(r["protection_ends"], "2027-06-07")         # 2027-03-15 + 84 days
        self.assertIn(MULTIPLE_CHUNK, CHUNK_IDS_IN_RESULT(r))

    def test_actual_early_does_not_stack_with_extension(self):
        # extended = flat 12 weeks from ACTUAL birth; the early-days adjustment does NOT apply
        r = calculate_timeline("2027-03-15", "employed", multiple_birth=True,
                               actual_birth_date="2027-03-01", today=date(2027, 3, 5))
        self.assertEqual(r["protection_ends"], "2027-05-24")         # 2027-03-01 + 84 days
        ends = date.fromisoformat(r["protection_ends"])
        birth = date.fromisoformat(r["actual_birth"])
        self.assertEqual((ends - birth).days, 84)


class TestYearBoundary(unittest.TestCase):
    def setUp(self):
        self.r = calculate_timeline("2027-01-05", "employed", today=TODAY)

    def test_starts_crosses_into_previous_year(self):
        self.assertEqual(self.r["protection_starts"], "2026-11-24")  # 2027-01-05 minus 42 days

    def test_ends(self):
        self.assertEqual(self.r["protection_ends"], "2027-03-02")    # 2027-01-05 plus 56 days


class TestLeapYear(unittest.TestCase):
    """Subtraction crossing 29 Feb 2028 (a leap year)."""

    def setUp(self):
        self.r = calculate_timeline("2028-03-10", "employed", today=date(2028, 2, 1))

    def test_starts_crosses_leap_feb(self):
        self.assertEqual(self.r["protection_starts"], "2028-01-28")  # 42 days before 2028-03-10

    def test_ends(self):
        self.assertEqual(self.r["protection_ends"], "2028-05-05")    # 2028-03-10 plus 56 days


class TestElterngeldWindowLeapClamp(unittest.TestCase):
    """Elterngeld date is add_months(birth, 3); month-end + leap must clamp."""

    def setUp(self):
        self.r = calculate_timeline("2027-11-15", "employed",
                                    actual_birth_date="2027-11-30", today=date(2027, 12, 1))

    def test_protection_ends_late_birth(self):
        self.assertEqual(self.r["protection_ends"], "2028-01-25")    # 2027-11-30 + 56 days

    def test_elterngeld_apply_by_clamped(self):
        self.assertEqual(self.r["elterngeld_apply_by"], "2028-02-29")  # add_months(2027-11-30, 3)

    def test_elterngeld_rule_cited(self):
        self.assertIn(ELTERNGELD_CHUNK, CHUNK_IDS_IN_RESULT(self.r))


class TestTraceability(unittest.TestCase):
    """Every shown date must trace to a rule carrying a real corpus chunk_id and authority."""

    def setUp(self):
        self.r = calculate_timeline("2027-03-15", "employed", today=TODAY)

    def test_rules_applied_nonempty(self):
        self.assertTrue(self.r["rules_applied"])

    def test_start_and_end_cite_the_timeline_chunk(self):
        self.assertIn(START_CHUNK, CHUNK_IDS_IN_RESULT(self.r))

    def test_every_rule_has_chunk_authority_and_date(self):
        for rule in self.r["rules_applied"]:
            self.assertTrue(rule["rule"])
            self.assertTrue(rule["source_chunk"])
            self.assertTrue(rule["authority"])
            self.assertTrue(rule["authority_tier"])
            self.assertTrue(rule["last_verified"])

    def test_certificate_caveat_present(self):
        joined = " ".join(self.r["caveats"]).lower()
        self.assertTrue(("doctor" in joined or "midwife" in joined) and "certificate" in joined)

    def test_no_amounts_or_eligibility(self):
        # dates only — the tool must never state a euro amount or an eligibility verdict
        blob = " ".join(self.r["caveats"] + [x["rule"] for x in self.r["rules_applied"]]).lower()
        self.assertNotIn("eur", blob)
        self.assertNotIn("eligible", blob)


class TestCivilServant(unittest.TestCase):
    """Verbeamtet -> the general MuSchG dates may not apply; flag the separate regime."""

    def setUp(self):
        self.r = calculate_timeline("2027-03-15", "civil-servant", today=TODAY)

    def test_personalstelle_in_confirmation(self):
        joined = " ".join(self.r["needs_confirmation_from"]).lower()
        self.assertIn("personalstelle", joined)

    def test_separate_regime_caveat(self):
        joined = " ".join(self.r["caveats"]).lower()
        self.assertTrue("mutterschutzverordnung" in joined or "separate" in joined)

    def test_beamtin_rule_cited(self):
        self.assertIn(BEAMTIN_CHUNK, CHUNK_IDS_IN_RESULT(self.r))


class TestInvalidInput(unittest.TestCase):
    def test_past_due_date(self):
        with self.assertRaises(ValueError):
            calculate_timeline("2020-01-01", "employed", today=TODAY)

    def test_implausibly_far_future(self):
        with self.assertRaises(ValueError):
            calculate_timeline("2030-01-01", "employed", today=TODAY)

    def test_malformed_string(self):
        with self.assertRaises(ValueError):
            calculate_timeline("not-a-date", "employed", today=TODAY)

    def test_actual_birth_in_future(self):
        with self.assertRaises(ValueError):
            calculate_timeline("2027-03-15", "employed",
                               actual_birth_date="2027-01-01", today=TODAY)

    def test_unknown_employment_status(self):
        with self.assertRaises(ValueError):
            calculate_timeline("2027-03-15", "astronaut", today=TODAY)


if __name__ == "__main__":
    unittest.main(verbosity=2)
