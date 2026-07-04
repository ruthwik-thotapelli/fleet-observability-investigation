import subprocess, sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "-q"])

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import Flowable

OUTPUT = "docs/Executive_Summary.pdf"
W, H = A4

# ── Color Palette ──────────────────────────────────────────────────
NAVY    = colors.HexColor("#1B2A4A")   # deep navy
ACCENT  = colors.HexColor("#2563EB")   # professional blue
ACCENT2 = colors.HexColor("#0EA5E9")   # sky blue
MUTED   = colors.HexColor("#64748B")   # slate
LIGHT   = colors.HexColor("#F1F5F9")   # light gray bg
BORDER  = colors.HexColor("#CBD5E1")   # border gray
WHITE   = colors.white
BLACK   = colors.HexColor("#0F172A")
RED_SOFT= colors.HexColor("#FEF2F2")
RED_BDR = colors.HexColor("#FCA5A5")
RED_TXT = colors.HexColor("#991B1B")
YLW_BG  = colors.HexColor("#FFFBEB")
YLW_BDR = colors.HexColor("#FCD34D")
YLW_TXT = colors.HexColor("#92400E")
GRN_BG  = colors.HexColor("#F0FDF4")
GRN_BDR = colors.HexColor("#86EFAC")
GRN_TXT = colors.HexColor("#166534")
BLU_BG  = colors.HexColor("#EFF6FF")
BLU_BDR = colors.HexColor("#BFDBFE")

# ── Sidebar Bar Flowable ──────────────────────────────────────────
class SideBar(Flowable):
    """Draws a colored left-border accent bar"""
    def __init__(self, height, color=ACCENT, width=4):
        Flowable.__init__(self)
        self.bar_height = height
        self.bar_color  = color
        self.bar_width  = width
        self.width  = 0
        self.height = 0

    def draw(self):
        self.canv.setFillColor(self.bar_color)
        self.canv.rect(0, -self.bar_height+2, self.bar_width, self.bar_height, fill=1, stroke=0)


# ── Styles ─────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE   = S("T",  fontSize=22, textColor=WHITE,  fontName="Helvetica-Bold", leading=26)
SUBT    = S("ST", fontSize=9,  textColor=colors.HexColor("#CBD5E1"), leading=14)
H2      = S("H2", fontSize=11, textColor=NAVY,   fontName="Helvetica-Bold", spaceBefore=0, spaceAfter=4)
BODY    = S("Bo", fontSize=9,  textColor=BLACK,  leading=14, alignment=TA_JUSTIFY)
BUL     = S("Bl", fontSize=9,  textColor=BLACK,  leading=13, leftIndent=12)
SMALL   = S("Sm", fontSize=8,  textColor=MUTED,  alignment=TA_CENTER)
BOLD9   = S("B9", fontSize=9,  textColor=NAVY,   fontName="Helvetica-Bold")
MONO    = S("Mo", fontSize=8,  textColor=MUTED,  fontName="Courier")
TH      = S("TH", fontSize=8,  textColor=WHITE,  fontName="Helvetica-Bold", alignment=TA_LEFT)
TD      = S("TD", fontSize=8,  textColor=BLACK,  leading=12)
CHIP    = S("Ch", fontSize=7,  textColor=WHITE,  fontName="Helvetica-Bold", alignment=TA_CENTER)

def sp(h=4):  return Spacer(1, h)

# ── Helpers ────────────────────────────────────────────────────────
INNER_W = W - 3.6*cm   # total inner width

def section_header(num, text):
    """Clean section header with number badge + text, no line"""
    badge_data = [[Paragraph(f"<b>{num}</b>", S("nb", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]]
    badge = Table(badge_data, colWidths=[0.7*cm], rowHeights=[0.7*cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), ACCENT),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("ROUNDEDCORNERS",[4]),
    ]))
    title_cell = Paragraph(f"<b>{text}</b>", S("sh", fontSize=12, textColor=NAVY, fontName="Helvetica-Bold"))
    row = Table([[badge, title_cell]], colWidths=[0.9*cm, INNER_W - 0.9*cm])
    row.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    bg = Table([[row]], colWidths=[INNER_W])
    bg.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), LIGHT),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LINEBELOW",     (0,0),(-1,-1), 2, ACCENT),
    ]))
    return [bg, sp(8)]

