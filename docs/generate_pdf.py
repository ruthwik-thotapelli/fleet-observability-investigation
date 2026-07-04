import subprocess, sys

# Install reportlab if not available
subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "-q"])

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import PageBreak

OUTPUT = "docs/Executive_Summary.pdf"

# ── Color palette ──────────────────────────────────────────────────
NAVY   = colors.HexColor("#0f3460")
RED    = colors.HexColor("#e94560")
LGRAY  = colors.HexColor("#f4f6fb")
MGRAY  = colors.HexColor("#dde0ee")
YELLOW = colors.HexColor("#fffbf0")
YLBDR  = colors.HexColor("#f0a500")
PINK   = colors.HexColor("#fff0f3")
BLUE   = colors.HexColor("#f0f4ff")
WHITE  = colors.white
BLACK  = colors.HexColor("#1a1a2e")

W, H = A4

# ── Document ───────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

# ── Styles ─────────────────────────────────────────────────────────
def S(name, **kw):
    base = getSampleStyleSheet()["Normal"]
    return ParagraphStyle(name, parent=base, **kw)

title_style   = S("Title",   fontSize=20, textColor=NAVY,  fontName="Helvetica-Bold", spaceAfter=2)
sub_style     = S("Sub",     fontSize=9,  textColor=colors.HexColor("#666666"), spaceAfter=10)
h2_style      = S("H2",      fontSize=12, textColor=NAVY,  fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
body_style    = S("Body",    fontSize=9,  textColor=BLACK, leading=14, alignment=TA_JUSTIFY)
bullet_style  = S("Bullet",  fontSize=9,  textColor=BLACK, leading=13, leftIndent=14, bulletIndent=0)
label_style   = S("Label",   fontSize=8,  textColor=WHITE, fontName="Helvetica-Bold")
small_style   = S("Small",   fontSize=8,  textColor=colors.HexColor("#999999"), alignment=TA_CENTER)
verdict_style = S("Verdict", fontSize=9,  textColor=WHITE, leading=14, fontName="Helvetica-Bold")
warn_style    = S("Warn",    fontSize=9,  textColor=BLACK, leading=13)
bold9         = S("Bold9",   fontSize=9,  textColor=NAVY,  fontName="Helvetica-Bold")

def hr(): return HRFlowable(width="100%", thickness=0.5, color=MGRAY, spaceAfter=6, spaceBefore=2)
def sp(h=4): return Spacer(1, h)

def section_title(text):
    return [Paragraph(text, h2_style), HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=6)]

def colored_box(text, bg, border):
    t = Table([[Paragraph(text, warn_style)]], colWidths=[doc.width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), bg),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LINECOLOR",    (0,0),(-1,-1), border),
        ("BOX",          (0,0),(-1,-1), 1, border),
        ("LINEBEFORE",   (0,0),(0,-1),  3, border),
        ("ROUNDEDCORNERS",[3]),
    ]))
    return t

