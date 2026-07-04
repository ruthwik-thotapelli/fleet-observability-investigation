# Fleet Observability Incident Investigation

A professional data engineering and observability investigation into an Autonomous Mobile Robot (AMR) fleet incident.

## Overview
This repository contains a full root cause analysis based on raw telemetry, trip lifecycle data, and operational logs. Rather than relying on generic observations, this project systematically merges and queries raw CSV and Log files to construct a precise incident timeline and definitively prove the root cause.

## Repository Structure
- `data/raw/`: Raw datasets (`telemetry.csv`, `trips.csv`, `events.log`).
- `src/`: Python scripts for data loading, preprocessing, EDA, and timeline reconstruction.
- `sql/`: SQL logic for replicating the analysis in a data warehouse.
- `notebooks/`: Executable Jupyter Notebook demonstrating the evidence-backed investigation.
- `outputs/`: Generated artifacts (Timeline CSV, EDA charts, Final Summary PDF).
- `docs/`: Investigation summaries and presentation scripts.

## Key Findings
1. **Primary Incident (Robot_01):** Severe network latency (1450ms) caused a resource lock timeout, resulting in a cancelled trip.
2. **Compute Saturation (Robot_02):** Pinned 95% CPU, yet the navigation stack remained resilient enough to complete the trip.
3. **Localization Glitch (Robot_03):** An out-of-bounds telemetry coordinate jump (X:999, Y:999) caused a temporary SLAM warning, but the robot recovered.
4. **Sensor Fault (Robot_04):** Battery level inexplicably rose from 30% to 32% during a trip, strongly indicating a faulty battery sensor or BMS calibration error.

## Getting Started
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python src/incident_timeline.py
```
