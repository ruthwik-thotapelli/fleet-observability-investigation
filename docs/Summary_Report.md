# Fleet Incident Investigation Summary

**Date:** July 2026  
**Role:** Data Analytics & Observability Intern

## 1. The Incident (10:00 AM - 11:00 AM)
During the specified window, the fleet experienced a critical trip failure, a compute saturation event, a localization warning, and a sensor anomaly. By fusing telemetry data, trip records, and system events, we reconstructed a precise timeline to identify the root causes.

## 2. Most Critical Issue: Robot_01 Network Failure
Robot_01 suffered the only mission-critical failure, resulting in a cancelled trip (`T101`). 
- **Evidence:** Event logs show a `NetworkLatencyHigh` warning of 1450ms at 10:06:10. Telemetry data at 10:10:00 confirms the 1450ms sustained latency. Immediately following the latency spike (10:06:18), a `ResourceLockTimeout` occurred for `Zone_B`.
- **Root Cause:** The 1.4-second network lag prevented Robot_01 from communicating with the server to acquire its next zone lock. This triggered an automatic safety timeout, cancelling the trip. This was primarily a **network condition**, not a compute or robot-behavior issue.

## 3. Detected Anomalies
1. **Robot_02 (Compute Saturation):** CPU hit 95% at 10:21:30. *Impact:* Despite the load, the robot successfully completed trip `T102`, demonstrating software resilience.
2. **Robot_03 (Localization Glitch):** At 10:18:00, telemetry recorded coordinates `X: 999, Y: 999`, triggering a `PositionJumpDetected` log. *Impact:* The robot recovered and finished trip `T204` 10 seconds later.
3. **Robot_04 (Hardware Sensor Error):** Battery telemetry climbed from 30% to 32%, accompanied by a `BatteryLevelJump` log. *Impact:* Since AMRs cannot charge while moving, this strongly suggests a faulty Battery Management System (BMS) sensor.
4. **Event Pipeline Idempotency:** Duplicate `TripStarted` logs for Robot_02 suggest a minor bug in the telemetry ingestion pipeline.

## 4. Hidden Observation (Beyond the Assignment)
**Observation:** The system allows a robot with a `BatteryLowWarning` (Robot_01) to begin a trip and acquire resource locks. 
**Why it matters:** In a warehouse environment, allowing low-battery robots to acquire locks on shared zones is dangerous. If the battery dies while occupying a critical intersection (`Zone_A`), it creates a physical blockade, shutting down the entire fleet's throughput. 

## 5. Assumptions
- Telemetry timestamps (e.g., `2026-06-30T10:04:00`) correspond directly to the event log timestamps (e.g., `10:05:12`) on the same day.
- A coordinate of `999, 999` represents an unhandled null or out-of-bounds error rather than a physical location.
- No physical battery hot-swaps occurred while Robot_04 was in the `running` state.
 
 
