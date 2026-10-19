"""
ChurnWatch: Customer Retention and Churn Risk Analytics
Comprehensive Python Data Analytics & Synthetic Dataset Engine
"""

import os
import json
import random
import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

for directory in [DATA_DIR, DASHBOARD_DIR, SCREENSHOTS_DIR]:
    os.makedirs(directory, exist_ok=True)

print(f"[*] Base directory: {BASE_DIR}")
print("[*] Generating synthetic multi-table datasets for 1,250 B2B SaaS accounts...")

# -------------------------------------------------------------
# 1. SUBSCRIPTIONS TABLE GENERATION
# -------------------------------------------------------------
COMPANY_PREFIXES = ["Apex", "Vertex", "Nimbus", "Vanguard", "Pulse", "Quantum", "Synergy", "Beacon", "Crest", "Horizon", 
                    "Zenith", "Nova", "Starlight", "Hyperion", "Cobalt", "Onyx", "Optima", "Aegis", "Solstice", "Prism",
                    "Acuity", "Elevate", "Velocity", "Aether", "Omni", "Strata", "Nexus", "Infinitum", "Klarity", "Luminary"]
COMPANY_SUFFIXES = ["Technologies", "Analytics", "Solutions", "Labs", "Systems", "Media", "Digital", "Logistics", 
                    "Health", "Financial", "Interactive", "Networks", "Cloud", "Dynamics", "Software", "Security"]

PLANS = [
    {"name": "Starter", "price": 49, "weight": 0.45, "seats": (3, 10)},
    {"name": "Professional", "price": 199, "weight": 0.40, "seats": (10, 50)},
    {"name": "Enterprise", "price": 799, "weight": 0.15, "seats": (50, 300)}
]

OWNERS = ["Sarah Chen", "Alex Miller", "David Kim", "Elena Rodriguez"]

num_customers = 1250
customer_ids = [f"CW-{1000 + i}" for i in range(num_customers)]

companies = []
for cid in customer_ids:
    name = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)}"
    companies.append(name)

# Distribute plans
plan_choices = np.random.choice([p["name"] for p in PLANS], size=num_customers, p=[p["weight"] for p in PLANS])

subscriptions = []
start_date_base = datetime.date(2024, 1, 1)

for i in range(num_customers):
    cid = customer_ids[i]
    company = companies[i]
    plan_name = plan_choices[i]
    plan_meta = next(p for p in PLANS if p["name"] == plan_name)
    monthly_price = plan_meta["price"]
    
    # Tenure between 1 and 30 months
    tenure_months = int(np.clip(np.random.gamma(shape=3.0, scale=4.0), 1, 30))
    signup_date = datetime.date(2026, 10, 1) - datetime.timedelta(days=int(tenure_months * 30.4))
    billing_cycle = np.random.choice(["Monthly", "Annual"], p=[0.65, 0.35])
    
    # Renewal date in next 1 to 90 days
    days_to_renewal = random.randint(3, 90)
    renewal_date = datetime.date(2026, 10, 19) + datetime.timedelta(days=days_to_renewal)
    
    # Seats
    min_s, max_s = plan_meta["seats"]
    licensed_seats = random.randint(min_s, max_s)
    
    subscriptions.append({
        "customer_id": cid,
        "company_name": company,
        "plan_tier": plan_name,
        "monthly_recurring_revenue": monthly_price,
        "tenure_months": tenure_months,
        "signup_date": signup_date.isoformat(),
        "renewal_date": renewal_date.isoformat(),
        "billing_cycle": billing_cycle,
        "licensed_seats": licensed_seats,
        "assigned_owner": random.choice(OWNERS)
    })

df_subs = pd.DataFrame(subscriptions)

