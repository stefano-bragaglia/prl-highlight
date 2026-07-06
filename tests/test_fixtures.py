from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "prl_examples"

EXPECTED_FILENAMES = {
    "aggregation.prl",
    "blocks_world.prl",
    "compact_patterns.prl",
    "disjunction.prl",
    "event_stream.prl",
    "existence_check.prl",
    "family_tree.prl",
    "fraud_detection.prl",
    "identity_key.prl",
    "imported_types.prl",
    "inheritance.prl",
    "loan_application.prl",
    "negation.prl",
    "self_modify.prl",
    "sharing.prl",
    "temperature_alarm.prl",
    "universal.prl",
}


def test_fixtures_present():
    actual = {p.name for p in FIXTURES_DIR.glob("*.prl")}
    assert actual == EXPECTED_FILENAMES


def test_fixtures_nonempty():
    for name in EXPECTED_FILENAMES:
        path = FIXTURES_DIR / name
        assert path.stat().st_size > 0, f"{name} is empty"