def make_table(headers, rows, col_widths=None, stripe=True):
    data = [[Paragraph(h, TH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), TD) for c in row])
    if col_widths is None:
        col_widths = [INNER_W / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",    (0,0),  (-1,0),  NAVY),
        ("LINEBELOW",     (0,0),  (-1,-1), 0.25, BORDER),
        ("LEFTPADDING",   (0,0),  (-1,-1), 7),
        ("RIGHTPADDING",  (0,0),  (-1,-1), 7),
        ("TOPPADDING",    (0,0),  (-1,-1), 5),
        ("BOTTOMPADDING", (0,0),  (-1,-1), 5),
        ("VALIGN",        (0,0),  (-1,-1), "TOP"),
    ]
    if stripe:
        for i in range(1, len(data), 2):
            style.append(("BACKGROUND", (0,i), (-1,i), LIGHT))
    t.setStyle(TableStyle(style))
    return t

def callout(text, bg, border, txt_color=BLACK):
    cell = Paragraph(text, S("ca", fontSize=9, textColor=txt_color, leading=13))
    t = Table([[cell]], colWidths=[INNER_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LINEBEFORE",    (0,0),(0,-1),  4, border),
        ("BOX",           (0,0),(-1,-1), 0.5, border),
    ]))
    return t

def anomaly_card(label, label_color, title, text):
    chip = Table([[Paragraph(label, CHIP)]], colWidths=[2.5*cm])
    chip.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), label_color),
        ("TOPPADDING",    (0,0),(-1,-1), 2),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("ROUNDEDCORNERS",[3]),
    ]))
    title_p = Paragraph(f"<b>{title}</b>", S("at", fontSize=9, textColor=NAVY, fontName="Helvetica-Bold"))
    header_row = Table([[chip, title_p]], colWidths=[2.7*cm, INNER_W - 2.7*cm])
    header_row.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    body_p = Paragraph(text, S("ab", fontSize=9, textColor=BLACK, leading=13))
    card = Table([[header_row], [body_p]], colWidths=[INNER_W])
    card.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), WHITE),
        ("BACKGROUND",    (0,0),(-1,0),  colors.HexColor("#F8FAFF")),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LINEBEFORE",    (0,0),(0,-1),  3, label_color),
        ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
        ("LINEBELOW",     (0,0),(-1,0),  0.5, BORDER),
    ]))
    return KeepTogether([card, sp(5)])

# ══════════════════════════════════════════════════════════════════
# PAGE TEMPLATE with header/footer
# ══════════════════════════════════════════════════════════════════
def on_page(canvas, doc):
    canvas.saveState()
    # Top banner
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 1.0*cm, W, 1.0*cm, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, H - 1.0*cm, 0.8*cm, 1.0*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(WHITE)
    canvas.drawString(1.0*cm, H - 0.65*cm, "FLEET OBSERVABILITY & INCIDENT INVESTIGATION")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(W - 1.0*cm, H - 0.65*cm, f"Executive Summary  |  July 2026")
    # Footer
    canvas.setFillColor(LIGHT)
    canvas.rect(0, 0, W, 0.9*cm, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, W, 0.15*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.8*cm, 0.32*cm, "Ruthwik Thotapelli  |  Data Analytics & Observability Intern  |  Ati Motors")
    canvas.drawRightString(W - 1.8*cm, 0.32*cm, f"Page {doc.page} of 3")
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    # Full-width navy hero banner
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 5.2*cm, W, 5.2*cm, fill=1, stroke=0)
    # Accent stripe
    canvas.setFillColor(ACCENT)
    canvas.rect(0, H - 5.2*cm, W, 0.25*cm, fill=1, stroke=0)
    canvas.setFillColor(ACCENT2)
    canvas.rect(0, H - 5.2*cm + 0.25*cm, W, 0.08*cm, fill=1, stroke=0)
    # Top-right decorative block
    canvas.setFillColor(ACCENT)
    canvas.setFillAlpha(0.15)
    canvas.rect(W - 5*cm, H - 5.2*cm, 5*cm, 5.2*cm, fill=1, stroke=0)
    canvas.setFillAlpha(1.0)
    # Title text
    canvas.setFont("Helvetica-Bold", 20)
    canvas.setFillColor(WHITE)
    canvas.drawString(1.8*cm, H - 2.2*cm, "Fleet Observability &")
    canvas.drawString(1.8*cm, H - 2.9*cm, "Incident Investigation")
    canvas.setFont("Helvetica", 9.5)
    canvas.setFillColor(colors.HexColor("#93C5FD"))
    canvas.drawString(1.8*cm, H - 3.55*cm, "Executive Summary Report  \u2014  Data Analytics & Observability Internship")
    # Meta info chips
    meta = [
        ("Author", "Ruthwik Thotapelli"),
        ("Role", "Data Analytics Intern"),
        ("Incident", "June 30, 2026"),
        ("Window", "10:00 AM \u2013 11:00 AM"),
    ]
    x = 1.8*cm
    for label, value in meta:
        canvas.setFillColor(ACCENT)
        canvas.setFillAlpha(0.35)
        canvas.roundRect(x, H - 4.65*cm, 4.8*cm, 0.6*cm, 4, fill=1, stroke=0)
        canvas.setFillAlpha(1.0)
        canvas.setFont("Helvetica-Bold", 6.5)
        canvas.setFillColor(colors.HexColor("#93C5FD"))
        canvas.drawString(x + 0.2*cm, H - 4.18*cm, label.upper())
        canvas.setFont("Helvetica", 8.5)
        canvas.setFillColor(WHITE)
        canvas.drawString(x + 0.2*cm, H - 4.52*cm, value)
        x += 5.1*cm
    # Footer
    canvas.setFillColor(LIGHT)
    canvas.rect(0, 0, W, 0.9*cm, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, W, 0.15*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.8*cm, 0.32*cm, "Ruthwik Thotapelli  |  Data Analytics & Observability Intern  |  Ati Motors")
    canvas.drawRightString(W - 1.8*cm, 0.32*cm, "Page 1 of 3")
    canvas.restoreState()


