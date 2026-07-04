<div align="center">
  <h1>🚀 Fleet Observability & Incident Investigation</h1>
  <p><strong>A Data-Driven Postmortem for Autonomous Mobile Robot (AMR) Operations</strong></p>

  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
  [![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458.svg)](https://pandas.pydata.org/)
  [![Jupyter](https://img.shields.io/badge/Jupyter-Interactive_Analysis-F37626.svg)](https://jupyter.org/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

---

## 📖 Overview

This repository contains an end-to-end data analytics and observability investigation into a critical incident involving a fleet of Autonomous Mobile Robots (AMRs) at Ati Motors. 

Between **10:00 AM and 11:00 AM**, the fleet experienced operational interruptions. Rather than relying on assumptions, this project leverages raw telemetry, trip lifecycle data, and system event logs to systematically reconstruct a minute-by-minute timeline, isolate anomalies, and prove the root cause.

## 🏗️ Project Architecture

```text
fleet-observability-investigation/
├── data/raw/             # Immutable raw data (events.log, telemetry.csv, trips.csv)
├── docs/                 # Incident summary reports and PDFs
├── notebooks/            # Executable Jupyter notebooks for presentation
├── outputs/              # Generated timeline CSVs and EDA figures
├── sql/                  # Equivalent Data Warehouse SQL queries
└── src/                  # Modular Python source code (ETL, Profiling, EDA)
```

## 🔍 Investigation Methodology

To ensure a highly defensible and accurate root-cause analysis, the investigation follows a strict Data Engineering lifecycle:

1. **Data Profiling (`src/preprocessing.py`)**: Assessed dataset health, missing values, timestamp consistency, and uniqueness before any analysis.
2. **Exploratory Data Analysis (`src/exploratory_analysis.py`)**: Visualized CPU, Battery, and Network latency distributions across the fleet to identify outliers.
3. **Timeline Reconstruction (`src/incident_timeline.py`)**: Merged asynchronous logs and telemetry streams into a single, chronologically sorted DataFrame to observe cascading failures.
4. **Root Cause Extraction (`notebooks/Fleet_Incident_Investigation.ipynb`)**: Mapped the primary failure point to a specific sub-system.

## 📊 Key Findings (The TL;DR)

* **Primary Failure (Robot_01):** Definitively identified as a **network-induced lock timeout**. A severe latency spike of `1450ms` prevented the robot from acquiring the `Zone_B` resource lock, triggering a safety timeout and trip cancellation. Compute and battery were confirmed stable at the time of failure.
* **Secondary Anomalies:** 
  * `Robot_02`: Experienced compute starvation (95% CPU) but successfully maintained navigation, indicating robust edge-software resilience.
  * `Robot_03`: Logged an out-of-bounds telemetry coordinate (`X:999, Y:999`) causing a temporary SLAM localization warning.
  * `Robot_04`: Recorded an impossible battery charge jump mid-trip, isolating a hardware defect in the Battery Management System (BMS).

## 🚀 Quick Start (Local Reproduction)

To replicate this investigation locally, ensure you have Python 3.9+ installed.

```bash
# 1. Clone the repository
git clone https://github.com/ruthwik-thotapelli/fleet-observability-investigation.git
cd fleet-observability-investigation

# 2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Reconstruct the timeline
python src/incident_timeline.py

# 5. Launch the interactive notebook
jupyter notebook notebooks/Fleet_Incident_Investigation.ipynb
```

## 💻 Data Warehouse / SQL

For deployment in an enterprise cloud environment (e.g., Snowflake, BigQuery), equivalent SQL logic is provided in `sql/analysis.sql`. These queries demonstrate how to extract the same latency spikes and hardware anomalies natively within a relational database.

---
*This project was completed as part of the Data Analytics & Observability Internship assignment.*
 
 
