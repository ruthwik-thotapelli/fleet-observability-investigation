-- Fleet Incident Investigation SQL Queries
-- Since the data is in CSV, these queries represent the logic we would run in a data warehouse (e.g., Snowflake/PostgreSQL) to find the same insights.

-- 1. What happened between 10:00 and 11:00?
-- Querying the events log timeline
SELECT 
    timestamp, 
    robot_id, 
    event_type, 
    details
FROM events_log
WHERE timestamp >= '10:00:00' AND timestamp <= '11:00:00'
ORDER BY timestamp ASC;

-- 2. Identify Robot_01's critical failure (Network Latency & Lock Timeout)
SELECT 
    t.timestamp,
    t.robot_id,
    t.network_latency_ms,
    e.event_type,
    e.details
FROM telemetry t
JOIN events_log e ON t.robot_id = e.robot_id
WHERE t.robot_id = 'Robot_01'
  AND t.network_latency_ms > 1000
ORDER BY t.timestamp;

-- 3. Find the missing trip end time (Robot_04)
SELECT 
    trip_id, 
    robot_id, 
    trip_start, 
    trip_status
FROM trips
WHERE trip_end IS NULL;

-- 4. Detect hardware sensor anomaly (Robot_04 Battery Jump)
SELECT 
    robot_id, 
    MIN(battery_level) as min_battery, 
    MAX(battery_level) as max_battery
FROM telemetry
WHERE robot_id = 'Robot_04'
GROUP BY robot_id
HAVING MAX(battery_level) > MIN(battery_level); -- Battery should only go down during trips
