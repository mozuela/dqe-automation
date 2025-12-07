import pandas as pd
import os
import glob

class ParquetReader:
    """Provides functionality to read and process Parquet files"""

    def __init__(self,base_path="/parquet_data"): #Default is "/parquet_data
        self.base_path = base_path

    def process(self,relative_path, include_subfolders=False):
        #Read Parquet files and return dataframe
        full_path = os.path.join(self.base_path,relative_path)

        try:
            if include_subfolders: #recursive to check subfolders
                pattern = os.path.join(full_path,"**","*.parquet")
                parquet_files = glob.glob(pattern,recursive=True)
            else: #only specify directory
                pattern = os.path.join(full_path, "*.parquet")
                parquet_files = glob.glob(pattern)

            if not parquet_files:
                raise FileNotFoundError (f"No parquet files found at : {full_path}")
            print(f"Found {len(parquet_files)} parquet file(s) at: {full_path}")

            #Read and process all parquet files
            data_frames = []
            for file_path in parquet_files:
                try:
                    df = pd.read_parquet(file_path)
                    data_frames.append(df)
                    print(f"Successfully read: {os.path.basename(file_path)} - {len(df)} rows")
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

            if not data_frames:
                raise Exception(f"No data could be read from Parquet files at: {full_path}")

            if len(data_frames) == 1:
                combined_df = data_frames[0]
            else:
                combined_df = pd.concat(data_frames, ignore_index=True)

            print(f"Combined Dataframe shape: {combined_df.shape}")
            return combined_df

        except Exception as e:
            raise Exception(f"Failed to process parquet files from {full_path}: {e}")

    def read_single_file(self, file_path):
        try:
            df= pd.read_parquet(file_path)
            print(f"Read {len(df)} rows from: {file_path}")
            return df
        except Exception as e:
            raise Exception (f"Failed to read parquet file {file_path}: {e}")

    def get_available_datasets(self):
        try:
            if os.path.exists(self.base_path):
                items = os.listdir(self.base_path)
                datasets = [item for item in items
                            if os.path.isdir(os.path.join(self.base_path, item))]
                return datasets
            else:
                print(f"Base path does not exist: {self.base_path}")
                return []
        except Exception as e:
            print(f"Error listing datasets: {e}")
            return []
