import pytest
import pandas as pd


@pytest.mark.parquet_data  # Add this marker so it runs with your command
def test_postgres_connector_basic(db_connection):
    """Basic test to verify the Postgres connector works"""
    # Simple query to test the connection
    test_query = "SELECT 1 as test_value, 'hello' as test_string"
    result = db_connection.get_data_sql(test_query)

    # Verify it returns a DataFrame
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]['test_value'] == 1
    assert result.iloc[0]['test_string'] == 'hello'
    print("✓ Postgres connector works correctly!")