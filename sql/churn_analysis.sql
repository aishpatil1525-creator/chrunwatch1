-- ====================================================================
-- PROJECT: ChurnWatch — Customer Retention & Churn Risk Analytics
-- SCRIPT: Production SQL Analytical Pipeline & Cohort Queries
-- DIALECT: ANSI SQL / PostgreSQL / Snowflake Compatible
-- ====================================================================

-- --------------------------------------------------------------------
-- 1. MONTHLY CHURN & RETENTION RATES BY COHORT
-- Computes customer count, churned accounts, and monthly churn rate
-- using window functions and CTEs.
-- --------------------------------------------------------------------
WITH monthly_cohort_base AS (
    SELECT 
        DATE_TRUNC('month', CAST(signup_date AS DATE)) AS cohort_month,
        customer_id,
        plan_tier,
        monthly_recurring_revenue,
        churn_occurred
    FROM unified_customers
),
cohort_aggregations AS (
    SELECT 
        cohort_month,
        plan_tier,
        COUNT(customer_id) AS total_cohort_accounts,
        SUM(monthly_recurring_revenue) AS total_cohort_mrr,
        SUM(CASE WHEN churn_occurred = 1 THEN 1 ELSE 0 END) AS churned_accounts,
        SUM(CASE WHEN churn_occurred = 1 THEN monthly_recurring_revenue ELSE 0 END) AS churned_mrr
    FROM monthly_cohort_base
    GROUP BY cohort_month, plan_tier
)
SELECT 
    cohort_month,
    plan_tier,
    total_cohort_accounts,
    total_cohort_mrr,
    churned_accounts,
    churned_mrr,
    ROUND((churned_accounts * 100.0 / NULLIF(total_cohort_accounts, 0)), 2) AS account_churn_rate_pct,
    ROUND((churned_mrr * 100.0 / NULLIF(total_cohort_mrr, 0)), 2) AS revenue_churn_rate_pct,
    ROUND(((total_cohort_accounts - churned_accounts) * 100.0 / NULLIF(total_cohort_accounts, 0)), 2) AS account_retention_rate_pct
FROM cohort_aggregations
ORDER BY cohort_month DESC, plan_tier;

-- --------------------------------------------------------------------
-- 2. MOM ROLLING CHURN TREND (WINDOW LAG ANALYSIS)
-- Tracks trajectory of churn rate change month-over-month.
-- --------------------------------------------------------------------
WITH monthly_activity AS (
    SELECT 
        DATE_TRUNC('month', CAST(last_active_date AS DATE)) AS activity_month,
        COUNT(customer_id) AS active_accounts,
        SUM(CASE WHEN churn_occurred = 1 THEN 1 ELSE 0 END) AS churned_in_month,
        SUM(monthly_recurring_revenue) AS active_mrr,
        SUM(CASE WHEN churn_occurred = 1 THEN monthly_recurring_revenue ELSE 0 END) AS lost_mrr
    FROM unified_customers
    GROUP BY DATE_TRUNC('month', CAST(last_active_date AS DATE))
)
SELECT 
    activity_month,
    active_accounts,
    churned_in_month,
    ROUND((churned_in_month * 100.0 / NULLIF(active_accounts, 0)), 2) AS monthly_churn_rate_pct,
    LAG(ROUND((churned_in_month * 100.0 / NULLIF(active_accounts, 0)), 2), 1) OVER (ORDER BY activity_month) AS prev_month_churn_rate,
    ROUND(
        (churned_in_month * 100.0 / NULLIF(active_accounts, 0)) - 
        LAG(ROUND((churned_in_month * 100.0 / NULLIF(active_accounts, 0)), 2), 1) OVER (ORDER BY activity_month), 
        2
    ) AS churn_rate_mom_delta_pct,
    lost_mrr,
    SUM(lost_mrr) OVER (ORDER BY activity_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_mrr_lost
FROM monthly_activity
ORDER BY activity_month ASC;

-- --------------------------------------------------------------------
-- 3. CHURN RISK STRATIFICATION & REVENUE EXPOSURE
-- Segmenting customers into High, Medium, and Low risk bands with
-- aggregate MRR exposure and average product engagement.
-- --------------------------------------------------------------------
SELECT 
    CASE 
        WHEN churn_risk_score >= 70 THEN 'High Risk (>70)'
        WHEN churn_risk_score >= 40 THEN 'Medium Risk (40-70)'
        ELSE 'Low Risk (<40)'
    END AS risk_tier,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM unified_customers), 1) AS customer_share_pct,
    SUM(monthly_recurring_revenue) AS total_mrr_in_tier,
    ROUND(AVG(seat_utilization_pct), 1) AS avg_seat_utilization_pct,
    ROUND(AVG(feature_adoption_score), 1) AS avg_feature_adoption_score,
    ROUND(AVG(engagement_change_pct), 1) AS avg_engagement_change_pct,
    ROUND(AVG(last_csat_score), 2) AS avg_csat_score,
    SUM(critical_escalations) AS total_critical_escalations
FROM unified_customers
GROUP BY 
    CASE 
        WHEN churn_risk_score >= 70 THEN 'High Risk (>70)'
        WHEN churn_risk_score >= 40 THEN 'Medium Risk (40-70)'
        ELSE 'Low Risk (<40)'
    END
ORDER BY MIN(churn_risk_score) DESC;

-- --------------------------------------------------------------------
-- 4. CUSTOMER SUCCESS MANAGER (CSM) WORKLOAD & RETENTION QUEUE
-- Evaluates portfolio risk, intervention distribution, and SLA adherence
-- across CSM team members.
-- --------------------------------------------------------------------
SELECT 
    assigned_owner AS csm_name,
    COUNT(customer_id) AS total_assigned_accounts,
    SUM(CASE WHEN risk_band = 'High Risk' THEN 1 ELSE 0 END) AS high_risk_accounts,
    SUM(CASE WHEN risk_band = 'Medium Risk' THEN 1 ELSE 0 END) AS medium_risk_accounts,
    SUM(CASE WHEN risk_band = 'High Risk' THEN monthly_recurring_revenue ELSE 0 END) AS high_risk_mrr_exposure,
    SUM(CASE WHEN intervention_status = 'Saved' THEN 1 ELSE 0 END) AS successfully_saved_accounts,
    SUM(CASE WHEN intervention_status IN ('Pending', 'Outreach Initiated') THEN 1 ELSE 0 END) AS active_interventions_pending,
    ROUND(
        SUM(CASE WHEN intervention_status = 'Saved' THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN risk_band IN ('High Risk', 'Medium Risk') THEN 1 ELSE 0 END), 0),
        1
    ) AS intervention_save_rate_pct
FROM unified_customers
GROUP BY assigned_owner
ORDER BY high_risk_mrr_exposure DESC;

-- --------------------------------------------------------------------
-- 5. AT-RISK ACTION QUEUE (PRIORITIZED FOR CSM RETENTION OUTREACH)
-- Ranked by Risk Score and MRR to maximize revenue preservation.
-- --------------------------------------------------------------------
SELECT 
    customer_id,
    company_name,
    plan_tier,
    monthly_recurring_revenue,
    tenure_months,
    churn_risk_score,
    risk_band,
    engagement_change_pct,
    seat_utilization_pct,
    last_csat_score,
    critical_escalations,
    recommended_action,
    assigned_owner,
    sla_due_date,
    intervention_status
FROM unified_customers
WHERE risk_band IN ('High Risk', 'Medium Risk')
  AND intervention_status != 'Saved'
ORDER BY 
    churn_risk_score DESC, 
    monthly_recurring_revenue DESC
LIMIT 50;
