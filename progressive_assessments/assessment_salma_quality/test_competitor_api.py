"""
Competitor Intelligence API  –  Exploration & Regression Tests
==============================================================

HOW TO USE THIS FILE
--------------------
1. Start the API first:
      python competitor_intelligence_api.py

2. Run the exploration suite (manual discovery):
      python test_competitor_api.py

3. Run the automated regression tests (pytest):
      pytest test_competitor_api.py -v

The exploration functions guide you through discovering issues.
The pytest classes at the bottom are starter shells for you to complete.
"""

import requests
import json
import sys
import pytest

API_URL = "http://localhost:8001"


# ══════════════════════════════════════════════════════════════
#  EXPLORATION SUITE  —  run with: python test_competitor_api.py
# ══════════════════════════════════════════════════════════════

def explore_basic_analysis():
    """Does a standard detailed-format query return the right competitor?"""
    print("\n" + "=" * 60)
    print("EXPLORE 1: Basic Analysis — detailed format")
    print("=" * 60)

    payload = {
        "query": "What is their current market position?",
        "competitor": "PhosphoTech",
        "format": "detailed",
    }
    r = requests.post(f"{API_URL}/analyze", json=payload)
    result = r.json()

    correct_name = "PhosphoTech" in result.get("summary", "")
    print(f"  Status code  : {r.status_code}")
    print(f"  Summary      : {result.get('summary', '—')}")
    print(f"  Confidence   : {result.get('confidence', '—')}")
    print(f"  Name check   : {'✓ PhosphoTech mentioned' if correct_name else '⚠️  WRONG or MISSING name'}")


def explore_brief_format():
    """Run the same brief-format query 4 times — does the name stay consistent?"""
    print("\n" + "=" * 60)
    print("EXPLORE 2: Brief Format — repeat 4×")
    print("=" * 60)
    print("  Requesting competitor: PhosphoTech")

    all_correct = True
    for i in range(1, 5):
        payload = {
            "query": "What is their current market position?",
            "competitor": "PhosphoTech",
            "format": "brief",
        }
        r = requests.post(f"{API_URL}/analyze", json=payload)
        result = r.json()
        summary = result.get("summary", "")
        correct = "PhosphoTech" in summary
        if not correct:
            all_correct = False
        label = "✓" if correct else "⚠️ "
        print(f"  Attempt {i}: {label}  {summary[:70]}")

    if all_correct:
        print("\n  ✓ All summaries mention PhosphoTech correctly.")
    else:
        print("\n  ⚠️  Some summaries mention a DIFFERENT competitor — investigate!")


def explore_unknown_competitor():
    """What happens when the competitor isn't in the database?"""
    print("\n" + "=" * 60)
    print("EXPLORE 3: Unknown Competitor")
    print("=" * 60)

    payload = {
        "query": "What are their recent strategic moves?",
        "competitor": "UnknownCorp",
    }
    r = requests.post(f"{API_URL}/analyze", json=payload)
    result = r.json()

    print(f"  Status code    : {r.status_code}")
    print(f"  Summary        : '{result.get('summary', '—')}'")
    print(f"  Insights count : {len(result.get('insights', []))}")
    print(f"  Confidence     : {result.get('confidence', '—')}")

    if r.status_code == 200 and not result.get("summary"):
        print(
            "\n  ⚠️  API returned HTTP 200 with empty data.\n"
            "      Should this be an error? What would an analyst think?"
        )
    elif r.status_code in (400, 404, 422):
        print(f"\n  ✓ API correctly returned HTTP {r.status_code} for unknown competitor.")


def explore_reproducibility():
    """Does the same query return the same result each time?"""
    print("\n" + "=" * 60)
    print("EXPLORE 4: Reproducibility — same query, 3×")
    print("=" * 60)

    payload = {
        "query": "What is their market share?",
        "competitor": "AgriGlobal",
        "format": "detailed",
    }

    confidences = []
    for i in range(1, 4):
        r = requests.post(f"{API_URL}/analyze", json=payload)
        conf = r.json().get("confidence")
        confidences.append(conf)
        print(f"  Attempt {i}: confidence = {conf}")

    unique_values = set(confidences)
    if len(unique_values) == 1:
        print("\n  ✓ Confidence is stable across calls.")
    else:
        print(
            f"\n  ⚠️  Confidence varies: {confidences}\n"
            "      Can you reproduce a specific result for debugging? Can you track quality over time?"
        )


