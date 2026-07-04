import pandas as pd
import os
import sys

def build_timeline():
    dl = __import__('data_loader').DataLoader('data')
    telemetry, trips, events = dl.load_all()

    # Normalize events timestamp (add artificial date to match telemetry if needed, but let's just use time)
    events['time_only'] = events['timestamp']
    events['source'] = 'Event Log'
    
    # Process trips
    trips_start = trips[['trip_start', 'robot_id', 'trip_id', 'source', 'destination', 'trip_status']].copy()
    trips_start.rename(columns={'trip_start': 'time_only'}, inplace=True)
    trips_start['event_type'] = 'Trip Started (' + trips_start['trip_id'] + ')'
    trips_start['source'] = 'Trips Data'
    
    trips_end = trips[['trip_end', 'robot_id', 'trip_id', 'source', 'destination', 'trip_status']].copy()
    trips_end = trips_end.dropna(subset=['trip_end'])
    trips_end.rename(columns={'trip_end': 'time_only'}, inplace=True)
    trips_end['event_type'] = 'Trip Ended (' + trips_end['trip_id'] + ') - ' + trips_end['trip_status']
    trips_end['source'] = 'Trips Data'
    
    # We will mainly use events.log for the detailed timeline since it has second-level precision.
    timeline = events[['time_only', 'robot_id', 'event_type', 'details', 'source']].copy()
    
    # Merge telemetry anomalies for the timeline
    telemetry['time_only'] = telemetry['timestamp'].astype(str).str[-8:] # extract HH:MM:SS
    # filter for anomalies to add to timeline
    t_anom = telemetry[(telemetry['network_latency_ms'] > 1000) | (telemetry['cpu_usage'] >= 90) | (telemetry['battery_level'] < 30)]
    t_events = []
    for _, row in t_anom.iterrows():
        t_events.append({
            'time_only': row['time_only'],
            'robot_id': row['robot_id'],
            'event_type': 'Telemetry Anomaly',
            'details': f"Batt:{row['battery_level']}% CPU:{row['cpu_usage']}% Lat:{row['network_latency_ms']}ms",
            'source': 'Telemetry Data'
        })
    
    timeline = pd.concat([timeline, pd.DataFrame(t_events)], ignore_index=True)
    timeline.sort_values(by='time_only', inplace=True)
    
    os.makedirs('outputs', exist_ok=True)
    timeline.to_csv('outputs/timeline.csv', index=False)
    print("Timeline saved to outputs/timeline.csv")
    print("\n--- INCIDENT TIMELINE ---")
    print(timeline.to_string())

if __name__ == '__main__':
    sys.path.append('src')
    build_timeline()
 
 
