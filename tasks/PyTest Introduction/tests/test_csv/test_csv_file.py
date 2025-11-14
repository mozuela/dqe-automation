import os.path
import pandas as pd
import re
import pytest


class TestCVSValidation:
    #Read the cvs file
    @pytest.fixture(scope="class")
    def get_cvs_data(self):
        cvs_file_path = os.path.join(os.path.dirname(__file__),'tasks/PyTest Introduction/src/data/data.csv')
        return pd.read_csv(cvs_file_path)

    #Test 1: validate that file is not empty
def test_file_not_empty(self, cvs_data):
    """Validate that file is not empty"""
    assert len(cvs_data)>0, "CVS file should not be empty - Found empty file"

    #Test 2: Validate the schema of the file (id, name, age, email)
def test_validate_schema(self, cvs_data):
    """Validate the schema of the file (id, name, age, email)"""
    expected_columns = ['id','name','age','email','is_active']
    actual_columns = cvs_data.columns.tolist()

    assert actual_columns == expected_columns, (
        f"CVS schema mismatch. Expected columns: {expected_columns},"
        f" found columns: {actual_columns}"
    )

    #Test 3: Validate that the age column contains valid values (0-100) - Use Custom and Predefined Marks (skip)
    @pytest.mark.skip(reason="Age validation TBD")
def test_age_column_valid(self, cvs_data):
    """Validate that the age column contains valid values """
    invalid_ages = cvs_data[~cvs_data['age'].between(0,100)]
    assert len(invalid_ages) == 0,(
        f"Invalid age values found. Age should be between 0 and 100"
        f"Row(s)s with invalid age:{invalid_ages[['id','age']].to_dict()}")

    #Test 4: Validate that the email column contains valid email addressess
def test_email_column_valid(self,cvs_data):
    """Validate that the email column contains valid email adresses format """
    email_pattern =  r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    invalid_emails = cvs_data[~cvs_data['email'].str.match(email_pattern, na=False)]
    assert len(invalid_emails) == 0, (
        f"Invalid emails values found. Email should follow standard format"
        f"Row(s)s with invalid email:{invalid_emails[['id', 'email']].to_dict()}"
    )


def test_active_players():
    assert 1 + 1 == 2


def test_active_player():
    assert 1 + 1 == 2

def test_duplicates():
    assert 1 + 1 == 2