# ══════════════════════════════════════════════════════════════════
# BUILD CONTENT
# ══════════════════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=5.6*cm,   bottomMargin=1.4*cm,
)

story = []

# ── 1. OBJECTIVE ──────────────────────────────────────────────────
story += section_header("1", "Project Objective")
story.append(Paragraph(
    "To conduct a rigorous, data-driven postmortem on a critical operational incident affecting a fleet "
    "of Autonomous Mobile Robots (AMRs). The goal was to move beyond assumptions and use "
    "<b>raw telemetry, trip lifecycle records, and system event logs</b> to precisely reconstruct "
    "the failure sequence, identify all fleet-wide anomalies, and conclusively prove the root cause "
    "of the mission-critical trip cancellation.",
    BODY
))
story.append(sp(12))

# ── 2. APPROACH ───────────────────────────────────────────────────
story += section_header("2", "Approach")
story.append(make_table(
    ["Phase", "Module", "Description"],
    [
        ["1  Data Profiling",           "preprocessing.py",        "Assessed dataset health — checked missing values, timestamp integrity, and row uniqueness across all three data sources before any analysis."],
        ["2  Exploratory Analysis",     "exploratory_analysis.py", "Visualized CPU, battery, and network latency distributions fleet-wide to isolate statistical outliers."],
        ["3  Timeline Reconstruction",  "incident_timeline.py",    "Fused three asynchronous data streams (telemetry, trips, events) into a single, second-level chronological timeline."],
        ["4  Root Cause Extraction",    "root_cause_analysis.py",  "Applied rule-based pattern matching on the fused timeline to link prior events to trip cancellation outcomes."],
    ],
    col_widths=[3.8*cm, 4.2*cm, 9.5*cm]
))
story.append(sp(12))

# ── 3. INCIDENT TIMELINE ──────────────────────────────────────────
story += section_header("3", "Incident Timeline  (10:00 AM \u2013 11:00 AM)")
story.append(make_table(
    ["Time", "Robot", "Event", "Details"],
    [
        ["10:05:12", "Robot_01", "Trip T101 Started",           "Source to Destination"],
        ["10:05:14", "Robot_01", "Resource Lock Acquired",      "Zone_A secured"],
        ["10:05:55", "Robot_01", "Battery Low Warning",         "Pre-trip check missed"],
        ["10:06:10", "Robot_01", "NETWORK LATENCY SPIKE",       "1450 ms sustained"],
        ["10:06:18", "Robot_01", "RESOURCE LOCK TIMEOUT",       "Zone_B -- failed to acquire"],
        ["10:06:20", "Robot_01", "TRIP T101 CANCELLED",         "Safety timeout triggered"],
        ["10:15:00", "Robot_02", "Trip T102 Started",           "Duplicate log entry observed"],
        ["10:17:40", "Robot_03", "Trip T204 Started",           "Zone_C lock acquired"],
        ["10:18:05", "Robot_03", "Position Jump Detected",      "Coords: X:999, Y:999"],
        ["10:18:15", "Robot_03", "Trip T204 Completed",         "Self-recovered successfully"],
        ["10:21:30", "Robot_02", "CPU Saturation",              "95% CPU load"],
        ["10:24:00", "Robot_02", "Trip T102 Completed",         "Resilient under compute load"],
        ["10:40:00", "Robot_04", "Trip T301 Started",           "Normal start"],
        ["10:44:00", "Robot_04", "Battery Level Jump",          "32% to 41% (impossible mid-trip)"],
    ],
    col_widths=[2.2*cm, 2.4*cm, 6.0*cm, 6.9*cm]
))
story.append(sp(7))
story.append(callout(
    "<b>Critical Cascade:</b>  The 1450ms network spike at 10:06:10 directly caused the Zone_B lock timeout "
    "8 seconds later, which triggered the automatic safety mechanism cancelling Trip T101. "
    "The <b>entire failure chain spanned only 10 seconds</b>.",
    BLU_BG, ACCENT
))

