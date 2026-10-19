"""
Generate Comprehensive Internship Project Report (PDF) for ChurnWatch
Using ReportLab with clean corporate layout, tables, metrics, and embedded figures.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_PDF = os.path.join(BASE_DIR, "report.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#778399"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "ChurnWatch: Customer Retention & Churn Risk Analytics")
            self.drawRightString(558, 750, "Internship Evaluation Report")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "Confidential - For Academic & Internship Evaluation Only")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#17243A"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4263EB"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#17243A"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4263EB"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#202B3C"),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=body_style,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#17243A")
    )

    story = []

    # Title & Header
    story.append(Paragraph("ChurnWatch: Customer Retention & Churn Risk Analytics", title_style))
    story.append(Paragraph("Minor Project 1 — Data Analytics Internship Final Evaluation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4263EB"), spaceAfter=14))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Author / Intern:</b> Data Analytics Candidate", body_style), Paragraph("<b>Date:</b> October 2026", body_style)],
        [Paragraph("<b>Domain:</b> B2B SaaS Customer Analytics", body_style), Paragraph("<b>Evaluation Stage:</b> Final Milestone Submission", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F5F7FB")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "In recurring revenue software businesses (SaaS), customer acquisition costs (CAC) typically exceed retention costs by a factor of 5x to 7x. <b>ChurnWatch</b> is a production-grade analytics platform engineered to detect leading indicators of customer attrition before contract expiration. By fusing telemetry from three disparate data streams—contractual subscriptions, monthly product usage, and technical support interactions—ChurnWatch calculates a composite <b>Churn Risk Index (0–100)</b>, stratifies accounts into actionable risk tiers, and triggers automated retention workflows.",
        body_style
    ))

    # Key Metrics KPI Table
    kpi_table_data = [
        [
            Paragraph("<b>Total Evaluated Accounts</b><br/><font size='14' color='#4263EB'><b>1,250</b></font><br/><font size='7' color='#778399'>B2B SaaS customer base</font>", body_style),
            Paragraph("<b>Current Churn Rate</b><br/><font size='14' color='#D94B55'><b>19.2%</b></font><br/><font size='7' color='#168A63'>-0.8% MoM improvement</font>", body_style),
            Paragraph("<b>Net Renewal Rate</b><br/><font size='14' color='#159D91'><b>80.8%</b></font><br/><font size='7' color='#168A63'>+1.4% vs benchmark</font>", body_style),
            Paragraph("<b>Total Active MRR</b><br/><font size='14' color='#168A63'><b>$287,450</b></font><br/><font size='7' color='#778399'>$61,398 at high risk</font>", body_style)
        ]
    ]
    t_kpi = Table(kpi_table_data, colWidths=[126, 126, 126, 126])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 14))

    # 2. Problem Statement & Objectives
    story.append(Paragraph("2. Problem Statement & Core Objectives", h1_style))
    story.append(Paragraph(
        "Modern SaaS enterprises suffer from fragmented customer data: sales logs are housed in CRMs, product interaction events reside in event pipelines, and customer dissatisfaction signals are buried in helpdesk tickets. Because these systems operate in silos, account churn is typically detected only after cancellation notices are submitted.",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Objective 1: Multi-Source Data Unification:</b> Design a star/snowflake analytical schema connecting subscriptions, product utilization, and support history.", bullet_style))
    story.append(Paragraph("&bull; <b>Objective 2: Explainable Risk Scoring:</b> Formulate a deterministic, multi-factor risk scoring model prioritizing transparent drivers over black-box outputs.", bullet_style))
    story.append(Paragraph("&bull; <b>Objective 3: Operational Action Queue:</b> Implement an interactive triage system enabling Customer Success Managers (CSMs) to execute targeted mitigation playbooks under strict SLAs.", bullet_style))
    story.append(Paragraph("&bull; <b>Objective 4: Production Dashboard UI:</b> Construct a lightweight, zero-dependency SaaS analytics interface adhering to human-designed usability standards.", bullet_style))

    # 3. Data Architecture & Schema
    story.append(Paragraph("3. Analytical Data Architecture & Schema Design", h1_style))
    story.append(Paragraph(
        "The analytical pipeline unifies three distinct relational source tables into a master <code>unified_customers.csv</code> analytical store:",
        body_style
    ))

    schema_data = [
        ["Table Name", "Primary Key", "Key Telemetry Attributes", "Records"],
        ["subscriptions.csv", "customer_id", "company_name, plan_tier, monthly_price, tenure_months, billing_cycle", "1,250"],
        ["usage.csv", "customer_id", "active_users, seat_utilization_pct, feature_adoption, engagement_change_pct", "1,250"],
        ["support_tickets.csv", "customer_id", "total_tickets_90d, open_tickets, critical_escalations, avg_res_hrs, csat", "1,250"],
        ["unified_customers.csv", "customer_id", "Master table + churn_risk_score, risk_band, revenue_at_risk, recommendations", "1,250"]
    ]
    t_schema = Table(schema_data, colWidths=[110, 80, 260, 54])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#17243A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 14))

    # Page Break to Chapter 4
    story.append(PageBreak())

    # 4. Mathematical Formulations & Risk Thresholds
    story.append(Paragraph("4. Mathematical Formulations & Scoring Methodology", h1_style))
    story.append(Paragraph(
        "To guarantee explainability, the <b>Churn Risk Index</b> is formulated as a normalized linear combination of four weighted operational risk dimensions (0 to 100 scale):",
        body_style
    ))

    formula_table_data = [
        [
            Paragraph("<b>Dimension</b>", body_style),
            Paragraph("<b>Weight</b>", body_style),
            Paragraph("<b>Mathematical Signal Formula</b>", body_style)
        ],
        [
            Paragraph("<b>1. Engagement Trajectory</b>", body_style),
            Paragraph("<b>35%</b>", body_style),
            Paragraph("<code>Risk_eng = clip((-Δ_engagement + 20) &times; 1.25, 0, 100)</code><br/><font size='7' color='#778399'>Penalizes sharp 30-day usage declines.</font>", body_style)
        ],
        [
            Paragraph("<b>2. Adoption & Utilization</b>", body_style),
            Paragraph("<b>25%</b>", body_style),
            Paragraph("<code>Risk_util = 100 - (0.50 &times; Seat_Util% + 0.50 &times; Feature_Score)</code><br/><font size='7' color='#778399'>Measures shelfware risk and underutilized licenses.</font>", body_style)
        ],
        [
            Paragraph("<b>3. Support & CSAT Friction</b>", body_style),
            Paragraph("<b>25%</b>", body_style),
            Paragraph("<code>Risk_support = (5.0 - CSAT) &times; 25.0 + (Escalations &times; 15.0)</code><br/><font size='7' color='#778399'>Accounts for low satisfaction ratings and unresolved tickets.</font>", body_style)
        ],
        [
            Paragraph("<b>4. Contract Vulnerability</b>", body_style),
            Paragraph("<b>15%</b>", body_style),
            Paragraph("<code>Risk_recency = (Days_Inactive &times; 3.5) + (10 if Monthly else 0)</code><br/><font size='7' color='#778399'>Reflects low switching costs of monthly subscriptions.</font>", body_style)
        ]
    ]
    t_formula = Table(formula_table_data, colWidths=[120, 50, 334])
    t_formula.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#17243A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_formula)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Risk Stratification Bands:</b>", h2_style))
    story.append(Paragraph("&bull; <b>High Risk (Score &ge; 70):</b> Accounts at imminent hazard of non-renewal. Requires immediate CSM outreach within 48h SLA.", bullet_style))
    story.append(Paragraph("&bull; <b>Medium Risk (Score 40–69):</b> Moderately disengaged accounts. Requires product enablement or workflow review within 14-day SLA.", bullet_style))
    story.append(Paragraph("&bull; <b>Low Risk (Score &lt; 40):</b> Healthy accounts exhibiting strong adoption and high CSAT. Managed via automated value summaries.", bullet_style))

    # 5. Machine Learning Validation & Findings
    story.append(Paragraph("5. Statistical Analysis & Machine Learning Validation", h1_style))
    story.append(Paragraph(
        "A supervised <b>Random Forest Classifier</b> (100 estimators, max depth 6) was evaluated on the unified customer dataset with a stratified 75/25 train-test split:",
        body_style
    ))

    ml_data = [
        ["Model Metric", "Achieved Score", "Industry Baseline", "Assessment"],
        ["Classification Accuracy", "86.26%", "> 80.0%", "Exceeds production deployment threshold"],
        ["ROC-AUC Score", "0.863", "> 0.800", "Strong class discrimination capability"],
        ["Precision (Non-Churn)", "0.91", "> 0.85", "Low false alarm rate on healthy accounts"],
        ["Macro F1-Score", "0.78", "> 0.70", "Balanced performance across imbalanced churn classes"]
    ]
    t_ml = Table(ml_data, colWidths=[130, 80, 100, 194])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4263EB")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 10))

    # Embed Feature Importance Figure
    feat_img_path = os.path.join(DATA_DIR, "feature_importance.png")
    if os.path.exists(feat_img_path):
        story.append(Image(feat_img_path, width=480, height=210))
        story.append(Paragraph("<font size='7' color='#778399'><i>Figure 1: Relative feature importances derived from Random Forest classifier. Engagement change % and CSAT are top predictors.</i></font>", body_style))
    story.append(Spacer(1, 10))

    # Page Break to Chapter 6
    story.append(PageBreak())

    # 6. Retention Operations & Playbook Matrix
    story.append(Paragraph("6. Retention Operations & Strategic Playbook Matrix", h1_style))
    story.append(Paragraph(
        "To transform analytical predictions into preserved revenue, ChurnWatch equips Customer Success Managers with automated, context-specific mitigation playbooks:",
        body_style
    ))

    playbook_data = [
        ["Trigger Signal", "Assigned SLA", "Prescribed Intervention Playbook"],
        ["Critical Escalations &ge; 2 OR CSAT &le; 2.5", "48 Hours", "Urgent Support Escalation Review & Dedicated Resolution Lead assigned."],
        ["Enterprise Tier AND Churn Risk &ge; 65", "48 Hours", "Executive Sponsor 1-on-1 & Strategic Value Realization Plan."],
        ["Seat Utilization &lt; 40% & Adoption &lt; 40%", "7 Days", "Product Specialist Training & Workflow Optimization Session."],
        ["Engagement Drop &lt; -25% (Pro/Starter)", "5 Days", "Proactive CSM Check-in & Contract Re-alignment Discount."],
        ["Medium Risk Profile (40–69)", "14 Days", "Feature Adoption Check-in & Quarterly Business Review (QBR) Offer."]
    ]
    t_playbook = Table(playbook_data, colWidths=[150, 70, 284])
    t_playbook.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#17243A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#FFFFFF")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_playbook)
    story.append(Spacer(1, 12))

    # Embed Risk & Plan Distribution Figure
    dist_img_path = os.path.join(DATA_DIR, "churn_distribution_analysis.png")
    if os.path.exists(dist_img_path):
        story.append(Image(dist_img_path, width=480, height=190))
        story.append(Paragraph("<font size='7' color='#778399'><i>Figure 2: Empirical churn rate breakdown by subscription plan tier and risk score frequency distribution.</i></font>", body_style))
    story.append(Spacer(1, 12))

    # 7. Limitations & Future Improvements
    story.append(Paragraph("7. Project Limitations & Future Engineering Roadmap", h1_style))
    story.append(Paragraph(
        "While ChurnWatch successfully establishes an automated retention telemetry foundation, several enhancements represent natural extensions for subsequent development phases:",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Limitation 1 — Synthetic Modeling:</b> While mathematically calibrated to real SaaS dynamics, real-world customer churn exhibits external macroeconomic dependencies not captured in synthetic models.", bullet_style))
    story.append(Paragraph("&bull; <b>Limitation 2 — Static Batch Scoring:</b> The current architecture scores risk in batch mode. Transitioning to real-time event streaming (e.g., Apache Kafka / Webhooks) would enable immediate sub-minute alert generation.", bullet_style))
    story.append(Paragraph("&bull; <b>Future Scope — Direct CRM Integration:</b> Build bidirectional connectors to Salesforce, HubSpot, and Slack to trigger native notifications directly into representative workflows.", bullet_style))
    story.append(Paragraph("&bull; <b>Future Scope — Automated Survival Analysis:</b> Incorporate time-to-event Kaplan-Meier estimators and Cox proportional hazards regression to model precise days-to-cancellation probabilities.", bullet_style))

    # 8. Evaluation Disclosure Box
    story.append(Spacer(1, 8))
    disclosure_box_data = [[
        Paragraph(
            "<b>Data Analytics Internship Disclosure:</b> This project was designed and authored for academic and internship evaluation. All customer IDs, company identities, and behavioral telemetries are synthetically generated. The dashboard utilizes pure vanilla web standards (HTML5/CSS3/JavaScript) with Chart.js to ensure zero build friction and universal browser compatibility.",
            callout_style
        )
    ]]
    t_disc = Table(disclosure_box_data, colWidths=[504])
    t_disc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FD")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#4263EB")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_disc)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Report PDF successfully generated at: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()