# -------------------------------------------------------------
# 2. USAGE METRICS GENERATION
# -------------------------------------------------------------
usage_data = []
for i, sub in enumerate(subscriptions):
    cid = sub["customer_id"]
    seats = sub["licensed_seats"]
    
    # Correlate usage: some accounts are healthy, some are declining
    is_at_risk_propensity = (i % 5 == 0) or (random.random() < 0.15)
    
    if is_at_risk_propensity:
        utilization = np.clip(np.random.normal(0.35, 0.15), 0.05, 0.70)
        active_days = int(np.clip(np.random.normal(7, 4), 1, 18))
        feature_adoption = int(np.clip(np.random.normal(32, 15), 10, 60))
        engagement_change_pct = round(float(np.clip(np.random.normal(-32, 15), -75, -5)), 1)
        login_trend = "Declining"
        days_since_active = random.randint(5, 28)
    else:
        utilization = np.clip(np.random.normal(0.82, 0.12), 0.40, 1.0)
        active_days = int(np.clip(np.random.normal(23, 4), 14, 30))
        feature_adoption = int(np.clip(np.random.normal(78, 14), 45, 98))
        engagement_change_pct = round(float(np.clip(np.random.normal(8, 12), -10, 48)), 1)
        login_trend = np.random.choice(["Increasing", "Stable"], p=[0.45, 0.55])
        days_since_active = random.randint(0, 4)

    active_users = max(1, int(round(seats * utilization)))
    last_active_date = datetime.date(2026, 10, 19) - datetime.timedelta(days=days_since_active)
    
    usage_data.append({
        "customer_id": cid,
        "active_users": active_users,
        "seat_utilization_pct": round(float(utilization * 100), 1),
        "monthly_active_days": active_days,
        "feature_adoption_score": feature_adoption,
        "engagement_change_pct": engagement_change_pct,
        "login_frequency_trend": login_trend,
        "last_active_date": last_active_date.isoformat(),
        "days_since_last_login": days_since_active
    })

df_usage = pd.DataFrame(usage_data)

# -------------------------------------------------------------
# 3. SUPPORT TICKETS GENERATION
# -------------------------------------------------------------
tickets_data = []
for i, sub in enumerate(subscriptions):
    cid = sub["customer_id"]
    u = usage_data[i]
    is_struggling = (u["engagement_change_pct"] < -15) or (u["seat_utilization_pct"] < 40)
    
    if is_struggling:
        total_tickets = int(np.clip(np.random.poisson(lam=5.5), 1, 15))
        escalations = int(np.clip(np.random.binomial(n=total_tickets, p=0.4), 0, 4))
        avg_res_hours = round(float(np.clip(np.random.normal(38.0, 12.0), 12.0, 72.0)), 1)
        csat = round(float(np.clip(np.random.normal(2.4, 0.7), 1.0, 3.8)), 1)
        open_tickets = random.randint(1, 4)
        nps_sentiment = np.random.choice(["Detractor", "Passive"], p=[0.75, 0.25])
    else:
        total_tickets = int(np.clip(np.random.poisson(lam=1.8), 0, 8))
        escalations = 0 if random.random() > 0.1 else 1
        avg_res_hours = round(float(np.clip(np.random.normal(14.0, 6.0), 2.0, 32.0)), 1)
        csat = round(float(np.clip(np.random.normal(4.6, 0.4), 3.5, 5.0)), 1)
        open_tickets = 0 if random.random() > 0.3 else 1
        nps_sentiment = np.random.choice(["Promoter", "Passive"], p=[0.80, 0.20])

    tickets_data.append({
        "customer_id": cid,
        "total_tickets_last_90d": total_tickets,
        "open_tickets": open_tickets,
        "critical_escalations": escalations,
        "avg_resolution_hours": avg_res_hours,
        "last_csat_score": csat,
        "nps_sentiment": nps_sentiment
    })

df_tickets = pd.DataFrame(tickets_data)

# Save the 3 individual relational CSVs
df_subs.to_csv(os.path.join(DATA_DIR, "subscriptions.csv"), index=False)
df_usage.to_csv(os.path.join(DATA_DIR, "usage.csv"), index=False)
df_tickets.to_csv(os.path.join(DATA_DIR, "support_tickets.csv"), index=False)

print("[OK] Saved subscriptions.csv, usage.csv, support_tickets.csv")

# -------------------------------------------------------------
# 4. UNIFIED ANALYTICAL MASTER DATASET & CHURN RISK SCORING
# -------------------------------------------------------------
# Join all 3 tables
df_master = df_subs.merge(df_usage, on="customer_id").merge(df_tickets, on="customer_id")

# Comprehensive Multi-factor Risk Scoring Algorithm (0-100 scale):
# Factor 1: Engagement Trend (weight 35%)
# Factor 2: Feature Adoption & Seat Utilization (weight 25%)
# Factor 3: Support Friction & Escalations (weight 25%)
# Factor 4: Recency of Login & Billing Cycle (weight 15%)

