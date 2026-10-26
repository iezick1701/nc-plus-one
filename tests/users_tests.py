from db.seed import read_file
import pytest


@pytest.fixture
def test_file():
    return read_file('users')

def test_extract_list(test_file):
    #arrange 
    expected = list


    #act
    check =test_file
    file_type = type(check)


    #assert 
    assert file_type == expected 


def test_list_not_empty(test_file):
    expected = True 
    length = len(test_file)
    test = length>0
    assert test == expected


def test_contains_dictionaries(test_file):
       expected = dict
       output = test_file[0]
       final = type(output)
       assert final == expected


def test_contains_correct_keys(test_file):
     expected = True
     check_list = ["name","email","password"]
     for user in test_file:
               result = all([key in user for key in check_list])
     assert result == expected
     
     
      




