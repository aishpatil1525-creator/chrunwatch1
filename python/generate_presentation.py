"""
Generate Professional 16:9 PowerPoint Presentation for ChurnWatch
Using python-pptx with sleek corporate styling, metrics, tables, and embedded high-res screenshots.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
OUTPUT_PPTX = os.path.join(BASE_DIR, "presentation.pptx")

# Palette Constants
NAVY = RGBColor(23, 36, 58)      # #17243A
PRIMARY = RGBColor(66, 99, 235)  # #4263EB
TEAL = RGBColor(21, 157, 145)    # #159D91
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(32, 43, 60)      # #202B3C
MUTED = RGBColor(119, 131, 153)  # #778399
LIGHT_BG = RGBColor(245, 247, 251)# #F5F7FB
CARD_BORDER = RGBColor(226, 232, 240)
DANGER = RGBColor(217, 75, 85)   # #D94B55
SUCCESS = RGBColor(22, 138, 99)  # #168A63

prs = Presentation()
# Set widescreen 16:9 (13.333 x 7.5 inches)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="CHURNWATCH ANALYTICS"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = PRIMARY
    p_c.font.name = "Arial"

    # Main slide title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.6))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_t.font.name = "Arial"

# -------------------------------------------------------------
# SLIDE 1: TITLE SLIDE (Deep Navy)
# -------------------------------------------------------------
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.color.rgb = NAVY

# Title
tbox1 = slide1.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(11), Inches(2.2))
tf1 = tbox1.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "ChurnWatch"
p1.font.size = Pt(46)
p1.font.bold = True
p1.font.color.rgb = WHITE
p1.font.name = "Arial"

p2 = tf1.add_paragraph()
p2.text = "Customer Retention & Churn Risk Analytics Platform"
p2.font.size = Pt(22)
p2.font.color.rgb = TEAL
p2.font.name = "Arial"
p2.space_before = Pt(8)

p3 = tf1.add_paragraph()
p3.text = "Data Analytics Internship Evaluation & Project Submission"
p3.font.size = Pt(14)
p3.font.color.rgb = RGBColor(160, 174, 192)
p3.font.name = "Arial"
p3.space_before = Pt(18)

# Author metadata box
meta_box = slide1.shapes.add_textbox(Inches(1.2), Inches(5.4), Inches(10), Inches(1.2))
tf_m = meta_box.text_frame
pm1 = tf_m.paragraphs[0]
pm1.text = "Author: Data Analytics Candidate   |   Project: Minor Project 1"
pm1.font.size = Pt(12)
pm1.font.bold = True
pm1.font.color.rgb = WHITE

pm2 = tf_m.add_paragraph()
pm2.text = "Stack: Python (Scikit-Learn/Pandas), ANSI SQL, Vanilla JS, HTML5/CSS3, Chart.js"
pm2.font.size = Pt(11)
pm2.font.color.rgb = RGBColor(160, 174, 192)

# -------------------------------------------------------------
# SLIDE 2: EXECUTIVE SUMMARY & CORE METRICS
# -------------------------------------------------------------
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Executive Problem Statement & Business Opportunity", "EXECUTIVE SUMMARY")

# Narrative box
nbox = slide2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(1.2))
tf_n = nbox.text_frame
tf_n.word_wrap = True
pn = tf_n.paragraphs[0]
pn.text = "Customer Acquisition Cost (CAC) in B2B SaaS is 5x–7x higher than retention cost. ChurnWatch consolidates multi-dimensional customer behavioral signals (licensing, engagement decay, and ticket friction) into an actionable retention engine."
pn.font.size = Pt(14)
pn.font.color.rgb = DARK

# 4 Metric Cards
kpis = [
    {"label": "TOTAL ACCOUNTS", "val": "1,250", "sub": "Evaluated B2B portfolio", "color": PRIMARY},
    {"label": "CHURN RATE", "val": "19.2%", "sub": "-0.8% MoM improvement", "color": DANGER},
    {"label": "RENEWAL RATE", "val": "80.8%", "sub": "+1.4% cohort benchmark", "color": SUCCESS},
    {"label": "TOTAL MRR", "val": "$287,450", "sub": "$61,398 high risk exposure", "color": TEAL}
]

for idx, k in enumerate(kpis):
    x = Inches(0.8 + idx * 2.95)
    y = Inches(2.9)
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.8), Inches(2.4))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_BG
    card.line.color.rgb = CARD_BORDER

    tb = slide2.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(2.4), Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p_l = tf.paragraphs[0]
    p_l.text = k["label"]
    p_l.font.size = Pt(10)
    p_l.font.bold = True
    p_l.font.color.rgb = MUTED

    p_v = tf.add_paragraph()
    p_v.text = k["val"]
    p_v.font.size = Pt(28)
    p_v.font.bold = True
    p_v.font.color.rgb = k["color"]
    p_v.space_before = Pt(8)

    p_s = tf.add_paragraph()
    p_s.text = k["sub"]
    p_s.font.size = Pt(10)
    p_s.font.color.rgb = DARK
    p_s.space_before = Pt(8)

# Bottom Key Takeaway
tbox_bot = slide2.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.0))
tf_b = tbox_bot.text_frame
tf_b.word_wrap = True
pb = tf_b.paragraphs[0]
pb.text = "Key Strategic Value: By triaging the top 20% highest-risk accounts, Customer Success teams can protect up to $61,398 in monthly recurring revenue with high-touch intervention playbooks."
pb.font.size = Pt(12)
pb.font.bold = True
pb.font.color.rgb = NAVY

# -------------------------------------------------------------
# SLIDE 3: DATA ARCHITECTURE & UNIFIED PIPELINE
# -------------------------------------------------------------
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Multi-Source Relational Data Architecture", "DATA ENGINEERING")

cols = [
    {"title": "1. Subscriptions Table", "sub": "Commercial Contract Baseline", "items": ["Customer ID & Company Name", "Plan Tier: Starter, Pro, Enterprise", "Monthly Recurring Revenue (MRR)", "Tenure Months & Billing Cycle", "Contract Renewal Dates"], "color": PRIMARY},
    {"title": "2. Product Usage Table", "sub": "Active Behavioral Telemetry", "items": ["Active Users vs Licensed Seats", "Seat Utilization Percentage", "Monthly Active Login Days", "Feature Adoption Index (0-100)", "30-Day Engagement Trend %"], "color": TEAL},
    {"title": "3. Support Tickets Table", "sub": "Friction & Dissatisfaction", "items": ["Total Tickets Past 90 Days", "Open Critical Escalations", "Average Resolution Time (Hours)", "Customer Satisfaction (CSAT 1-5)", "NPS Sentiment Classification"], "color": DANGER}
]

for idx, c in enumerate(cols):
    x = Inches(0.8 + idx * 3.95)
    y = Inches(1.5)
    box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.75), Inches(4.5))
    box.fill.solid()
    box.fill.fore_color.rgb = LIGHT_BG
    box.line.color.rgb = CARD_BORDER

    tb = slide3.shapes.add_textbox(x + Inches(0.25), y + Inches(0.25), Inches(3.25), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = c["title"]
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = c["color"]

    p2 = tf.add_paragraph()
    p2.text = c["sub"]
    p2.font.size = Pt(10)
    p2.font.bold = True
    p2.font.color.rgb = MUTED
    p2.space_before = Pt(4)

    for item in c["items"]:
        pi = tf.add_paragraph()
        pi.text = f"•  {item}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(10)

bottom_master = slide3.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.7))
tf_bm = bottom_master.text_frame
p_bm = tf_bm.paragraphs[0]
p_bm.text = "→ Master Table: unified_customers.csv merges all 3 streams into 1,250 analytical accounts with computed risk scores."
p_bm.font.size = Pt(12)
p_bm.font.bold = True
p_bm.font.color.rgb = NAVY

# -------------------------------------------------------------
# SLIDE 4: RISK SCORING METHODOLOGY & FORMULA
# -------------------------------------------------------------
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Multi-Factor Churn Risk Scoring Index (0–100)", "ALGORITHMIC METHODOLOGY")

# Left Column: Dimension weights
left_box = slide4.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.5))
tf_l = left_box.text_frame
tf_l.word_wrap = True

pl1 = tf_l.paragraphs[0]
pl1.text = "Composite Weighted Scoring Dimensions:"
pl1.font.size = Pt(14)
pl1.font.bold = True
pl1.font.color.rgb = NAVY

dims = [
    ("35% Engagement Decay", "Penalizes significant drops in 30-day active sessions & usage."),
    ("25% Seat Underutilization", "Detects shelfware risk when paid licenses are left unassigned."),
    ("25% Support Friction", "Accounts for low CSAT (< 3.0) and open critical ticket escalations."),
    ("15% Contract Vulnerability", "Evaluates recency of login and monthly contract flexibility.")
]

for d_title, d_desc in dims:
    pd_t = tf_l.add_paragraph()
    pd_t.text = f"• {d_title}"
    pd_t.font.size = Pt(12)
    pd_t.font.bold = True
    pd_t.font.color.rgb = PRIMARY
    pd_t.space_before = Pt(12)

    pd_d = tf_l.add_paragraph()
    pd_d.text = d_desc
    pd_d.font.size = Pt(10.5)
    pd_d.font.color.rgb = DARK

# Right Column: Risk Stratification Tiers
r_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.5), Inches(5.5), Inches(4.8))
r_box.fill.solid()
r_box.fill.fore_color.rgb = LIGHT_BG
r_box.line.color.rgb = CARD_BORDER

tb_r = slide4.shapes.add_textbox(Inches(7.25), Inches(1.75), Inches(5.0), Inches(4.2))
tf_r = tb_r.text_frame
tf_r.word_wrap = True

pr1 = tf_r.paragraphs[0]
pr1.text = "Actionable Risk Stratification Bands:"
pr1.font.size = Pt(14)
pr1.font.bold = True
pr1.font.color.rgb = NAVY

tiers = [
    ("HIGH RISK (> 70 Score)", "252 Accounts ($61,398 MRR)", "Immediate CSM intervention required under 48h SLA. High probability of attrition.", DANGER),
    ("MEDIUM RISK (40–70 Score)", "156 Accounts ($36,144 MRR)", "Workflow enablement review & feature training required within 14-day SLA.", RGBColor(217, 144, 32)),
    ("LOW RISK (< 40 Score)", "842 Accounts ($189,908 MRR)", "Healthy accounts with strong adoption. Monitored via automated value summaries.", SUCCESS)
]

for t_title, t_sub, t_desc, col in tiers:
    pt1 = tf_r.add_paragraph()
    pt1.text = t_title
    pt1.font.size = Pt(11)
    pt1.font.bold = True
    pt1.font.color.rgb = col
    pt1.space_before = Pt(10)

    pt2 = tf_r.add_paragraph()
    pt2.text = f"{t_sub} — {t_desc}"
    pt2.font.size = Pt(9.5)
    pt2.font.color.rgb = DARK

# -------------------------------------------------------------
# SLIDE 5: MODEL EVALUATION & DRIVER FINDINGS (WITH CHART)
# -------------------------------------------------------------
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Machine Learning Validation & Key Predictive Drivers", "MODEL EVALUATION")

# Left text metrics
l_box5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.0), Inches(5.5))
tf5 = l_box5.text_frame
tf5.word_wrap = True

p5_1 = tf5.paragraphs[0]
p5_1.text = "Supervised Random Forest Benchmark:"
p5_1.font.size = Pt(14)
p5_1.font.bold = True
p5_1.font.color.rgb = NAVY

p5_metrics = [
    ("Classification Accuracy: 86.26%", "Exceeds standard 80% deployment baseline on test set."),
    ("ROC-AUC Score: 0.863", "Indicates strong discrimination between churners & healthy accounts."),
    ("Non-Churn Precision: 0.91", "Minimizes false alarms on stable, healthy customers."),
    ("Top Churn Predictor", "Engagement Change % accounts for 31.4% of model importance.")
]

for m_t, m_d in p5_metrics:
    pm = tf5.add_paragraph()
    pm.text = f"• {m_t}"
    pm.font.size = Pt(11.5)
    pm.font.bold = True
    pm.font.color.rgb = PRIMARY
    pm.space_before = Pt(10)

    pd = tf5.add_paragraph()
    pd.text = m_d
    pd.font.size = Pt(10)
    pd.font.color.rgb = DARK

# Embed Feature Importance Chart on Right
feat_chart = os.path.join(DATA_DIR, "feature_importance.png")
if os.path.exists(feat_chart):
    slide5.shapes.add_picture(feat_chart, Inches(6.0), Inches(1.5), width=Inches(6.5))

# -------------------------------------------------------------
# SLIDE 6: SAAS DASHBOARD DEMONSTRATION (WITH SCREENSHOT)
# -------------------------------------------------------------
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Human-Crafted SaaS Analytics Dashboard Interface", "PRODUCT EXPERIENCE")

# Embed Overview Screenshot
overview_ss = os.path.join(SCREENSHOTS_DIR, "01_overview_dashboard.png")
if os.path.exists(overview_ss):
    slide6.shapes.add_picture(overview_ss, Inches(0.8), Inches(1.4), width=Inches(8.2))

# Right Column Features
r_box6 = slide6.shapes.add_textbox(Inches(9.3), Inches(1.4), Inches(3.4), Inches(5.5))
tf6 = r_box6.text_frame
tf6.word_wrap = True

p6_1 = tf6.paragraphs[0]
p6_1.text = "Design Highlights:"
p6_1.font.size = Pt(14)
p6_1.font.bold = True
p6_1.font.color.rgb = NAVY

highlights = [
    ("Palette & Structure", "Deep Navy (#17243A) sidebar with soft light canvas (#F5F7FB) and 8px grid."),
    ("Executive KPI Cards", "Live counts, rates, and MoM deltas for high-level decision makers."),
    ("Chart.js Telemetry", "Dual-axis churn trajectories, plan tier comparisons, and risk donut."),
    ("Lightweight Tech Stack", "Zero build step, vanilla HTML/CSS/JS with Chart.js via CDN.")
]

for h_t, h_d in highlights:
    ph1 = tf6.add_paragraph()
    ph1.text = f"• {h_t}"
    ph1.font.size = Pt(11)
    ph1.font.bold = True
    ph1.font.color.rgb = PRIMARY
    ph1.space_before = Pt(10)

    ph2 = tf6.add_paragraph()
    ph2.text = h_d
    ph2.font.size = Pt(9.5)
    ph2.font.color.rgb = DARK

# -------------------------------------------------------------
# SLIDE 7: RETENTION OPERATIONS & ACTION QUEUE
# -------------------------------------------------------------
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Prioritized Retention Operations & Live CSM Triage", "OPERATIONAL PLAYBOOKS")

# Embed Operations Screenshot
ops_ss = os.path.join(SCREENSHOTS_DIR, "03_retention_operations_queue.png")
if os.path.exists(ops_ss):
    slide7.shapes.add_picture(ops_ss, Inches(0.8), Inches(1.4), width=Inches(8.2))

# Right Column Playbooks
r_box7 = slide7.shapes.add_textbox(Inches(9.3), Inches(1.4), Inches(3.4), Inches(5.5))
tf7 = r_box7.text_frame
tf7.word_wrap = True

p7_1 = tf7.paragraphs[0]
p7_1.text = "Operational Controls:"
p7_1.font.size = Pt(14)
p7_1.font.bold = True
p7_1.font.color.rgb = NAVY

ops_points = [
    ("Prioritized Queue", "Ranked dynamically by Risk Score and MRR exposure to maximize revenue saved."),
    ("Live Owner Reassignment", "Working dropdown updates customer success assignment instantly."),
    ("Status Mutations", "Switching status to 'Saved' secures MRR and recalculates portfolio stats in real-time."),
    ("Contextual Playbooks", "Automated recommendation rules based on support friction vs usage drop.")
]

for op_t, op_d in ops_points:
    po1 = tf7.add_paragraph()
    po1.text = f"• {op_t}"
    po1.font.size = Pt(11)
    po1.font.bold = True
    po1.font.color.rgb = TEAL
    po1.space_before = Pt(10)

    po2 = tf7.add_paragraph()
    po2.text = op_d
    po2.font.size = Pt(9.5)
    po2.font.color.rgb = DARK

# -------------------------------------------------------------
# SLIDE 8: PRODUCTION SQL ANALYTICAL SUITE
# -------------------------------------------------------------
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Production ANSI SQL Analytical Pipeline", "DATA PIPELINE")

sql_boxes = [
    ("1. Monthly Cohort Retention", "Utilizes DATE_TRUNC and multi-level aggregation CTEs to track account churn rate vs revenue churn rate across customer signup cohorts."),
    ("2. MoM Rolling Churn Window", "Implements LAG() and SUM() OVER (ORDER BY month) window functions to compute month-over-month trajectory deltas and cumulative MRR lost."),
    ("3. Risk Stratification CTEs", "Stratifies customers into High, Medium, and Low risk bands with aggregate MRR exposure and average product engagement."),
    ("4. CSM Portfolio Tracking", "Evaluates individual customer success manager portfolios, intervention completion rates, and active SLA adherence.")
]

for idx, (s_title, s_desc) in enumerate(sql_boxes):
    r = idx // 2
    c = idx % 2
    x = Inches(0.8 + c * 5.9)
    y = Inches(1.5 + r * 2.7)

    box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.4))
    box.fill.solid()
    box.fill.fore_color.rgb = LIGHT_BG
    box.line.color.rgb = CARD_BORDER

    tb = slide8.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(5.2), Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p1 = tf.paragraphs[0]
    p1.text = s_title
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = PRIMARY

    p2 = tf.add_paragraph()
    p2.text = s_desc
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = DARK
    p2.space_before = Pt(8)

# -------------------------------------------------------------
# SLIDE 9: SUMMARY & INTERNSHIP EVALUATION TAKEAWAYS
# -------------------------------------------------------------
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "Internship Evaluation Summary & Future Scope", "CONCLUSION")

box9 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
box9.fill.solid()
box9.fill.fore_color.rgb = LIGHT_BG
box9.line.color.rgb = CARD_BORDER

tb9 = slide9.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.0), Inches(4.8))
tf9 = tb9.text_frame
tf9.word_wrap = True

p9_1 = tf9.paragraphs[0]
p9_1.text = "Key Internship Deliverables & Accomplishments:"
p9_1.font.size = Pt(16)
p9_1.font.bold = True
p9_1.font.color.rgb = NAVY

bullets9 = [
    ("Complete Data Pipeline: ", "Generated and validated multi-table relational schema for 1,250 B2B accounts."),
    ("Validated Machine Learning: ", "Engineered predictive Random Forest model achieving 86.26% accuracy and 0.863 ROC-AUC."),
    ("SaaS-Grade Dashboard: ", "Engineered human-crafted, responsive UI with Chart.js, instant search, and live triage controls."),
    ("Actionable Playbooks: ", "Equipped Customer Success teams with SLA-driven intervention playbooks protecting $61K in MRR."),
    ("Future Enhancements: ", "Real-time Kafka event streaming, bidirectional CRM webhooks, and Kaplan-Meier survival analysis.")
]

for b_bold, b_text in bullets9:
    p = tf9.add_paragraph()
    p.text = f"✓  {b_bold}{b_text}"
    p.font.size = Pt(12)
    p.font.color.rgb = DARK
    p.space_before = Pt(12)

# Save Presentation
prs.save(OUTPUT_PPTX)
print(f"[OK] PowerPoint Presentation successfully created at: {OUTPUT_PPTX}")

if __name__ == "__main__":
    pass