def compute_risk_score(row):
    eng_risk = np.clip((-(row["engagement_change_pct"]) + 20) * 1.25, 0, 100)
    util_risk = 100 - (row["seat_utilization_pct"] * 0.5 + row["feature_adoption_score"] * 0.5)
    util_risk = np.clip(util_risk, 0, 100)
    csat_risk = (5.0 - row["last_csat_score"]) * 25.0
    escalation_penalty = row["critical_escalations"] * 15.0
    support_risk = np.clip(csat_risk + escalation_penalty, 0, 100)
    recency_risk = np.clip(row["days_since_last_login"] * 3.5, 0, 100)
    if row["billing_cycle"] == "Monthly":
        recency_risk = min(100, recency_risk + 10)
        
    score = (eng_risk * 0.35) + (util_risk * 0.25) + (support_risk * 0.25) + (recency_risk * 0.15)
    return int(round(np.clip(score, 5, 98)))

df_master["churn_risk_score"] = df_master.apply(compute_risk_score, axis=1)

def assign_risk_band(score):
    if score >= 70:
        return "High Risk"
    elif score >= 40:
        return "Medium Risk"
    else:
        return "Low Risk"

df_master["risk_band"] = df_master["churn_risk_score"].apply(assign_risk_band)

df_master["revenue_at_risk"] = df_master.apply(
    lambda r: r["monthly_recurring_revenue"] if r["risk_band"] in ["High Risk", "Medium Risk"] else 0,
    axis=1
)

def determine_recommendation(row):
    if row["critical_escalations"] >= 2 or (row["last_csat_score"] <= 2.5 and row["open_tickets"] > 0):
        return "Urgent Support Escalation Review & Dedicated Resolution Lead"
    elif row["plan_tier"] == "Enterprise" and row["churn_risk_score"] >= 65:
        return "Executive Sponsor 1-on-1 & Strategic Value Realization Plan"
    elif row["seat_utilization_pct"] < 40 and row["feature_adoption_score"] < 40:
        return "Product Specialist Training & Workflow Optimization Session"
    elif row["engagement_change_pct"] < -25:
        return "Proactive CSM Check-in & Contract Re-alignment Discount"
    elif row["risk_band"] == "Medium Risk":
        return "Feature Adoption Check-in & Quarterly Business Review Offer"
    else:
        return "Standard Account Health Monitor & Automated Value Summary"

df_master["recommended_action"] = df_master.apply(determine_recommendation, axis=1)

def assign_sla(row):
    if row["risk_band"] == "High Risk":
        days = random.randint(2, 6)
    elif row["risk_band"] == "Medium Risk":
        days = random.randint(7, 14)
    else:
        days = random.randint(20, 35)
    return (datetime.date(2026, 10, 19) + datetime.timedelta(days=days)).isoformat()

df_master["sla_due_date"] = df_master.apply(assign_sla, axis=1)

INTERVENTION_STATUSES = ["Pending", "Outreach Initiated", "Meeting Scheduled", "Offer Extended", "Saved", "Escalated"]
def assign_intervention_status(row):
    if row["risk_band"] == "High Risk":
        return np.random.choice(INTERVENTION_STATUSES, p=[0.35, 0.30, 0.15, 0.10, 0.05, 0.05])
    elif row["risk_band"] == "Medium Risk":
        return np.random.choice(["Pending", "Outreach Initiated", "Saved"], p=[0.60, 0.25, 0.15])
    else:
        return "Monitoring"

df_master["intervention_status"] = df_master.apply(assign_intervention_status, axis=1)

df_master["churn_occurred"] = df_master["churn_risk_score"].apply(
    lambda s: 1 if (s > 75 and random.random() < 0.82) or (s > 50 and random.random() < 0.35) or (random.random() < 0.03) else 0
)

df_master.to_csv(os.path.join(DATA_DIR, "unified_customers.csv"), index=False)
print("[OK] Saved unified_customers.csv with 1,250 analytical customer records.")

# -------------------------------------------------------------
# 5. DATASET SUMMARY & METRICS COMPUTATION FOR DASHBOARD
# -------------------------------------------------------------
total_customers = len(df_master)
active_customers = len(df_master[df_master["churn_occurred"] == 0])
total_churned = int(df_master["churn_occurred"].sum())
overall_churn_rate = round((total_churned / total_customers) * 100, 1)
overall_renewal_rate = round(100.0 - overall_churn_rate, 1)
total_mrr = int(df_master["monthly_recurring_revenue"].sum())
at_risk_mrr = int(df_master[df_master["risk_band"] == "High Risk"]["monthly_recurring_revenue"].sum())

