import pytest
from fastapi.testclient import TestClient



class Students:
    def __init__(self, first_name:str, last_name:str,major:str, years:int ):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def get_default_data():
    return Students("John", "Doe", "CSE", 5)


def test_check_student_data(get_default_data):
    assert get_default_data.first_name == "John"
    assert get_default_data.last_name  == "Doe"
    assert get_default_data.major == "CSE"
    assert get_default_data.years == 5