def make_table(headers, rows, col_widths=None):
    data = [[Paragraph(f"<b>{h}</b>", S("th", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold"))
             for h in headers]] + \
           [[Paragraph(str(c), S("td", fontSize=8, textColor=BLACK, leading=12)) for c in row]
            for row in rows]
    if col_widths is None:
        col_widths = [doc.width / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  NAVY),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, LGRAY]),
        ("LINEBELOW",      (0,0),(-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    t.setStyle(TableStyle(style))
    return t

def verdict_box(text):
    t = Table([[Paragraph(text, verdict_style)]], colWidths=[doc.width])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("ROUNDEDCORNERS",[4]),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════
# BUILD CONTENT
# ══════════════════════════════════════════════════════════════════
story = []

# ── HEADER ────────────────────────────────────────────────────────
story.append(Paragraph("Fleet Observability &amp; Incident Investigation", title_style))
story.append(HRFlowable(width="100%", thickness=3, color=RED, spaceAfter=4))
story.append(Paragraph(
    "<b>Executive Summary Report</b> &nbsp;|&nbsp; "
    "Author: Ruthwik Thotapelli &nbsp;|&nbsp; "
    "Role: Data Analytics &amp; Observability Intern &nbsp;|&nbsp; July 2026<br/>"
    "Fleet: Autonomous Mobile Robot (AMR) Operations &nbsp;|&nbsp; "
    "Incident Window: <b>10:00 AM – 11:00 AM, June 30, 2026</b>",
    sub_style
))

# ── 1. OBJECTIVE ─────────────────────────────────────────────────
story += section_title("1. Project Objective")
story.append(Paragraph(
    "To conduct a rigorous, data-driven postmortem on a critical operational incident affecting a "
    "fleet of Autonomous Mobile Robots (AMRs). The goal was to move beyond assumptions and use "
    "<b>raw telemetry, trip lifecycle records, and system event logs</b> to precisely reconstruct "
    "the failure sequence, identify all anomalies across the fleet, and conclusively prove the "
    "root cause of the mission-critical trip cancellation.",
    body_style
))
story.append(sp(8))

# ── 2. APPROACH ───────────────────────────────────────────────────
story += section_title("2. Approach")
story.append(make_table(
    ["Phase", "Script", "Description"],
    [
        ["1. Data Profiling",     "preprocessing.py",        "Assessed dataset health — checked missing values, timestamp integrity, and row uniqueness across all three data sources before any analysis."],
        ["2. Exploratory Analysis","exploratory_analysis.py", "Visualized CPU, battery, and network latency distributions fleet-wide to isolate statistical outliers."],
        ["3. Timeline Reconstruction","incident_timeline.py","Fused three asynchronous data streams (telemetry, trips, events) into a single, second-level chronological timeline."],
        ["4. Root Cause Extraction","root_cause_analysis.py","Applied rule-based pattern matching on the fused timeline to link prior events to trip cancellation outcomes."],
    ],
    col_widths=[3.5*cm, 4.5*cm, 9.5*cm]
))
story.append(sp(8))

# ── 3. TIMELINE ───────────────────────────────────────────────────
story += section_title("3. Incident Timeline (10:00 AM – 11:00 AM)")
story.append(make_table(
    ["Time", "Robot", "Event", "Details"],
    [
        ["10:05:12", "Robot_01", "Trip T101 Started",            "Source → Destination"],
        ["10:05:14", "Robot_01", "Resource Lock Acquired",       "Zone_A secured ✓"],
        ["10:05:55", "Robot_01", "⚠ Battery Low Warning",        "Pre-trip check missed"],
        ["10:06:10", "Robot_01", "🚨 Network Latency Spike",     "1450 ms sustained"],
        ["10:06:18", "Robot_01", "🚨 Resource Lock Timeout",     "Zone_B — failed to acquire"],
        ["10:06:20", "Robot_01", "❌ Trip T101 CANCELLED",       "Safety timeout triggered"],
        ["10:15:00", "Robot_02", "Trip T102 Started",            "Duplicate log entry observed"],
        ["10:17:40", "Robot_03", "Trip T204 Started",            "Zone_C lock acquired"],
        ["10:18:05", "Robot_03", "⚠ Position Jump Detected",    "Coords: X:999, Y:999"],
        ["10:18:15", "Robot_03", "Trip T204 Completed",          "Self-recovered ✓"],
        ["10:21:30", "Robot_02", "⚠ CPU Saturation",            "95% CPU load"],
        ["10:24:00", "Robot_02", "Trip T102 Completed",          "Resilient under compute load ✓"],
        ["10:40:00", "Robot_04", "Trip T301 Started",            "Normal start"],
        ["10:44:00", "Robot_04", "⚠ Battery Level Jump",        "32% → 41% (impossible mid-trip)"],
    ],
    col_widths=[2.3*cm, 2.5*cm, 6.2*cm, 6.5*cm]
))
story.append(sp(6))
story.append(colored_box(
    "<b>🚨 Critical Cascade:</b> The 1450ms network spike at 10:06:10 directly caused the Zone_B "
    "lock timeout 8 seconds later, which triggered the automatic safety mechanism cancelling "
    "Trip T101. The <b>entire failure chain spanned only 10 seconds</b>.",
    PINK, RED
))

# ── PAGE 2 ────────────────────────────────────────────────────────
story.append(PageBreak())

# ── 4. FIVE ANOMALIES ─────────────────────────────────────────────
story += section_title("4. Five Detected Anomalies")

anomalies = [
    ("ANOMALY 1 — Network Latency Spike (Robot_01)", RED,
     "<b>Observed:</b> Network latency of <b>1450 ms</b> at 10:06:10, confirmed in both event logs and telemetry.<br/>"
     "<b>Threshold:</b> Normal ops require &lt;200 ms for lock acquisition RPC calls.<br/>"
     "<b>Impact:</b> <b>Mission-critical.</b> Directly caused Trip T101 cancellation."),
    ("ANOMALY 2 — CPU Saturation (Robot_02)", NAVY,
     "<b>Observed:</b> CPU utilization reached <b>95%</b> at 10:21:30, well above the 90% alert threshold.<br/>"
     "<b>Impact:</b> Non-critical. Robot_02 successfully completed Trip T102, demonstrating edge-software resilience."),
    ("ANOMALY 3 — SLAM Localization Glitch (Robot_03)", NAVY,
     "<b>Observed:</b> Telemetry logged coordinates <b>X:999, Y:999</b> at 10:18:05 — a sentinel value "
     "indicating an unhandled null or out-of-bounds SLAM output.<br/>"
     "<b>Impact:</b> Non-critical. Robot self-recovered within 10 seconds and completed Trip T204."),
    ("ANOMALY 4 — Impossible Battery Jump (Robot_04)", NAVY,
     "<b>Observed:</b> Battery level rose from <b>32% → 41%</b> during an active running trip at 10:44:00. "
     "Confirmed by a BatteryLevelJump event log entry.<br/>"
     "<b>Impact:</b> Non-critical operationally, but <b>hardware-critical</b>. AMRs cannot charge while in motion. "
     "This isolates a defective Battery Management System (BMS) sensor requiring replacement."),
    ("ANOMALY 5 — Event Log Idempotency Bug (Robot_02)", NAVY,
     "<b>Observed:</b> The TripStarted event for Trip T102 was logged <b>twice</b> at exactly 10:15:00.<br/>"
     "<b>Impact:</b> Non-critical operationally, but indicates a bug in the telemetry ingestion pipeline "
     "that could corrupt downstream analytics, aggregations, and billing counts."),
]

for (title, color, desc) in anomalies:
    label_data = [[Paragraph(title, S("lbl", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold"))]]
    label_tbl = Table(label_data, colWidths=[doc.width])
    label_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
    ]))
    desc_data = [[Paragraph(desc, S("d", fontSize=9, textColor=BLACK, leading=13))]]
    desc_tbl = Table(desc_data, colWidths=[doc.width])
    desc_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), LGRAY),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LINEBELOW",     (0,0),(-1,-1), 0.5, MGRAY),
    ]))
    story.append(KeepTogether([label_tbl, desc_tbl, sp(5)]))