high_risk_count = int(len(df_master[df_master["risk_band"] == "High Risk"]))
med_risk_count = int(len(df_master[df_master["risk_band"] == "Medium Risk"]))
low_risk_count = int(len(df_master[df_master["risk_band"] == "Low Risk"]))

print("\n--- Summary Metrics ---")
print(f"Total Accounts: {total_customers}")
print(f"Total MRR: ${total_mrr:,.2f}")
print(f"Active Churn Rate: {overall_churn_rate}%")
print(f"Renewal Rate: {overall_renewal_rate}%")
print(f"High Risk Accounts: {high_risk_count} (${at_risk_mrr:,.2f} MRR at risk)")
print(f"Medium Risk Accounts: {med_risk_count}")
print(f"Low Risk Accounts: {low_risk_count}")

# -------------------------------------------------------------
# 6. EXPORT CLEAN JAVASCRIPT PAYLOAD FOR DASHBOARD (data.js)
# -------------------------------------------------------------
queue_records = df_master.sort_values(by=["churn_risk_score", "monthly_recurring_revenue"], ascending=[False, False])

js_data = {
    "generatedAt": "2026-10-19T17:30:00Z",
    "metrics": {
        "totalCustomers": total_customers,
        "activeCustomers": active_customers,
        "churnRate": overall_churn_rate,
        "churnRateDelta": -0.8,
        "renewalRate": overall_renewal_rate,
        "renewalRateDelta": 1.4,
        "totalMRR": total_mrr,
        "mrrDelta": 4.6,
        "highRiskCount": high_risk_count,
        "mediumRiskCount": med_risk_count,
        "lowRiskCount": low_risk_count,
        "atRiskMRR": at_risk_mrr
    },
    "monthlyChurnTrend": {
        "labels": ["Nov 25", "Dec 25", "Jan 26", "Feb 26", "Mar 26", "Apr 26", "May 26", "Jun 26", "Jul 26", "Aug 26", "Sep 26", "Oct 26"],
        "churnRates": [7.4, 7.1, 6.8, 6.9, 6.5, 6.2, 5.9, 5.7, 5.4, 5.1, 4.8, 4.3],
        "targetRates": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        "mrrLost": [14200, 13800, 13100, 13500, 12400, 11800, 11200, 10900, 10400, 9800, 9200, 8400]
    },
    "planBreakdown": {
        "plans": ["Starter", "Professional", "Enterprise"],
        "customerCounts": [
            int(len(df_master[df_master["plan_tier"] == "Starter"])),
            int(len(df_master[df_master["plan_tier"] == "Professional"])),
            int(len(df_master[df_master["plan_tier"] == "Enterprise"]))
        ],
        "churnRates": [
            round(float(df_master[df_master["plan_tier"] == "Starter"]["churn_occurred"].mean() * 100), 1),
            round(float(df_master[df_master["plan_tier"] == "Professional"]["churn_occurred"].mean() * 100), 1),
            round(float(df_master[df_master["plan_tier"] == "Enterprise"]["churn_occurred"].mean() * 100), 1)
        ],
        "mrrTotals": [
            int(df_master[df_master["plan_tier"] == "Starter"]["monthly_recurring_revenue"].sum()),
            int(df_master[df_master["plan_tier"] == "Professional"]["monthly_recurring_revenue"].sum()),
            int(df_master[df_master["plan_tier"] == "Enterprise"]["monthly_recurring_revenue"].sum())
        ]
    },
    "riskDistribution": {
        "labels": ["High Risk (>70)", "Medium Risk (40-70)", "Low Risk (<40)"],
        "counts": [high_risk_count, med_risk_count, low_risk_count],
        "percentages": [
            round((high_risk_count / total_customers) * 100, 1),
            round((med_risk_count / total_customers) * 100, 1),
            round((low_risk_count / total_customers) * 100, 1)
        ],
        "revenue": [
            at_risk_mrr,
            int(df_master[df_master["risk_band"] == "Medium Risk"]["monthly_recurring_revenue"].sum()),
            int(df_master[df_master["risk_band"] == "Low Risk"]["monthly_recurring_revenue"].sum())
        ]
    },
    "recentActivity": [
        {"timestamp": "12 mins ago", "type": "critical", "message": "High Churn Risk alert triggered for Apex Systems (Enterprise, $799/mo) — Engagement dropped 42%."},
        {"timestamp": "45 mins ago", "type": "saved", "message": "Elena Rodriguez marked Vanguard Health (Pro, $199/mo) as SAVED after executive discount intervention."},
        {"timestamp": "2 hrs ago", "type": "warning", "message": "CSAT dropped to 1.8 for Nimbus Technologies — 3 open urgent tickets pending review."},
        {"timestamp": "4 hrs ago", "type": "info", "message": "Monthly Retention Report generated: Net Churn Rate improved by 0.8% MoM."},
        {"timestamp": "6 hrs ago", "type": "saved", "message": "David Kim initiated retention playbook for Zenith Solutions — SLA target set for 48h."}
    ],
    "customers": queue_records.to_dict(orient="records")
}

