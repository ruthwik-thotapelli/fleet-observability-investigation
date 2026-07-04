import pandas as pd

class RootCauseAnalyzer:
    def __init__(self, timeline_path: str):
        self.timeline = pd.read_csv(timeline_path)
        
    def analyze_trip_failures(self):
        """
        Analyzes the timeline to find the root cause of cancelled trips.
        """
        cancelled_events = self.timeline[self.timeline['event_type'] == 'TripCancelled']
        report = []
        
        for _, cancel_event in cancelled_events.iterrows():
            robot = cancel_event['robot_id']
            time = cancel_event['time_only']
            
            # Look at events leading up to the cancellation (window of 60 seconds)
            # Simplification: just get the 5 events immediately prior for that robot
            robot_history = self.timeline[self.timeline['robot_id'] == robot]
            prior_events = robot_history[robot_history['time_only'] <= time].tail(5)
            
            # Check for critical network or lock issues
            has_latency = prior_events['event_type'].str.contains('NetworkLatency').any()
            has_lock_timeout = prior_events['event_type'].str.contains('ResourceLockTimeout').any()
            
            conclusion = "Unknown"
            if has_latency and has_lock_timeout:
                conclusion = "Network-induced Resource Lock Timeout. High latency prevented lock acquisition."
                
            report.append({
                'robot_id': robot,
                'failure_time': time,
                'root_cause': conclusion,
                'evidence': prior_events[['time_only', 'event_type', 'details']].to_dict('records')
            })
            
        return report

if __name__ == '__main__':
    analyzer = RootCauseAnalyzer('../outputs/timeline.csv')
    results = analyzer.analyze_trip_failures()
    for r in results:
        print(f"Robot: {r['robot_id']}")
        print(f"Root Cause: {r['root_cause']}")
