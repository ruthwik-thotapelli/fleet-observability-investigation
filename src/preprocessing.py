import pandas as pd
import numpy as np

def profile_dataframe(df: pd.DataFrame, name: str) -> dict:
    """Provides a data quality profile for a given dataframe."""
    profile = {
        'name': name,
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum()
    }
    return profile

def check_invalid_timestamps(df: pd.DataFrame, time_col: str) -> int:
    """Check for timestamps that cannot be parsed."""
    invalid_count = 0
    for val in df[time_col]:
        try:
            pd.to_datetime(val)
        except:
            invalid_count += 1
    return invalid_count

def run_profiling(telemetry: pd.DataFrame, trips: pd.DataFrame, events: pd.DataFrame) -> None:
    print("=== Data Profiling Report ===")
    
    # 1. Telemetry Profile
    t_prof = profile_dataframe(telemetry, 'Telemetry')
    print(f"Dataset: {t_prof['name']}")
    print(f" - Shape: {t_prof['rows']} rows, {t_prof['columns']} columns")
    print(f" - Missing Values: {t_prof['missing_values']}")
    print(f" - Duplicates: {t_prof['duplicates']}")
    print(f" - Unique Robots: {telemetry['robot_id'].nunique()}")
    print(f" - Unique Trips in Telemetry: {telemetry['trip_id'].nunique()}")
    
    # 2. Trips Profile
    tr_prof = profile_dataframe(trips, 'Trips')
    print(f"\nDataset: {tr_prof['name']}")
    print(f" - Shape: {tr_prof['rows']} rows, {tr_prof['columns']} columns")
    print(f" - Missing Values: {tr_prof['missing_values']}")
    print(f" - Duplicates: {tr_prof['duplicates']}")
    print(f" - Trip Status Breakdown:\n{trips['trip_status'].value_counts().to_string()}")
    
    # 3. Events Profile
    e_prof = profile_dataframe(events, 'Events')
    print(f"\nDataset: {e_prof['name']}")
    print(f" - Shape: {e_prof['rows']} rows, {e_prof['columns']} columns")
    print(f" - Missing Values: {e_prof['missing_values']}")
    print(f" - Duplicates: {e_prof['duplicates']}")
    
    # Invalid timestamps check
    # Need to check format, assuming '10:00' format is parsable by pandas or needs prefix
    # We will just see if we can convert them
    print("\n=== Data Quality Score ===")
    total_records = t_prof['rows'] + tr_prof['rows'] + e_prof['rows']
    total_issues = t_prof['missing_values'] + t_prof['duplicates'] + \
                   tr_prof['missing_values'] + tr_prof['duplicates'] + \
                   e_prof['missing_values'] + e_prof['duplicates']
    score = max(0, 100 - (total_issues / total_records * 100))
    print(f"Estimated Quality Score: {score:.2f}/100")
 
