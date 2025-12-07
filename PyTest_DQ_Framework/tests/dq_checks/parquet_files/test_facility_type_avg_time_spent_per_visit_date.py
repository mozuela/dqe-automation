"""
Description: Data Quality checks facility type average time per visit dataset
Requirement(s): TICKET-1234
Author(s): Julia Mendoza
"""

import pytest
import os

@pytest.fixture(scope='module')
def source_data(db_connection): #Get data from PostreSQL
    source_query = """
    SELECT 
        f.facility_type,
        DATE(v.visit_timestamp) as visit_date,
        AVG(v.duration_minutes) as avg_time_spent
    FROM src_generated_visits v
    JOIN src_generated_facilities f ON v.facility_id = f.facility_id
    WHERE f.facility_type IS NOT NULL 
      AND v.visit_timestamp IS NOT NULL
    GROUP BY f.facility_type, DATE(v.visit_timestamp)
    ORDER BY f.facility_type, DATE(v.visit_timestamp)
    """
    source_data = db_connection.get_data_sql(source_query)
    return source_data

@pytest.fixture(scope='module')
def target_data(parquet_reader): #Get data from parquet files
    target_path ='facility_type_avg_time_spent_per_visit_date'
    target_data = parquet_reader.process(target_path, include_subfolders=True)
    return target_data

#Smoke test
@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    """Smoke test: Ensure target data is not empty"""
    data_quality_library.check_dataset_is_not_empty(target_data)

#Data Completeness Tests
# Validate that all required data points are present in the target dataset and match the source dataset.
# Characteristics:Compare the source data (PostgreSQL) with the target data (Parquet files).
# Check for missing rows or columns.

@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_count(source_data, target_data, data_quality_library):
    """Compare record counts between source and target"""
    data_quality_library.check_count(source_data, target_data)

# Data Quality Tests
# Purpose: Validate the integrity, accuracy, and quality of the dataset.
# Characteristics:Check for duplicates, null values.

@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_duplicates(target_data, data_quality_library):
    """Check for duplicate records"""
    data_quality_library.check_duplicates(target_data, ['facility_type','visit_date'])

@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_not_null_values(target_data, data_quality_library):
    """Check for null values """
    data_quality_library.check_not_null_values(target_data, ['facility_type', 'visit_date'])

@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_avg_time_spent_range(target_data, data_quality_library):
    """Validate that average time spent """
    data_quality_library.check_value_range(target_data, 'avg_time_spent', 0, 1440)

@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_facility_type_values(target_data, data_quality_library):
    """Validate facility_type contains only expected values"""
    expected_facility_types = ['Hospital', 'Clinic', 'Urgent Care', 'Specialty Center']
    data_quality_library.check_allowed_values(target_data, 'facility_type', expected_facility_types)