# ── PAGE 2 ────────────────────────────────────────────────────────
story.append(PageBreak())

# ── 4. FIVE ANOMALIES ─────────────────────────────────────────────
story += section_header("4", "Five Detected Anomalies")

story.append(anomaly_card(
    "ANOMALY 1  |  CRITICAL", colors.HexColor("#DC2626"),
    "Network Latency Spike  \u2014  Robot_01",
    "<b>Observed:</b> Network latency of <b>1450 ms</b> at 10:06:10, confirmed in both event logs and telemetry.<br/>"
    "<b>Threshold:</b> Normal operations require &lt;200 ms for lock acquisition RPC calls.<br/>"
    "<b>Impact:</b> Mission-critical. Directly caused Trip T101 cancellation."
))
story.append(anomaly_card(
    "ANOMALY 2  |  WARNING", colors.HexColor("#D97706"),
    "CPU Saturation  \u2014  Robot_02",
    "<b>Observed:</b> CPU utilization reached <b>95%</b> at 10:21:30, above the 90% alert threshold.<br/>"
    "<b>Impact:</b> Non-critical. Robot_02 successfully completed Trip T102, demonstrating edge-software resilience under extreme compute pressure."
))
story.append(anomaly_card(
    "ANOMALY 3  |  WARNING", colors.HexColor("#D97706"),
    "SLAM Localization Glitch  \u2014  Robot_03",
    "<b>Observed:</b> Telemetry logged coordinates <b>X:999, Y:999</b> at 10:18:05 \u2014 a sentinel value indicating "
    "an unhandled null or out-of-bounds SLAM output.<br/>"
    "<b>Impact:</b> Non-critical. Robot self-recovered within 10 seconds and completed Trip T204."
))
story.append(anomaly_card(
    "ANOMALY 4  |  HARDWARE", colors.HexColor("#7C3AED"),
    "Impossible Battery Jump  \u2014  Robot_04",
    "<b>Observed:</b> Battery level rose from <b>32% to 41%</b> during an active running trip at 10:44:00, "
    "confirmed by a BatteryLevelJump event log entry.<br/>"
    "<b>Impact:</b> Hardware-critical. AMRs cannot charge while in motion. This isolates a defective "
    "Battery Management System (BMS) sensor requiring replacement."
))
story.append(anomaly_card(
    "ANOMALY 5  |  SOFTWARE", colors.HexColor("#0891B2"),
    "Event Log Idempotency Bug  \u2014  Robot_02",
    "<b>Observed:</b> The TripStarted event for Trip T102 was logged <b>twice</b> at exactly 10:15:00.<br/>"
    "<b>Impact:</b> Non-critical operationally, but this indicates a bug in the telemetry ingestion pipeline "
    "that could corrupt downstream analytics, aggregations, and billing counts."
))

story.append(sp(6))

# ── 5. ROOT CAUSE ─────────────────────────────────────────────────
story += section_header("5", "Root Cause")

# Verdict box
verdict_data = [[
    Paragraph(
        "<b>Root Cause: Network-Induced Resource Lock Timeout</b><br/><br/>"
        "A severe network latency spike (1450ms) on Robot_01 prevented it from communicating with "
        "the resource management server within the required timeout window. The server, unable to "
        "receive lock acquisition confirmation for Zone_B, triggered an automatic safety timeout "
        "and cancelled Trip T101.<br/><br/>"
        "<b>Compute was stable at 54% CPU. Battery level was 76%. The failure was purely a network-layer issue.</b>",
        S("vd", fontSize=9.5, textColor=WHITE, leading=15)
    )
]]
verdict_tbl = Table(verdict_data, colWidths=[INNER_W])
verdict_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), NAVY),
    ("LEFTPADDING",   (0,0),(-1,-1), 16),
    ("RIGHTPADDING",  (0,0),(-1,-1), 16),
    ("TOPPADDING",    (0,0),(-1,-1), 12),
    ("BOTTOMPADDING", (0,0),(-1,-1), 12),
    ("LINEBEFORE",    (0,0),(0,-1),  5, ACCENT2),
]))
story.append(verdict_tbl)
story.append(sp(8))

