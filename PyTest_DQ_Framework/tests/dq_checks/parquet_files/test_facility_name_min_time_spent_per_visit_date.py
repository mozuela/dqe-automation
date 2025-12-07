"""
Description: Data Quality checks for Min time spent per visit dataset
Requirement(s): TICKET-1234
Author(s): Julia Mendoza
"""

import pytest

@pytest.fixture(scope='module')
def source_data(db_connection): #Get data from PostreSQL
    source_query = """
    SELECT 
        f.facility_name,
        DATE(v.visit_timestamp) as visit_date,
        MIN(v.duration_minutes) as min_time_spent
    FROM src_generated_visits v
    JOIN src_generated_facilities f ON v.facility_id = f.facility_id
    WHERE f.facility_name IS NOT NULL 
      AND v.visit_timestamp IS NOT NULL
    GROUP BY f.facility_name, DATE(v.visit_timestamp)
    ORDER BY f.facility_name, DATE(v.visit_timestamp)
    """
    source_data = db_connection.get_data_sql(source_query)
    return source_data

@pytest.fixture(scope='module')
def target_data(parquet_reader): #Get data from parquet files
    target_path ='facility_name_min_time_spent_per_visit_date'
    target_data = parquet_reader.process(target_path, include_subfolders=True)
    return target_data

#Smoke test
@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    """Smoke test: Ensure target data is not empty"""
    data_quality_library.check_dataset_is_not_empty(target_data)

#Data Completeness Tests
# Validate that all required data points are present in the target dataset and match the source dataset.
# Characteristics:Compare the source data (PostgreSQL) with the target data (Parquet files).
# Check for missing rows or columns.

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_count(source_data, target_data, data_quality_library):
    """Compare record counts between source and target"""
    data_quality_library.check_count(source_data, target_data)

# Data Quality Tests
# Purpose: Validate the integrity, accuracy, and quality of the dataset.
# Characteristics:Check for duplicates, null values.

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_duplicates(target_data, data_quality_library):
    """Check for duplicate records"""
    data_quality_library.check_duplicates(target_data, ['facility_name','visit_date'])

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_check_not_null_values(target_data, data_quality_library):
    """Check for null values """
    data_quality_library.check_not_null_values(target_data, ['facility_name', 'visit_date', 'min_time_spent'])

