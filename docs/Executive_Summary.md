<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  body {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
    color: #1a1a2e;
    line-height: 1.6;
    margin: 0;
    padding: 0;
  }
  h1 {
    font-size: 22px;
    color: #0f3460;
    border-bottom: 3px solid #e94560;
    padding-bottom: 6px;
    margin-bottom: 4px;
  }
  h2 {
    font-size: 14px;
    color: #0f3460;
    border-left: 4px solid #e94560;
    padding-left: 8px;
    margin-top: 18px;
    margin-bottom: 6px;
  }
  h3 {
    font-size: 12px;
    color: #e94560;
    margin-bottom: 2px;
  }
  .header-meta {
    font-size: 11px;
    color: #666;
    margin-bottom: 14px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
    margin: 8px 0;
  }
  th {
    background-color: #0f3460;
    color: white;
    padding: 5px 8px;
    text-align: left;
  }
  td {
    padding: 4px 8px;
    border-bottom: 1px solid #dde;
  }
  tr:nth-child(even) td { background-color: #f4f6fb; }
  .critical-box {
    background: #fff0f3;
    border: 1px solid #e94560;
    border-left: 4px solid #e94560;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
  }
  .info-box {
    background: #f0f4ff;
    border: 1px solid #0f3460;
    border-left: 4px solid #0f3460;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
  }
  .warn-box {
    background: #fffbf0;
    border: 1px solid #f0a500;
    border-left: 4px solid #f0a500;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
  }
  .verdict {
    background: #0f3460;
    color: white;
    border-radius: 4px;
    padding: 10px 14px;
    margin: 10px 0;
    font-size: 12px;
  }
  ul, ol { margin: 4px 0; padding-left: 20px; }
  li { margin-bottom: 2px; }
  strong { color: #0f3460; }
  .label { display:inline-block; background:#e94560; color:white; border-radius:3px; padding:1px 6px; font-size:10px; font-weight:700; margin-right:4px; }
  .label-blue { background:#0f3460; }
  .label-green { background:#1a8c5c; }
  .label-orange { background:#d97706; }
  hr { border: none; border-top: 1px solid #dde; margin: 12px 0; }
</style>

# Fleet Observability & Incident Investigation
## Executive Summary Report

<div class="header-meta">
<strong>Author:</strong> Ruthwik Thotapelli &nbsp;|&nbsp; <strong>Role:</strong> Data Analytics & Observability Intern &nbsp;|&nbsp; <strong>Date:</strong> July 2026<br>
<strong>Fleet:</strong> Autonomous Mobile Robot (AMR) Operations &nbsp;|&nbsp; <strong>Incident Window:</strong> 10:00 AM – 11:00 AM, June 30, 2026
</div>

---

## 1. Project Objective

To conduct a rigorous, data-driven postmortem on a critical operational incident affecting a fleet of Autonomous Mobile Robots (AMRs). The goal was to move beyond assumptions and use raw telemetry, trip lifecycle records, and system event logs to **precisely reconstruct the sequence of failures**, identify all anomalies across the fleet, and **conclusively prove the root cause** of the mission-critical trip cancellation.

---

## 2. Approach

The investigation followed a strict Data Engineering lifecycle across four phases:

| Phase | Script | Description |
|-------|--------|-------------|
| **1. Data Profiling** | `preprocessing.py` | Assessed dataset health — checked missing values, timestamp integrity, and row uniqueness across all three data sources before any analysis. |
| **2. Exploratory Analysis** | `exploratory_analysis.py` | Visualized CPU, battery, and network latency distributions fleet-wide to isolate statistical outliers. |
| **3. Timeline Reconstruction** | `incident_timeline.py` | Fused three asynchronous data streams (telemetry, trips, events) into a single, second-level chronological timeline. |
| **4. Root Cause Extraction** | `root_cause_analysis.py` | Applied rule-based pattern matching on the timeline to link prior events to cancellation outcomes. |

---

## 3. Incident Timeline

The following is a minute-by-minute reconstruction of the incident window:

| Time | Robot | Event | Details |
|------|-------|-------|---------|
| 10:05:12 | Robot_01 | Trip T101 Started | Source → Destination |
| 10:05:14 | Robot_01 | Resource Lock Acquired | Zone_A secured ✅ |
| 10:05:55 | Robot_01 | ⚠️ Battery Low Warning | Pre-trip check missed |
| **10:06:10** | **Robot_01** | **🚨 Network Latency Spike** | **1450 ms sustained** |
| **10:06:18** | **Robot_01** | **🚨 Resource Lock Timeout** | **Zone_B — failed to acquire** |
| **10:06:20** | **Robot_01** | **❌ Trip T101 Cancelled** | **Safety timeout triggered** |
| 10:15:00 | Robot_02 | Trip T102 Started | Duplicate log entry observed |
| 10:17:40 | Robot_03 | Trip T204 Started | Zone_C lock acquired |
| 10:18:05 | Robot_03 | ⚠️ Position Jump Detected | Coordinates: X:999, Y:999 |
| 10:18:15 | Robot_03 | Trip T204 Completed | Recovered successfully ✅ |
| 10:21:30 | Robot_02 | ⚠️ CPU Saturation | 95% CPU load |
| 10:24:00 | Robot_02 | Trip T102 Completed | Resilient under compute load ✅ |
| 10:40:00 | Robot_04 | Trip T301 Started | Normal start |
| 10:44:00 | Robot_04 | ⚠️ Battery Level Jump | 32% → 41% (impossible mid-trip) |

<div class="critical-box">
<strong>🚨 Critical Cascade:</strong> The 1450ms network spike at 10:06:10 directly caused the Zone_B lock timeout 8 seconds later, which triggered the automatic safety mechanism cancelling Trip T101. The entire failure chain spanned only <strong>10 seconds</strong>.
</div>

---

## 4. Five Detected Anomalies

<br>

<span class="label">ANOMALY 1</span> **Network Latency Spike — Robot_01**

- **Observed:** Network latency of **1450 ms** at 10:06:10, confirmed in both event logs and telemetry.
- **Threshold:** Normal operations require < 200 ms for lock acquisition RPC calls.
- **Impact:** **Mission-critical.** Directly caused Trip T101 cancellation.

<span class="label">ANOMALY 2</span> **CPU Saturation — Robot_02**

- **Observed:** CPU utilization reached **95%** at 10:21:30, well above the 90% alert threshold.
- **Impact:** Non-critical. Robot_02 successfully completed Trip T102, demonstrating edge-software resilience under compute pressure.

<span class="label">ANOMALY 3</span> **SLAM Localization Glitch — Robot_03**

- **Observed:** Telemetry coordinates logged as **X: 999, Y: 999** at 10:18:05 — a sentinel value indicating an unhandled null or out-of-bounds SLAM output.
- **Impact:** Non-critical. The robot self-recovered within 10 seconds and completed Trip T204.

<span class="label">ANOMALY 4</span> **Impossible Battery Jump — Robot_04**

- **Observed:** Battery level rose from **32% → 41%** during an active running trip at 10:44:00. Confirmed by a `BatteryLevelJump` event log entry.
- **Impact:** Non-critical operationally, but **hardware-critical**. AMRs cannot charge while in motion. This isolates a defective Battery Management System (BMS) sensor.

<span class="label">ANOMALY 5</span> **Event Log Idempotency Bug — Robot_02**

- **Observed:** The `TripStarted` event for Trip T102 was logged **twice** at exactly 10:15:00.
- **Impact:** Non-critical operationally. However, this indicates a bug in the telemetry ingestion pipeline that could corrupt downstream analytics, aggregations, and billing counts.

---

## 5. Root Cause

<div class="verdict">
<strong>Root Cause:</strong> A severe network latency spike (1450ms) on Robot_01 prevented it from communicating with the resource management server within the required timeout window. The server, unable to receive lock acquisition confirmation for Zone_B, triggered an automatic safety timeout and cancelled Trip T101. <br><br>
<strong>Compute was stable (54% CPU). Battery was not the cause.</strong> The failure was purely a network-layer issue.
</div>

**Confirmed Evidence Chain:**
1. `NetworkLatencyHigh (1450ms)` logged at **10:06:10**
2. `ResourceLockTimeout (Zone_B)` logged **8 seconds later** at 10:06:18
3. `TripCancelled (T101)` logged **2 seconds later** at 10:06:20

---

## 6. Additional Observation — Hidden Safety Risk

<div class="warn-box">
<strong>⚠️ Critical Safety Design Flaw Identified</strong><br><br>
At 10:05:55, Robot_01 generated a <code>BatteryLowWarning</code> — and yet the system allowed the robot to continue its trip, acquire Zone_A, and attempt to acquire Zone_B.<br><br>
<strong>Why this is dangerous:</strong> In a warehouse environment, if a low-battery robot acquires a lock on a shared critical zone (e.g., a central intersection) and its battery dies mid-transit, it creates a <strong>physical blockade</strong>. Other robots cannot enter that zone until the lock is manually released and the robot is physically removed, potentially shutting down the entire fleet's throughput.<br><br>
<strong>Recommendation:</strong> Implement a <em>pre-trip battery gate</em> — any robot below a configurable threshold (e.g., 30%) should be barred from acquiring new zone locks and immediately routed to a charging dock.
</div>

---

## 7. Conclusion

This investigation conclusively identified a **network-induced resource lock timeout** as the sole cause of the mission-critical Trip T101 cancellation. The four secondary anomalies (CPU saturation, SLAM glitch, BMS sensor fault, and log duplication) were isolated to individual robots and did not affect fleet-wide operations — a testament to the robustness of the edge-deployed robot software.

**Key Takeaways:**

| Finding | Status | Action Required |
|---------|--------|-----------------|
| Robot_01 Trip Cancellation | Root cause proven | Network SLA audit + redundancy review |
| Robot_02 CPU Saturation | Edge software resilient | Monitor; set capacity alerts |
| Robot_03 SLAM Glitch | Self-recovered | Improve SLAM null handling |
| Robot_04 BMS Sensor Fault | Hardware defect | BMS replacement & calibration |
| Pipeline Idempotency Bug | Software defect | Fix ingestion deduplication logic |
| Low-battery lock acquisition | **Safety design risk** | **Implement pre-trip battery gate** |

The most urgent systemic risk is not the network incident itself, but the **absence of a battery-level pre-check** before zone lock acquisition — a policy gap that could cause a significantly more severe operational disruption in the future.

---

<div style="text-align:center; font-size:10px; color:#999; margin-top:16px;">
Fleet Observability & Incident Investigation · Data Analytics Internship Submission · July 2026
</div>