story.append(Paragraph("<b>Confirmed Evidence Chain:</b>", BOLD9))
story.append(sp(3))
evidence = make_table(
    ["#", "Timestamp", "Event", "Proof"],
    [
        ["1", "10:06:10", "NetworkLatencyHigh (1450ms)", "Event log + telemetry data both confirm"],
        ["2", "10:06:18", "ResourceLockTimeout (Zone_B)", "8 seconds after latency spike"],
        ["3", "10:06:20", "TripCancelled (T101)",          "2 seconds after lock timeout"],
    ],
    col_widths=[0.6*cm, 2.4*cm, 5.5*cm, 9.0*cm]
)
story.append(evidence)

# ── PAGE 3 ────────────────────────────────────────────────────────
story.append(PageBreak())

# ── 6. ADDITIONAL OBSERVATION ─────────────────────────────────────
story += section_header("6", "Additional Observation \u2014 Hidden Safety Risk")

story.append(callout(
    "<b>Safety Design Flaw Identified</b><br/><br/>"
    "At 10:05:55, Robot_01 generated a <b>BatteryLowWarning</b> and yet the system allowed the robot "
    "to continue its trip, acquire Zone_A, and attempt to acquire Zone_B.<br/><br/>"
    "<b>Why this is dangerous:</b> In a warehouse environment, if a low-battery robot acquires a lock "
    "on a shared critical zone and its battery dies mid-transit, it creates a <b>physical blockade</b>. "
    "No other robot can enter that zone until the lock is manually released and the robot is physically "
    "removed \u2014 potentially <b>shutting down the entire fleet's throughput</b>.<br/><br/>"
    "<b>Recommendation:</b> Implement a pre-trip battery gate \u2014 any robot below a configurable "
    "threshold (e.g., 30%) should be barred from acquiring new zone locks and immediately routed to a charging dock.",
    YLW_BG, YLW_BDR, colors.HexColor("#78350F")
))
story.append(sp(12))

# ── 7. CONCLUSION ─────────────────────────────────────────────────
story += section_header("7", "Conclusion")
story.append(Paragraph(
    "This investigation conclusively identified a <b>network-induced resource lock timeout</b> as the sole "
    "cause of the mission-critical Trip T101 cancellation. The four secondary anomalies were isolated "
    "to individual robots and did not affect fleet-wide operations \u2014 a testament to the robustness "
    "of the edge-deployed robot software.",
    BODY
))
story.append(sp(8))

story.append(make_table(
    ["Finding", "Severity", "Status", "Recommended Action"],
    [
        ["Robot_01 Trip Cancellation",  "CRITICAL",  "Root cause proven",      "Network SLA audit + redundancy review"],
        ["Robot_02 CPU Saturation",     "WARNING",   "Edge SW resilient",      "Set capacity alerts; monitor trends"],
        ["Robot_03 SLAM Glitch",        "WARNING",   "Self-recovered",         "Improve SLAM null/boundary handling"],
        ["Robot_04 BMS Sensor Fault",   "HARDWARE",  "Defect confirmed",       "BMS sensor replacement & calibration"],
        ["Pipeline Idempotency Bug",    "SOFTWARE",  "Defect confirmed",       "Fix ingestion deduplication logic"],
        ["Low-battery lock policy",     "SAFETY",    "Gap identified",         "Implement pre-trip battery gate ASAP"],
    ],
    col_widths=[4.5*cm, 2.2*cm, 3.0*cm, 7.8*cm]
))
story.append(sp(10))

story.append(callout(
    "<b>Key Takeaway:</b>  The most urgent systemic risk is not the network incident itself, but the "
    "<b>absence of a battery-level pre-check</b> before zone lock acquisition \u2014 a policy gap that "
    "could cause a significantly more severe operational disruption and full fleet gridlock if left unaddressed.",
    RED_SOFT, RED_BDR, colors.HexColor("#7F1D1D")
))

story.append(sp(16))
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))
story.append(Paragraph(
    "Fleet Observability &amp; Incident Investigation  \u00b7  Data Analytics &amp; Observability Internship Submission  \u00b7  July 2026",
    SMALL
))

# ── BUILD ─────────────────────────────────────────────────────────
doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
print("PDF generated: " + OUTPUT)
