# 🚀 ChurnWatch — Customer Retention and Churn Risk Analytics

**📘 Minor Project 1 — Data Analytics Internship Evaluation Submission**  
**🏢 Domain:** B2B SaaS Customer Analytics & Retention Operations

---

## 1. 📊 Project Overview
Repository link : https://github.com/aishpatil1525-creator/chrunwatch1.git
Demo of live link :https://drive.google.com/file/d/1FI0vZGqBCqvpjU1QLs4frkqildDdJpH9/view?usp=sharing

**ChurnWatch** is a production-grade business intelligence and customer retention platform designed for SaaS organizations. By unifying multi-source telemetries—contractual subscriptions, monthly product usage, and technical support interactions—ChurnWatch calculates a multi-dimensional **Churn Risk Index (0–100)** to detect early attrition signals, prioritize high-value revenue exposure, and equip Customer Success Managers (CSMs) with context-specific mitigation playbooks under strict SLAs.

```graphql
ChurnWatch_Submission/
├── 📁 dashboard/
│   ├── 📄 index.html           # Production SaaS dashboard UI (Inter font, responsive, zero-build)
│   ├── 🎨 style.css            # Custom design system: 8px grid, Navy #17243A, Primary #4263EB, Teal #159D91
│   ├── ⚙️ app.js               # Reactive controllers, dynamic filters, Chart.js managers, intervention ops
│   └── 📊 data.js              # Embedded analytical dataset (1,250 accounts) for high-speed offline execution
├── 📁 data/
│   ├── 📄 subscriptions.csv    # Plan tiers (Starter, Pro, Enterprise), MRR, start date, status, renewal date
│   ├── 📄 usage.csv            # Monthly active days, feature adoption scores, seat utilization %
│   ├── 📄 support_tickets.csv  # Escalations, avg resolution time, CSAT ratings, open urgent tickets
│   ├── 📄 unified_customers.csv# Master analytical table with computed risk scores, bands, and MRR
│   ├── 🖼️ feature_importance.png# Matplotlib chart of Random Forest predictive drivers
│   └── 🖼️ churn_distribution_analysis.png# Empirical churn rate by plan tier & score distribution
├── 📁 python/
│   ├── 🐍 churn_analysis.py    # Synthetic dataset generator, feature engineering, and Random Forest model
│   ├── 🐍 generate_report_pdf.py# Automated ReportLab compiler for the multi-page PDF report
│   ├── 🐍 generate_presentation.py# Automated PowerPoint slide deck compiler (python-pptx)
│   └── 🧪 test_and_capture.py  # Playwright headless browser test suite & 4K screenshot generator
├── 📁 sql/
│   └── 🗄️ churn_analysis.sql  # Production CTEs, window functions, cohort retention, and at-risk queues
├── 📁 screenshots/
│   ├── 🖼️ 01_overview_dashboard.png # Executive KPIs, monthly churn trend, risk donut, plan breakdown
│   ├── 🖼️ 02_customer_analysis_table.png # Filterable customer table with search, progress bars, badges
│   ├── 🖼️ 03_retention_operations_queue.png # Triage queue with live owner & status mutation controls
│   └── 🖼️ 04_reports_methodology.png # Embedded report preview & mathematical formulas
├── 📄 README.md                # Complete documentation, setup, and running instructions
├── 📄 requirements.txt         # Minimal Python requirements for reproducible analysis
├── 📄 .gitignore               # Clean repository ignore configuration
├── 📕 report.pdf               # Comprehensive multi-page project report (ReportLab PDF)
└── 📊 presentation.pptx        # 16:9 modern corporate executive slide deck
```

---

## 2. 📈 Key Metrics & Business Impact

| **Metric** | **Value** | **Context & Benchmark** |
|---|---|---|
| 👥 **Total Evaluated Accounts** | **1,250** | Multi-tier B2B customer base |
| 📉 **Active Churn Rate** | **19.2%** | Favorable -0.8% MoM improvement |
| 🔄 **Net Renewal Rate (NRR)** | **80.8%** | +1.4% vs cohort baseline |
| 💰 **Monthly Recurring Revenue (MRR)** | **$287,450** | Portfolio total ($61,398 at high risk) |
| 🤖 **Random Forest Model Accuracy** | **86.26%** | Evaluated on 25% holdout test set |
| 🎯 **Model ROC-AUC Score** | **0.863** | Strong discrimination between churners & retainers |

---

## 3. ⚡ Quick Start & Dashboard Running Instructions

The ChurnWatch dashboard is constructed using **pure vanilla HTML5, CSS3, and JavaScript** with Chart.js loaded via CDN. It requires **no Node.js, npm, webpack, Vite, or external compilation**.