def explore_format_validation():
    """Does the API validate the `format` field?"""
    print("\n" + "=" * 60)
    print("EXPLORE 5: Format Validation")
    print("=" * 60)

    invalid_formats = ["executive", "summary", "quick", "BRIEF", "123"]

    for fmt in invalid_formats:
        payload = {
            "query": "What is their market position?",
            "competitor": "NutriCorp",
            "format": fmt,
        }
        r = requests.post(f"{API_URL}/analyze", json=payload)
        if r.status_code in (400, 422):
            print(f"  format='{fmt}' → ✓ Rejected with HTTP {r.status_code}")
        else:
            print(
                f"  format='{fmt}' → ⚠️  Accepted silently (HTTP {r.status_code}). "
                "Is the caller told their format was ignored?"
            )


def explore_batch_name_consistency():
    """In a batch request with brief format, do all summaries name the right competitor?"""
    print("\n" + "=" * 60)
    print("EXPLORE 6: Batch — brief format name consistency")
    print("=" * 60)

    payload = {
        "queries": [
            {"query": "Market position?", "competitor": "PhosphoTech", "format": "brief"},
            {"query": "Market position?", "competitor": "AgriGlobal",  "format": "brief"},
            {"query": "Market position?", "competitor": "NutriCorp",   "format": "brief"},
        ]
    }
    r = requests.post(f"{API_URL}/analyze/batch", json=payload)
    analyses = r.json().get("analyses", [])

    for a in analyses:
        requested = a["competitor"]
        summary   = a.get("summary", "")
        correct   = requested in summary
        print(
            f"  Requested: {requested:12s} | Summary: {summary[:55]}… "
            f"| {'✓' if correct else '⚠️  WRONG NAME'}"
        )


# ══════════════════════════════════════════════════════════════
#  REGRESSION TESTS  —  run with: pytest test_competitor_api.py -v
#  Fill in the TODO sections based on what you discovered above.
# ══════════════════════════════════════════════════════════════

class TestCompetitorAccuracy:
    """The summary must always mention the competitor that was requested."""

    def test_detailed_format_names_correct_competitor(self):
        """
        In 'detailed' format the summary should include the requested competitor's name.
        """
        # TODO: implement this test
        # Hint: request PhosphoTech in detailed format, assert "PhosphoTech" in summary
        pass

    def test_brief_format_names_correct_competitor(self):
        """
        In 'brief' format the summary must still reference the requested competitor.
        Run multiple times to catch intermittent failures.
        """
        # TODO: implement this test
        # Hint: run the same brief-format request 5 times, assert the name each time
        pass

    def test_batch_brief_format_names_correct_competitors(self):
        """
        Each entry in a batch response must name its own requested competitor.
        """
        # TODO: implement this test
        pass


class TestErrorHandling:
    """The API must communicate failures clearly rather than returning empty 200s."""

    def test_unknown_competitor_returns_http_error(self):
        """
        Querying a competitor not in the knowledge base should return a 4xx error,
        not a silent HTTP 200 with empty data.
        """
        # TODO: implement this test
        # Hint: post with competitor="NonExistentCompany", assert status_code != 200
        pass

    def test_invalid_format_returns_validation_error(self):
        """
        Passing an unsupported format value should return HTTP 422 or 400,
        not a silent success.
        """
        # TODO: implement this test
        # Hint: post with format="executive", assert status_code in (400, 422)
        pass


class TestReproducibility:
    """The same inputs must always produce the same outputs."""

    def test_same_query_same_confidence_score(self):
        """
        Identical requests must return identical confidence scores.
        A score that changes on every call cannot be tracked or used for regression.
        """
        # TODO: implement this test
        # Hint: post the same payload twice, assert result1["confidence"] == result2["confidence"]
        pass


# ══════════════════════════════════════════════════════════════
#  CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  COMPETITOR INTELLIGENCE API — EXPLORATION SUITE")
    print("=" * 70)
    print("\nMake sure the API is running:  python competitor_intelligence_api.py")
    print("\nPress Enter to start…", end="")
    input()

    try:
        r = requests.get(f"{API_URL}/health")
        r.raise_for_status()
        print(f"\n✓ API is reachable (version {r.json().get('version', '?')})\n")
    except Exception as e:
        print(f"\n✗ Cannot connect to API at {API_URL}:  {e}")
        sys.exit(1)

    explore_basic_analysis()
    explore_brief_format()
    explore_unknown_competitor()
    explore_reproducibility()
    explore_format_validation()
    explore_batch_name_consistency()

    print("\n" + "=" * 70)
    print("  EXPLORATION COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Write up each ⚠️  finding as a bug report.")
    print("  2. Fill in the pytest TODO stubs and run:  pytest test_competitor_api.py -v")
    print()
