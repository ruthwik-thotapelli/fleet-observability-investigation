import pandas as pd

def detect_anomalies(telemetry: pd.DataFrame, events: pd.DataFrame) -> dict:
    """
    Scans telemetry and events for operational anomalies using rule-based and threshold logic.
    """
    anomalies = {
        'network_latency': [],
        'cpu_saturation': [],
        'battery_jumps': [],
        'localization_errors': []
    }
    
    # 1. Network Latency Spikes (> 1000ms)
    high_latency = telemetry[telemetry['network_latency_ms'] > 1000]
    if not high_latency.empty:
        anomalies['network_latency'] = high_latency[['timestamp', 'robot_id', 'network_latency_ms']].to_dict('records')
        
    # 2. CPU Saturation (> 90%)
    high_cpu = telemetry[telemetry['cpu_usage'] > 90]
    if not high_cpu.empty:
        anomalies['cpu_saturation'] = high_cpu[['timestamp', 'robot_id', 'cpu_usage']].to_dict('records')
        
    # 3. Impossible Battery Jumps (Battery level increases without charging state)
    # Using the events log for the hardware sensor error
    battery_jumps = events[events['event_type'] == 'BatteryLevelJump']
    if not battery_jumps.empty:
        anomalies['battery_jumps'] = battery_jumps[['timestamp', 'robot_id', 'details']].to_dict('records')
        
    # 4. Localization / SLAM Glitches (Coordinates = 999)
    glitches = telemetry[(telemetry['position_x'] > 900) | (telemetry['position_y'] > 900)]
    if not glitches.empty:
        anomalies['localization_errors'] = glitches[['timestamp', 'robot_id', 'position_x', 'position_y']].to_dict('records')
        
    return anomalies

if __name__ == '__main__':
    from data_loader import DataLoader
    dl = DataLoader('../data')
    t, tr, e = dl.load_all()
    detected = detect_anomalies(t, e)
    for category, items in detected.items():
        print(f"--- {category.upper()} ---")
        for item in items:
            print(item)