js_content = f"// ChurnWatch Master Analytical Dataset\n// Generated dynamically for production client dashboard\n\nconst CHURNWATCH_DATA = {json.dumps(js_data, indent=2)};\n\nif (typeof module !== 'undefined') module.exports = CHURNWATCH_DATA;\n"

with open(os.path.join(DASHBOARD_DIR, "data.js"), "w", encoding="utf-8") as f:
    f.write(js_content)

print("[OK] Successfully wrote dashboard/data.js with complete client data payload.")

# -------------------------------------------------------------
# 7. PYTHON MACHINE LEARNING & STATISTICAL EDA
# -------------------------------------------------------------
print("\n[*] Training Random Forest Churn Classifier for feature importance analysis...")

feature_cols = [
    "monthly_recurring_revenue", "tenure_months", "licensed_seats",
    "active_users", "seat_utilization_pct", "monthly_active_days",
    "feature_adoption_score", "engagement_change_pct", "days_since_last_login",
    "total_tickets_last_90d", "open_tickets", "critical_escalations",
    "avg_resolution_hours", "last_csat_score"
]

X = df_master[feature_cols]
y = df_master["churn_occurred"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

rf_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
roc = roc_auc_score(y_test, y_prob)

print(f"[OK] Model Accuracy: {acc * 100:.2f}%")
print(f"[OK] Model ROC-AUC Score: {roc:.3f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

importances = rf_model.feature_importances_
feat_df = pd.DataFrame({"Feature": feature_cols, "Importance": importances}).sort_values("Importance", ascending=False)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
colors = ['#4263EB' if i < 3 else '#159D91' if i < 6 else '#778399' for i in range(len(feat_df))]
sns.barplot(data=feat_df.head(8), x="Importance", y="Feature", palette=colors, ax=ax)
ax.set_title("Key Drivers of SaaS Customer Churn (Random Forest Importance)", fontsize=13, fontweight='bold', color='#17243A', pad=12)
ax.set_xlabel("Relative Predictive Importance", fontsize=10, fontweight='bold', color='#202B3C')
ax.set_ylabel("", fontsize=10)
plt.tight_layout()
feat_chart_path = os.path.join(DATA_DIR, "feature_importance.png")
plt.savefig(feat_chart_path)
plt.close()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=300)

plan_churn_s = df_master.groupby("plan_tier")["churn_occurred"].mean() * 100
ax1.bar(plan_churn_s.index, plan_churn_s.values, color=['#4263EB', '#159D91', '#D94B55'], width=0.55)
ax1.set_title("Churn Rate by Plan Tier (%)", fontsize=11, fontweight='bold', color='#17243A')
ax1.set_ylabel("Churn Rate (%)", fontsize=9)
for idx, val in enumerate(plan_churn_s.values):
    ax1.text(idx, val + 0.3, f"{val:.1f}%", ha='center', fontweight='bold', fontsize=9)

sns.histplot(df_master["churn_risk_score"], bins=20, kde=True, color='#4263EB', ax=ax2)
ax2.axvline(70, color='#D94B55', linestyle='--', label='High Risk Threshold (70)')
ax2.axvline(40, color='#D99020', linestyle='--', label='Medium Risk Threshold (40)')
ax2.set_title("Customer Risk Score Distribution", fontsize=11, fontweight='bold', color='#17243A')
ax2.set_xlabel("Computed Risk Score (0-100)", fontsize=9)
ax2.legend(fontsize=8)

plt.tight_layout()
dist_chart_path = os.path.join(DATA_DIR, "churn_distribution_analysis.png")
plt.savefig(dist_chart_path)
plt.close()

print(f"[OK] Generated analytical charts: {feat_chart_path}, {dist_chart_path}")
print("[OK] Python churn analytics engine completed successfully.")
