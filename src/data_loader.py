import pandas as pd
import os
import re
from typing import Dict, Tuple

class DataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.telemetry_path = os.path.join(data_dir, 'raw', 'telemetry.csv')
        self.trips_path = os.path.join(data_dir, 'raw', 'trips.csv')
        self.events_path = os.path.join(data_dir, 'raw', 'events.log')

    def load_telemetry(self) -> pd.DataFrame:
        df = pd.read_csv(self.telemetry_path)
        # Convert timestamp assuming format is HH:MM or HH:MM:SS
        # Will handle specific formatting in preprocessing
        return df

    def load_trips(self) -> pd.DataFrame:
        df = pd.read_csv(self.trips_path)
        return df

    def load_events(self) -> pd.DataFrame:
        events = []
        with open(self.events_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Expected format: 10:05:12 Robot_01 EventType [Optional Data]
                parts = line.split(' ', 3)
                timestamp = parts[0]
                robot_id = parts[1] if len(parts) > 1 else None
                event_type = parts[2] if len(parts) > 2 else None
                details = parts[3] if len(parts) > 3 else None
                events.append({
                    'timestamp': timestamp,
                    'robot_id': robot_id,
                    'event_type': event_type,
                    'details': details
                })
        return pd.DataFrame(events)

    def load_all(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        return self.load_telemetry(), self.load_trips(), self.load_events()