story.append(sp(4))

# ── 5. ROOT CAUSE ─────────────────────────────────────────────────
story += section_title("5. Root Cause")
story.append(verdict_box(
    "Root Cause: A severe network latency spike (1450ms) on Robot_01 prevented it from "
    "communicating with the resource management server within the required timeout window. "
    "The server, unable to receive lock acquisition confirmation for Zone_B, triggered an "
    "automatic safety timeout and cancelled Trip T101.\n\n"
    "Compute was stable (54% CPU). Battery was NOT the cause. "
    "The failure was purely a network-layer issue."
))
story.append(sp(6))
story.append(Paragraph("<b>Confirmed Evidence Chain:</b>", bold9))
story.append(Paragraph("1. NetworkLatencyHigh (1450ms) logged at <b>10:06:10</b>", bullet_style))
story.append(Paragraph("2. ResourceLockTimeout (Zone_B) logged <b>8 seconds later</b> at 10:06:18", bullet_style))
story.append(Paragraph("3. TripCancelled (T101) logged <b>2 seconds later</b> at 10:06:20", bullet_style))

# ── PAGE 3 ────────────────────────────────────────────────────────
story.append(PageBreak())

# ── 6. ADDITIONAL OBSERVATION ─────────────────────────────────────
story += section_title("6. Additional Observation — Hidden Safety Risk")
story.append(colored_box(
    "<b>⚠ Critical Safety Design Flaw Identified</b><br/><br/>"
    "At 10:05:55, Robot_01 generated a <b>BatteryLowWarning</b> — and yet the system allowed the robot "
    "to continue its trip, acquire Zone_A, and attempt to acquire Zone_B.<br/><br/>"
    "<b>Why this is dangerous:</b> In a warehouse environment, if a low-battery robot acquires a lock "
    "on a shared critical zone (e.g., a central intersection) and its battery dies mid-transit, it creates "
    "a <b>physical blockade</b>. Other robots cannot enter that zone until the lock is manually released "
    "and the robot is physically removed — potentially shutting down the <b>entire fleet's throughput</b>.<br/><br/>"
    "<b>Recommendation:</b> Implement a <i>pre-trip battery gate</i> — any robot below a configurable "
    "threshold (e.g., 30%) should be barred from acquiring new zone locks and immediately routed to a charging dock.",
    YELLOW, YLBDR
))
story.append(sp(8))

