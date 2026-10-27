import pytest
from db.seed import read_file
from db.connection import get_connection


@pytest.fixture
def test_file():
    return read_file("venues")


def test_extract_list(test_file):
    assert isinstance(test_file, list)


def test_list_not_empty(test_file):
    assert len(test_file) > 0


def test_contains_dictionaries(test_file):
    for venue in test_file:
        assert isinstance(venue, dict)


def test_contains_correct_keys(test_file):
    expected = ["name", "address", "capacity"]

    for venue in test_file:
        assert all(key in venue for key in expected)


def test_venues_have_correct_data_types(test_file):
    for venue in test_file:
        assert isinstance(venue["name"], str)
        assert isinstance(venue["address"], (str, type(None)))
        assert isinstance(venue["capacity"], int)


def test_venues_have_no_empty_names(test_file):
    for venue in test_file:
        assert venue["name"].strip() != ""


def test_venues_have_positive_capacity(test_file):
    for venue in test_file:
        assert venue["capacity"] > 0


def test_venues_inserted_correctly(test_file):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT name, address, capacity
            FROM venues
            ORDER BY id
        """)

        result = cursor.fetchall()

        expected = [
            (venue["name"], venue["address"], venue["capacity"])
            for venue in test_file
        ]

        assert result == expected

    finally:
        cursor.close()
        conn.close()



