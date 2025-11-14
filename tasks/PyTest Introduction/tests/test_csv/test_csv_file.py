import os.path
import pandas as pd
import re
import pytest


class TestCVSValidation:
    #Read the cvs file
    @pytest.fixture(scope="class")
    def get_csv_data(self):
        csv_file_path = os.path.join(os.path.dirname(__file__),'../../src/data/data.csv')
        return pd.read_csv(csv_file_path)

    #Test 1: validate that file is not empty
    @pytest.mark.csv_test
    @pytest.mark.data_validation
    def test_file_not_empty(self, get_csv_data):
        """Validate that file is not empty"""
        assert len(get_csv_data)>0, "CVS file should not be empty - Found empty file"

    #Test 2: Validate the schema of the file (id, name, age, email)
    @pytest.mark.schema_test
    def test_validate_schema(self, get_csv_data):
        """Validate the schema of the file (id, name, age, email)"""
        expected_columns = ['id','name','age','email','is_active']
        actual_columns = get_csv_data.columns.tolist()

        assert actual_columns == expected_columns, (
            f"CVS schema mismatch. Expected columns: {expected_columns},"
            f" found columns: {actual_columns}"
        )

    #Test 3: Validate that the age column contains valid values (0-100) - Use Custom and Predefined Marks (skip)
    @pytest.mark.skip(reason="Age validation TBD")
    @pytest.mark.data_validation
    def test_age_column_valid(self, get_csv_data):
        """Validate that the age column contains valid values """
        invalid_ages = get_csv_data[~get_csv_data['age'].between(0,100)]
        assert len(invalid_ages) == 0,(
            f"Invalid age values found. Age should be between 0 and 100"
            f"Row(s)s with invalid age:{invalid_ages[['id','age']].to_dict()}")

    #Test 4: Validate that the email column contains valid email addressess
    @pytest.mark.csv_test
    @pytest.mark.data_validation
    def test_email_column_valid(self, get_csv_data):
        """Validate that the email column contains valid email adresses format """
        email_pattern =  r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = get_csv_data[~get_csv_data['email'].str.match(email_pattern, na=False)]
        assert len(invalid_emails) == 0, (
            f"Invalid emails values found. Email should follow standard format"
            f"Row(s)s with invalid email:{invalid_emails[['id', 'email']].to_dict()}"
        )

    #Test 5: Validate there are not duplicates - Use Custom and Predefined Marks (xfail)
    @pytest.mark.xfail(reason="Duplicate rows expected in current test data ")
    @pytest.mark.data_validation
    def test_duplicates(self, get_csv_data):
        """Validate there are not duplicate rows"""
        duplicates = get_csv_data[get_csv_data.duplicated()]
        assert len(duplicates) == 0, (
            f"Duplicate rows found. Expected no duplicates, but found {len(duplicates)}"
        )

    #Test 6: Validate is active with parameter - Use Custom and Predefined Marks (parametrize)
    @pytest.mark.parametrize("id,expected_is_active", [
        (1, False),
        (2, True)
    ])
    @pytest.mark.csv_test
    def test_active_players(self, get_csv_data, id, expected_is_active):
        """Validate is_active = False for id = 1 and is_active = True for id= 2"""
        row = get_csv_data[get_csv_data['id']==id]
        assert len(row) == 1, f"Row with id {id} not found in CSV data"

        actual_is_active = row['is_active'].iloc[0]
        assert actual_is_active == expected_is_active, (
            f"is_active should be {expected_is_active} for id {id},"
            f" actual value found: {actual_is_active}"
        )

    #Test 7: Validate is active without parameter
    @pytest.mark.csv_test
    def test_active_player(self, get_csv_data):
        """Validate is_active = True for id =2 without parameter """
        row = get_csv_data[get_csv_data['id']==2]
        assert len(row) == 1, "ID 2 not found in CSV data"

        actual_is_active = row['is_active'].iloc[0]
        assert actual_is_active == True, (
            f"is_active should be True for ID 2, actual value found: {actual_is_active}"
        )