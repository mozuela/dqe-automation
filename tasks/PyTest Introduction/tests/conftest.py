import pytest
import pandas as pd

# Fixture to read the CSV file
@pytest.fixture(scope="session")
def csv_data():
    """Fixture to read the CSV file once per session"""
    csv_path ="task/PyTest Introduction/src/data/data.csv"
    return pd.read_csv(csv_path)

# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def validate_schema(csv_data):
    """Fixture to validate the schema of the file"""
    expected_columns = ['id','name','age','email','is_active']
    actual_columns = csv_data.columns.tolist()
    assert actual_columns== expected_columns, f"Schema mistmatch: Expected: {expected_columns}, Actual columns: {actual_columns}"
    return csv_data

# A fixture to read the CSV file and return its content. Parameters: path_to_file.
@pytest.fixture(scope="session")
def csv_data_from_path():
    """Fixture to read CSV file with customizable path"""
    def _read_csv(path_to_file):
        if not os.path.exists(path_to_file):
            raise FileNotFoundError(f"CSV file not found: {path_to_file}")
        return pd.read_csv(path_to_file)
    return _read_csv

# A fixture to validate the schema of the file. Parameters: actual_schema, expected_schema.
@pytest.fixture(scope="session")
def schema_validator():
    """Fixture to validate schema with customizable expected schema"""
    def _validate_schema(actual_schema, expected_schema):
        assert actual_schema == expected_schema, (
            f"Schema validation failed. Expected: {expected_schema}, Got: {actual_schema}"
        )
        return True
    return _validate_schema

# Pytest hook to mark unmarked tests with a custom mark
def pytest_configure(config):
    """ Register custom markers in pytest """
    config.addinvalue_line("markers",
                           "unmarked: test that do not have a explicit marks (assigned automatically)"
                           )
    config.addinivalue_line("markers",
                            "csv_test: tests related to CSV file validation"
                            )
    config.addinivalue_line("markers",
                            "schema_test: tests for schema validation"
                            )
    config.addinivalue_line("markers",
                            "data_validation: tests for data content validation"
                            )

    #mark tests that do not have explicit marks. The hook should assign tests without marks to a custom mark:unmarked.
    def pytest_collection_modifyitems(config, items):
        """
        Hook to automatically assign 'unmarked' mark to tests without explicit marks
        """
        for item in items:
            # Check if the test has any markers
            if not any(item.iter_markers()):
                # Assign 'unmarked' mark if no marks
                item.add_marker(pytest.mark.unmarked)