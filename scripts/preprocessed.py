import pandas as pd
def preprocess_data(df, save_pickle=False, pickle_path=None):
    """
    Preprocess the data by handling missing values and encoding categorical features.

    Parameters:
    - df: DataFrame containing the raw data
    - save_csv: Whether to save the preprocessed data to a CSV file
    - csv_path: Path to save the CSV file if save_csv is True
    """

    # Remove the last row from the dataset since it contains a NaN value in the target column
    df_processed = df.iloc[:-1, :]

    # Change time from an object to a datetime
    df_processed["time"] = pd.to_datetime(df_processed["time"])

    # Convert weather_code to categorical    
    df_processed["weather_code"] = df_processed["weather_code"].astype("category")

    if save_pickle:
        df_processed.to_pickle(pickle_path)
        print("Preprocessed data file saved to:", pickle_path)

    return df_processed


