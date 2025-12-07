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
        v.patient_id,
        f.facility_type,
        SUM(v.treatment_cost) as sum_treatment_cost
    FROM src_generated_visits v
    JOIN src_generated_facilities f ON v.facility_id = f.facility_id
    WHERE f.facility_type IS NOT NULL 
      AND v.treatment_cost IS NOT NULL
    GROUP BY v.patient_id, f.facility_type
    ORDER BY v.patient_id, f.facility_type
    """
    source_data = db_connection.get_data_sql(source_query)
    return source_data

@pytest.fixture(scope='module')
def target_data(parquet_reader): #Get data from parquet files
    target_path ='patient_sum_treatment_cost_per_facility_type'
    target_data = parquet_reader.process(target_path, include_subfolders=True)
    return target_data

#Smoke test
@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    """Smoke test: Ensure target data is not empty"""
    data_quality_library.check_dataset_is_not_empty(target_data)

#Data Completeness Tests
# Validate that all required data points are present in the target dataset and match the source dataset.
# Characteristics:Compare the source data (PostgreSQL) with the target data (Parquet files).
# Check for missing rows or columns.

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_count(source_data, target_data, data_quality_library):
    """Compare record counts between source and target"""
    data_quality_library.check_count(source_data, target_data)

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_column_structure(target_data):
    """Verify target has correct column structure"""
    expected_columns = ['facility_type', 'full_name', 'sum_treatment_cost']

# Data Quality Tests
# Purpose: Validate the integrity, accuracy, and quality of the dataset.
# Characteristics:Check for duplicates, null values.

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_duplicates(target_data, data_quality_library):
    """Check for duplicate records by patient and facility type"""
    data_quality_library.check_duplicates(target_data, ['full_name','facility_type'])

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_not_null_values(target_data, data_quality_library):
    """Check for null values """
    data_quality_library.check_not_null_values(target_data, ['full_name', 'facility_type', 'sum_treatment_cost'])

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_sum_treatment_cost_positive(target_data, data_quality_library):
    """Validate that total treatment cost is positive"""
    data_quality_library.check_value_range(target_data, 'sum_treatment_cost', 0, float('inf'))