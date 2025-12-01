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
        assert df1.count == df2.count, f"fCount mismatch: {count1} vs {count2}"

    @staticmethod
    #Check if the dfs have same data
    def check_data_full_data_set(df1, df2):
        df1 = df2

    @staticmethod
    #Check if the df has data
    def check_dataset_is_not_empty(df):
        df.is_not_empty

    @staticmethod
    #Check not null in the columns 
    def check_not_null_values(df, column_names=None):
        col for df.column_names:
            col.not_null
