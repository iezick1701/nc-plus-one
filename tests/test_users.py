import pytest
from db.seed import read_file
from db.connection import get_connection
from db.password import check_pwd


@pytest.fixture
def test_file():
    return read_file("users")


def test_extract_list(test_file):
    assert isinstance(test_file, list)


def test_list_not_empty(test_file):
    assert len(test_file) > 0


def test_contains_dictionaries(test_file):
    for user in test_file:
        assert isinstance(user, dict)


def test_contains_correct_keys(test_file):
    expected = ["email", "password", "name"]

    for user in test_file:
        assert all(key in user for key in expected)


def test_users_have_correct_data_types(test_file):
    for user in test_file:
        assert isinstance(user["email"], str)
        assert isinstance(user["password"], str)
        assert isinstance(user["name"], str)


def test_users_have_no_empty_fields(test_file):
    for user in test_file:
        assert user["email"].strip() != ""
        assert user["password"].strip() != ""
        assert user["name"].strip() != ""


def test_users_have_unique_emails(test_file):
    emails = [user["email"] for user in test_file]

    assert len(emails) == len(set(emails))


def test_users_inserted_correctly(test_file):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT   email, password, name
            FROM users
            ORDER BY id
        """)

        result = cursor.fetchall()

        db_users = {
            row[0]: row
            for row in result
        }

        assert len(result) == len(test_file)

        for user in test_file:
            db_user = db_users[user["email"]]

            assert db_user[0] == user["email"]
            assert db_user[2] == user["name"]
            assert check_pwd(user["password"], db_user[1])

    finally:
        cursor.close()
        conn.close()


def test_users_have_created_at():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT created_at FROM users")

        result = cursor.fetchall()

        for row in result:
            assert row[0] is not None

    finally:
        cursor.close()
        conn.close()
     
      