# ── 7. CONCLUSION ─────────────────────────────────────────────────
story += section_title("7. Conclusion")
story.append(Paragraph(
    "This investigation conclusively identified a <b>network-induced resource lock timeout</b> as the sole "
    "cause of the mission-critical Trip T101 cancellation. The four secondary anomalies (CPU saturation, "
    "SLAM glitch, BMS sensor fault, and log duplication) were isolated to individual robots and did not "
    "affect fleet-wide operations — a testament to the robustness of the edge-deployed robot software.",
    body_style
))
story.append(sp(8))

story.append(make_table(
    ["Finding", "Status", "Action Required"],
    [
        ["Robot_01 Trip Cancellation", "Root cause proven",       "Network SLA audit + redundancy review"],
        ["Robot_02 CPU Saturation",    "Edge software resilient", "Monitor; set capacity alerts"],
        ["Robot_03 SLAM Glitch",       "Self-recovered",          "Improve SLAM null handling"],
        ["Robot_04 BMS Sensor Fault",  "Hardware defect",         "BMS replacement & calibration"],
        ["Pipeline Idempotency Bug",   "Software defect",         "Fix ingestion deduplication logic"],
        ["Low-battery lock policy",    "SAFETY RISK",             "Implement pre-trip battery gate — URGENT"],
    ],
    col_widths=[5.5*cm, 4.0*cm, 8.0*cm]
))
story.append(sp(10))
story.append(colored_box(
    "<b>Key Takeaway:</b> The most urgent systemic risk is not the network incident itself, but the "
    "<b>absence of a battery-level pre-check</b> before zone lock acquisition — a policy gap that "
    "could cause a significantly more severe operational disruption if left unaddressed.",
    PINK, RED
))
story.append(sp(16))
story.append(hr())
story.append(Paragraph(
    "Fleet Observability &amp; Incident Investigation · Data Analytics &amp; Observability Internship · July 2026",
    small_style
))

# ── BUILD ─────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF successfully generated: {OUTPUT}")
