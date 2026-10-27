import pytest
from db.seed import read_file
from db.connection import get_connection


@pytest.fixture
def test_file():
    return read_file("rsvps")


def test_extract_list(test_file):
    assert isinstance(test_file, list)


def test_list_not_empty(test_file):
    assert len(test_file) > 0


def test_contains_dictionaries(test_file):
    for rsvp in test_file:
        assert isinstance(rsvp, dict)


def test_contains_correct_keys(test_file):
    expected = ["attendee_id", "event_id"]

    for rsvp in test_file:
        assert all(key in rsvp for key in expected)


def test_rsvps_have_correct_data_types(test_file):
    for rsvp in test_file:
        assert isinstance(rsvp["attendee_id"], int)
        assert isinstance(rsvp["event_id"], int)


def test_rsvps_have_positive_ids(test_file):
    for rsvp in test_file:
        assert rsvp["attendee_id"] > 0
        assert rsvp["event_id"] > 0


def test_rsvps_inserted_correctly(test_file):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT attendee_id, event_id
            FROM rsvps
            ORDER BY id
        """)

        result = cursor.fetchall()

        expected = [
            (rsvp["attendee_id"], rsvp["event_id"])
            for rsvp in test_file
        ]

        assert result == expected

    finally:
        cursor.close()
        conn.close()


def test_rsvps_have_created_at():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT created_at FROM rsvps")

        result = cursor.fetchall()

        for row in result:
            assert row[0] is not None

    finally:
        cursor.close()
        conn.close()