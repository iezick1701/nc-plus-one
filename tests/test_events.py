import pytest
from db.seed import read_file
from db.connection import get_connection


@pytest.fixture
def test_file():
    return read_file("events")


def test_extract_list(test_file):
    assert isinstance(test_file, list)


def test_list_not_empty(test_file):
    assert len(test_file) > 0


def test_contains_dictionaries(test_file):
    for event in test_file:
        assert isinstance(event, dict)


def test_contains_correct_keys(test_file):
    expected = [
        "title",
        "description",
        "starts_at",
        "ends_at",
        "organiser_id",
        "venue_id"
    ]

    for event in test_file:
        assert all(key in event for key in expected)


def test_events_have_correct_data_types(test_file):
    for event in test_file:
        assert isinstance(event["title"], str)
        assert isinstance(event["starts_at"], str)
        assert isinstance(event["ends_at"], str)
        assert isinstance(event["organiser_id"], int)
        assert isinstance(event["venue_id"], int)


def test_events_have_no_empty_titles(test_file):
    for event in test_file:
        assert event["title"].strip() != ""


def test_events_have_positive_ids(test_file):
    for event in test_file:
        assert event["organiser_id"] > 0
        assert event["venue_id"] > 0


def test_events_inserted_correctly(test_file):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, description, starts_at, ends_at,
               organiser_id, venue_id
        FROM events
    """)

    result = cursor.fetchall()

    assert len(result) == len(test_file)

    conn.close()