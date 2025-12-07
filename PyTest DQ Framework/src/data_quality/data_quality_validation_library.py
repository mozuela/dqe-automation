import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    #Find duplicates
    def check_duplicates(df, column_names=None):
        if column_names:
            duplicates = df.duplicated(subset=column_names, keep=False) #Marks ALL duplicates as True
        else:
            duplicates = df.duplicated(keep=False)

        duplicates_count = duplicates.sum()
        assert duplicates_count == 0, f"Found {duplicates_count} duplicate records"

    @staticmethod
    #Compare row counts btw dataframes
    def check_count(df1, df2):
        count1 = len(df1)
        count2 = len(df2)
        assert count1 == count2, f"Count mismatch: {count1} vs {count2}"

    @staticmethod
    #Check if the dfs have same data
    def check_data_full_data_set(df1, df2):
        set1 = set(df1.itertuples(index=False, name=None))
        set2 = set(df2.itertuples(index=False, name=None))
        assert set1 == set2, f"Dataframe data does not match"

    @staticmethod
    #Check if the df has data
    def check_dataset_is_not_empty(df):
        assert len(df)>0, "Dataframe is empty"

    @staticmethod
    #Check not null in the columns
    def check_not_null_values(df, column_names=None):
        if column_names is None:
            column_names = df.columns.tolist()

        if not isinstance(column_names, list):
            raise TypeError(f"column_names must be a list, got {type(column_names)}")
        for column in column_names:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' not found in DataFrame")

            null_count = df[column].isnull().sum()
            assert null_count == 0, f"Column '{column}' has {null_count} null values"

    @staticmethod
    def check_value_range(df, column_name, min_value=None, max_value=None):
        # Check range in the columns
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame")

        # Check for values below minimum
        if min_value is not None:
            below_min = (df[column_name] < min_value).sum()
            assert below_min == 0, f"Column '{column_name}' has {below_min} values below minimum {min_value}"

        # Check for values above maximum
        if max_value is not None:
            above_max = (df[column_name] > max_value).sum()
            assert above_max == 0, f"Column '{column_name}' has {above_max} values above maximum {max_value}"

    @staticmethod
    #Check if values in a column are in the allowed list
    def check_allowed_values(df, column_name, allowed_values):
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame")

        if not isinstance(allowed_values, list):
            raise TypeError(f"allowed_values must be a list, got {type(allowed_values)}")

        # Check for values not in allowed list
        invalid_values = df[~df[column_name].isin(allowed_values)][column_name]
        invalid_count = len(invalid_values)

        if invalid_count > 0:
            # Get sample of invalid values for error message
            sample_invalid = invalid_values.head(5).tolist()
            error_msg = f"Column '{column_name}' has {invalid_count} invalid values"
            if invalid_count > 5:
                error_msg += f" (sample: {sample_invalid}...)"
            else:
                error_msg += f": {sample_invalid}"
            raise AssertionError(error_msg)