### 🅰️ Option A: Direct Browser Launch (Easiest)

1. 📂 Open your File Explorer.
2. 📁 Navigate to `ChurnWatch_Submission/dashboard/`.
3. 🌐 Double-click `index.html` to open it directly in Chrome, Edge, Firefox, or Safari.

### 🅱️ Option B: Local Python HTTP Server

To run the dashboard as a local web service:

```bash
# 📂 Navigate to the dashboard directory
cd ChurnWatch_Submission/dashboard

# 🚀 Start Python's built-in lightweight HTTP server
python -m http.server 8000
```

Open your browser and navigate to:

```text
http://localhost:8000
```

---

## 4. 🐍 How to Run Python Analytics & Model Training

### 1. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🧠 Execute Data Generation & Churn Analytics

```bash
python python/churn_analysis.py
```

This script will:

- 📊 Generate 1,250 realistic B2B accounts across `subscriptions.csv`, `usage.csv`, and `support_tickets.csv`.
- 🔗 Join and compute the composite Churn Risk Score in `unified_customers.csv`.
- ⚡ Export the optimized client payload into `dashboard/data.js`.
- 🤖 Train a Random Forest classifier and output performance metrics (Accuracy: 86.26%, ROC-AUC: 0.863).
- 📈 Generate high-resolution figures (`feature_importance.png`, `churn_distribution_analysis.png`).

### 3. 🧪 Automated Browser Testing & Screenshot Capture

```bash
python python/test_and_capture.py
```

Tests the dashboard DOM, verifies zero console errors, and captures 4K screenshots of all 4 views into `screenshots/`.

---

## 5. 🧮 Mathematical Formulations

### 1. 📉 Monthly Account Churn Rate

```math
Account Churn Rate = (Accounts Churned in Period / Total Active Accounts at Start of Period) × 100
```

### 2. 🔄 Net Renewal Rate

```math
Renewal Rate = ((Total Accounts at Renewal − Churned Accounts) / Total Accounts at Renewal) × 100
```

### 3. 🎯 Multi-Factor Churn Risk Index (0–100)

The Churn Risk Index is a normalized linear composite of four operational risk dimensions:

**Score = 0.35 ⋅ Rengagement + 0.25 ⋅ Rutilization + 0.25 ⋅ Rsupport + 0.15 ⋅ Rrecency**

- 📉 **Engagement Risk (`Rengagement`):** Penalizes 30-day usage declines below target baselines.
- 🪑 **Utilization Risk (`Rutilization`):** Measures shelfware risk ($100 - (0.5 · SeatUtil% + 0.5 · FeatureScore)$).
- 🎧 **Support Friction (`Rsupport`):** Combines low CSAT (`≤2.5`) and unresolved critical ticket escalations.
- 📅 **Contract Vulnerability (`Rrecency`):** Accounts for inactivity days and monthly vs annual billing flexibility.

---

## 6. 🚦 Risk Stratification & Strategic Playbooks

| **Risk Band** | **Score Range** | **Accounts** | **At-Risk MRR** | **Required SLA** | **Prescribed Playbook** |
|---|---|---:|---:|---|---|
| 🔴 **High Risk** | **`≥70`** | 252 | $61,398 | **48 Hours** | Executive Sponsor 1-on-1 check-in, dedicated resolution lead for support escalations, and strategic contract realignment discount. |
| 🟡 **Medium Risk** | **`40−69`** | 156 | $36,144 | **14 Days** | Product specialist onboarding, feature adoption review, and Quarterly Business Review (QBR) offer. |
| 🟢 **Low Risk** | **`<40`** | 842 | $189,908 | **30 Days** | Automated value realization summaries and healthy milestone check-ins. |

---

## 7. 🌐 Hosting & Deployment Options

The ChurnWatch dashboard is 100% client-side compatible and can be deployed for free within 60 seconds:

- 🚀 **Netlify Drop:** Drag and drop the `ChurnWatch_Submission/dashboard/` folder into [app.netlify.com/drop](https://app.netlify.com/drop) for an instant live HTTPS link.
- 🐙 **GitHub Pages:** Push the repository to GitHub, go to **Settings > Pages**, and set the root/folder to publish.
- ☁️ **Vercel / Cloudflare Pages:** Connect repository for instantaneous static edge hosting.

---

## 8. 🔐 Ethical & Academic Disclosure

In compliance with data privacy ethics and evaluation guidelines:

- 🛡️ **All customer profiles, company names, telemetries, and support logs are synthetically generated.** No real proprietary data or user PII is utilized.
- 📊 All metrics are calculated deterministically from the underlying synthetic tables.
