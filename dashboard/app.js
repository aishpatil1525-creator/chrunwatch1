/**
 * ChurnWatch — SaaS Analytics Dashboard Application Controller
 * Pure vanilla JavaScript with reactive controllers & Chart.js integration
 */

document.addEventListener('DOMContentLoaded', () => {
  // Check if data is loaded
  if (typeof CHURNWATCH_DATA === 'undefined') {
    console.error('CHURNWATCH_DATA is not defined. Ensure data.js is loaded.');
    return;
  }

  // Application State
  const state = {
    currentView: 'overview',
    customers: [...CHURNWATCH_DATA.customers],
    metrics: { ...CHURNWATCH_DATA.metrics },
    searchQuery: '',
    filterPlan: 'ALL',
    filterRisk: 'ALL',
    sortBy: 'risk_desc',
    currentPage: 1,
    pageSize: 15,
    opsOwnerFilter: 'ALL',
    opsStatusFilter: 'ALL',
    charts: {}
  };

  // DOM Elements
  const elements = {
    sidebar: document.getElementById('sidebar'),
    mobileMenuOpen: document.getElementById('mobileMenuOpen'),
    mobileMenuClose: document.getElementById('mobileMenuClose'),
    navItems: document.querySelectorAll('.nav-item'),
    viewPanels: document.querySelectorAll('.view-panel'),
    pageTitle: document.getElementById('pageTitle'),
    pageSubtitle: document.getElementById('pageSubtitle'),
    timeRangeSelect: document.getElementById('timeRangeSelect'),
    quickExportBtn: document.getElementById('quickExportBtn'),
    downloadFullDataBtn: document.getElementById('downloadFullDataBtn'),
    atRiskBadge: document.getElementById('atRiskBadge'),
    toastContainer: document.getElementById('toastContainer'),

    // Customer Table
    customerSearchInput: document.getElementById('customerSearchInput'),
    filterPlanSelect: document.getElementById('filterPlanSelect'),
    filterRiskSelect: document.getElementById('filterRiskSelect'),
    sortSelect: document.getElementById('sortSelect'),
    customersTableBody: document.getElementById('customersTableBody'),
    tableResultsCount: document.getElementById('tableResultsCount'),
    prevPageBtn: document.getElementById('prevPageBtn'),
    nextPageBtn: document.getElementById('nextPageBtn'),
    pageIndicator: document.getElementById('pageIndicator'),

    // Operations
    opsHighRiskCount: document.getElementById('opsHighRiskCount'),
    opsAtRiskMRR: document.getElementById('opsAtRiskMRR'),
    opsPendingSlaCount: document.getElementById('opsPendingSlaCount'),
    opsSavedMRR: document.getElementById('opsSavedMRR'),
    opsOwnerFilter: document.getElementById('opsOwnerFilter'),
    opsStatusFilter: document.getElementById('opsStatusFilter'),
    operationsQueueList: document.getElementById('operationsQueueList'),

    // Customer Modal
    customerModal: document.getElementById('customerModal'),
    modalCustomerName: document.getElementById('modalCustomerName'),
    modalCustomerId: document.getElementById('modalCustomerId'),
    modalCustomerContent: document.getElementById('modalCustomerContent'),
    modalCloseBtn: document.getElementById('modalCloseBtn'),

    // Activity Feed
    activityFeed: document.getElementById('activityFeed'),
    refreshActivityBtn: document.getElementById('refreshActivityBtn')
  };

  // View configuration metadata
  const VIEW_META = {
    overview: {
      title: 'Executive Overview',
      subtitle: 'Key retention metrics, early risk alerts, and churn trajectory across all accounts.'
    },
    customers: {
      title: 'Customer Analysis & Telemetry',
      subtitle: 'Explore granular engagement signals, product usage metrics, and multi-factor churn risk scores.'
    },
    operations: {
      title: 'Retention Operations & Action Queue',
      subtitle: 'Triage high-risk accounts, manage CSM playbooks, and update active intervention statuses.'
    },
    reports: {
      title: 'Methodology, Models & Export',
      subtitle: 'Executive project documentation, KPI formulas, model performance benchmarks, and data exports.'
    }
  };

  // --------------------------------------------------------------------------
  // INITIALIZATION
  // --------------------------------------------------------------------------
  function init() {
    setupNavigation();
    initOverviewMetrics();
    initCharts();
    renderActivityFeed();
    renderCustomerTable();
    renderOperationsQueue();
    updateOperationsStats();
    setupEventListeners();
  }

  // --------------------------------------------------------------------------
  // NAVIGATION & VIEW SWITCHING
  // --------------------------------------------------------------------------
  function setupNavigation() {
    elements.navItems.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetView = btn.getAttribute('data-view');
        switchView(targetView);
      });
    });

    // Mobile drawer toggle
    if (elements.mobileMenuOpen) {
      elements.mobileMenuOpen.addEventListener('click', () => {
        elements.sidebar.classList.add('open');
      });
    }

    if (elements.mobileMenuClose) {
      elements.mobileMenuClose.addEventListener('click', () => {
        elements.sidebar.classList.remove('open');
      });
    }
  }

  function switchView(viewName) {
    state.currentView = viewName;

    // Update active nav item
    elements.navItems.forEach(item => {
      item.classList.toggle('active', item.getAttribute('data-view') === viewName);
    });

    // Update visible view panel
    elements.viewPanels.forEach(panel => {
      panel.classList.toggle('active', panel.id === `view-${viewName}`);
    });

    // Update titles
    if (VIEW_META[viewName]) {
      elements.pageTitle.textContent = VIEW_META[viewName].title;
      elements.pageSubtitle.textContent = VIEW_META[viewName].subtitle;
    }

    // Close mobile menu if open
    elements.sidebar.classList.remove('open');

    // Trigger Chart.js resize if switching to overview
    if (viewName === 'overview') {
      setTimeout(() => {
        Object.values(state.charts).forEach(c => c && c.resize && c.resize());
      }, 50);
    }
  }

  // --------------------------------------------------------------------------
  // KPI METRICS & CHARTS
  // --------------------------------------------------------------------------
  function initOverviewMetrics() {
    const m = state.metrics;
    document.getElementById('kpiTotalCustomers').textContent = m.totalCustomers.toLocaleString();
    document.getElementById('kpiChurnRate').textContent = `${m.churnRate.toFixed(1)}%`;
    document.getElementById('kpiRenewalRate').textContent = `${m.renewalRate.toFixed(1)}%`;
    document.getElementById('kpiMRR').textContent = `$${m.totalMRR.toLocaleString()}`;
    
    // Sidebar alert pill
    elements.atRiskBadge.textContent = m.highRiskCount;
    document.getElementById('overviewHighRiskBadge').textContent = `${m.highRiskCount} High Risk Accounts`;
  }

  function initCharts() {
    // 1. Monthly Churn Trend Chart
    const trendCtx = document.getElementById('monthlyChurnChart');
    if (trendCtx) {
      const trendData = CHURNWATCH_DATA.monthlyChurnTrend;
      state.charts.trend = new Chart(trendCtx.getContext('2d'), {
        type: 'line',
        data: {
          labels: trendData.labels,
          datasets: [
            {
              label: 'Actual Churn Rate (%)',
              data: trendData.churnRates,
              borderColor: '#4263EB',
              backgroundColor: 'rgba(66, 99, 235, 0.08)',
              borderWidth: 2.5,
              tension: 0.35,
              fill: true,
              pointBackgroundColor: '#4263EB',
              pointHoverRadius: 6
            },
            {
              label: 'Target Threshold (5.0%)',
              data: trendData.targetRates,
              borderColor: '#D99020',
              borderWidth: 1.8,
              borderDash: [5, 5],
              tension: 0,
              fill: false,
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#17243A',
              titleFont: { family: 'Inter', size: 12 },
              bodyFont: { family: 'Inter', size: 12 },
              padding: 10,
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y}%`
              }
            }
          },
          scales: {
            y: {
              min: 0,
              max: 10,
              ticks: {
                callback: val => `${val}%`,
                font: { family: 'Inter', size: 11 },
                color: '#778399'
              },
              grid: { color: '#EDF2F7' }
            },
            x: {
              ticks: { font: { family: 'Inter', size: 11 }, color: '#778399' },
              grid: { display: false }
            }
          }
        }
      });
    }

    // 2. Customer Risk Stratification Donut
    const donutCtx = document.getElementById('riskDonutChart');
    if (donutCtx) {
      const riskData = CHURNWATCH_DATA.riskDistribution;
      state.charts.donut = new Chart(donutCtx.getContext('2d'), {
        type: 'doughnut',
        data: {
          labels: riskData.labels,
          datasets: [{
            data: riskData.counts,
            backgroundColor: ['#D94B55', '#D99020', '#168A63'],
            borderWidth: 2,
            borderColor: '#FFFFFF',
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '72%',
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#17243A',
              callbacks: {
                label: ctx => ` ${ctx.label}: ${ctx.raw} accounts (${riskData.percentages[ctx.dataIndex]}%)`
              }
            }
          }
        }
      });

      // Populate Donut Side Legend
      const legendWrap = document.getElementById('riskDonutLegend');
      if (legendWrap) {
        legendWrap.innerHTML = `
          <div class="risk-stat-row high">
            <span class="risk-stat-label">High Risk (>70)</span>
            <span class="risk-stat-val text-danger">${riskData.counts[0]} accounts</span>
            <span class="risk-stat-sub">$${riskData.revenue[0].toLocaleString()} at risk</span>
          </div>
          <div class="risk-stat-row medium">
            <span class="risk-stat-label">Medium Risk (40-70)</span>
            <span class="risk-stat-val text-warning">${riskData.counts[1]} accounts</span>
            <span class="risk-stat-sub">$${riskData.revenue[1].toLocaleString()} MRR</span>
          </div>
          <div class="risk-stat-row low">
            <span class="risk-stat-label">Low Risk (<40)</span>
            <span class="risk-stat-val text-success">${riskData.counts[2]} accounts</span>
            <span class="risk-stat-sub">$${riskData.revenue[2].toLocaleString()} MRR</span>
          </div>
        `;
      }
    }

    // 3. Churn by Plan Tier Bar Chart
    const planCtx = document.getElementById('planChurnChart');
    if (planCtx) {
      const planData = CHURNWATCH_DATA.planBreakdown;
      state.charts.plan = new Chart(planCtx.getContext('2d'), {
        type: 'bar',
        data: {
          labels: planData.plans.map(p => `${p} Plan`),
          datasets: [{
            label: 'Churn Rate (%)',
            data: planData.churnRates,
            backgroundColor: ['#4263EB', '#159D91', '#D94B55'],
            borderRadius: 6,
            barThickness: 38
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#17243A',
              callbacks: {
                label: ctx => ` Churn Rate: ${ctx.raw}% (MRR: $${planData.mrrTotals[ctx.dataIndex].toLocaleString()})`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 30,
              ticks: {
                callback: val => `${val}%`,
                font: { family: 'Inter', size: 11 },
                color: '#778399'
              },
              grid: { color: '#EDF2F7' }
            },
            x: {
              ticks: { font: { family: 'Inter', size: 11 }, color: '#778399' },
              grid: { display: false }
            }
          }
        }
      });
    }
  }

  // --------------------------------------------------------------------------
  // ACTIVITY FEED
  // --------------------------------------------------------------------------
  function renderActivityFeed() {
    if (!elements.activityFeed) return;
    const items = CHURNWATCH_DATA.recentActivity || [];
    elements.activityFeed.innerHTML = items.map(item => `
      <div class="activity-item">
        <div class="activity-icon-dot ${item.type}"></div>
        <div class="activity-content">
          <div class="activity-msg">${escapeHtml(item.message)}</div>
          <div class="activity-time">${item.timestamp}</div>
        </div>
      </div>
    `).join('');
  }

  // --------------------------------------------------------------------------
  // CUSTOMER ANALYSIS TABLE
  // --------------------------------------------------------------------------
  function getFilteredCustomers() {
    return state.customers.filter(c => {
      // Search filter
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        const matchId = c.customer_id.toLowerCase().includes(q);
        const matchName = c.company_name.toLowerCase().includes(q);
        if (!matchId && !matchName) return false;
      }
      // Plan filter
      if (state.filterPlan !== 'ALL' && c.plan_tier !== state.filterPlan) {
        return false;
      }
      // Risk filter
      if (state.filterRisk !== 'ALL' && c.risk_band !== state.filterRisk) {
        return false;
      }
      return true;
    }).sort((a, b) => {
      if (state.sortBy === 'risk_desc') return b.churn_risk_score - a.churn_risk_score;
      if (state.sortBy === 'risk_asc') return a.churn_risk_score - b.churn_risk_score;
      if (state.sortBy === 'mrr_desc') return b.monthly_recurring_revenue - a.monthly_recurring_revenue;
      if (state.sortBy === 'tenure_desc') return b.tenure_months - a.tenure_months;
      if (state.sortBy === 'eng_asc') return a.engagement_change_pct - b.engagement_change_pct;
      return 0;
    });
  }

  function renderCustomerTable() {
    const filtered = getFilteredCustomers();
    const totalRecords = filtered.length;
    const totalPages = Math.max(1, Math.ceil(totalRecords / state.pageSize));

    // Clamp current page
    if (state.currentPage > totalPages) state.currentPage = totalPages;
    if (state.currentPage < 1) state.currentPage = 1;

    const startIdx = (state.currentPage - 1) * state.pageSize;
    const endIdx = Math.min(startIdx + state.pageSize, totalRecords);
    const pageRecords = filtered.slice(startIdx, endIdx);

    // Update pagination UI
    elements.tableResultsCount.textContent = totalRecords === 0 
      ? 'No matching customer accounts found'
      : `Showing ${startIdx + 1}–${endIdx} of ${totalRecords.toLocaleString()} accounts`;
    elements.pageIndicator.textContent = `Page ${state.currentPage} of ${totalPages}`;
    elements.prevPageBtn.disabled = state.currentPage <= 1;
    elements.nextPageBtn.disabled = state.currentPage >= totalPages;

    // Render table rows
    if (pageRecords.length === 0) {
      elements.customersTableBody.innerHTML = `
        <tr>
          <td colspan="9" style="text-align: center; padding: 36px; color: #778399;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 8px; color: #94A3B8;"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/></svg>
            <p>No customer accounts match your current filters.</p>
          </td>
        </tr>
      `;
      return;
    }

    elements.customersTableBody.innerHTML = pageRecords.map(c => {
      // Risk badge class
      const badgeClass = c.risk_band === 'High Risk' ? 'badge-danger' :
                         c.risk_band === 'Medium Risk' ? 'badge-warning' : 'badge-success';

      // Engagement indicator
      const engClass = c.engagement_change_pct < 0 ? 'text-danger' : 'text-success';
      const engSign = c.engagement_change_pct > 0 ? '+' : '';

      // Utilization bar fill
      const utilFillClass = c.seat_utilization_pct < 40 ? 'bg-danger' :
                            c.seat_utilization_pct < 70 ? 'bg-warning' : 'bg-teal';

      return `
        <tr>
          <td>
            <div class="customer-cell">
              <span class="company-name">${escapeHtml(c.company_name)}</span>
              <span class="customer-id">${c.customer_id}</span>
            </div>
          </td>
          <td><span class="badge badge-plan">${c.plan_tier}</span></td>
          <td>${c.tenure_months} mo</td>
          <td>
            <div class="metric-pill-row">
              <div class="progress-bar-wrap" title="Seat Utilization: ${c.seat_utilization_pct}%">
                <div class="progress-fill ${utilFillClass}" style="width: ${c.seat_utilization_pct}%"></div>
              </div>
              <span style="font-size: 0.76rem; font-weight: 500;">${c.seat_utilization_pct}%</span>
              <span class="${engClass}" style="font-size: 0.72rem; margin-left: 4px;">(${engSign}${c.engagement_change_pct}%)</span>
            </div>
          </td>
          <td><strong>$${c.monthly_recurring_revenue}</strong>/mo</td>
          <td>
            <span style="font-weight: 600;">${c.last_csat_score.toFixed(1)}</span>
            ${c.critical_escalations > 0 ? `<span class="badge badge-danger" style="margin-left: 6px;">${c.critical_escalations} esc</span>` : ''}
          </td>
          <td>
            <span style="font-size: 1rem; font-weight: 700;">${c.churn_risk_score}</span><span style="font-size: 0.70rem; color: #94A3B8;">/100</span>
          </td>
          <td><span class="badge ${badgeClass}">${c.risk_band}</span></td>
          <td>
            <button class="btn btn-sm btn-outline view-customer-btn" data-id="${c.customer_id}">
              Inspect
            </button>
          </td>
        </tr>
      `;
    }).join('');

    // Attach inspect listeners
    document.querySelectorAll('.view-customer-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const cid = btn.getAttribute('data-id');
        showCustomerModal(cid);
      });
    });
  }

  // --------------------------------------------------------------------------
  // RETENTION OPERATIONS QUEUE & LIVE CONTROLS
  // --------------------------------------------------------------------------
  function renderOperationsQueue() {
    if (!elements.operationsQueueList) return;

    // Filter queue to High Risk & Medium Risk accounts
    const queueRecords = state.customers.filter(c => {
      if (c.risk_band !== 'High Risk' && c.risk_band !== 'Medium Risk') return false;
      if (state.opsOwnerFilter !== 'ALL' && c.assigned_owner !== state.opsOwnerFilter) return false;
      if (state.opsStatusFilter !== 'ALL' && c.intervention_status !== state.opsStatusFilter) return false;
      return true;
    }).slice(0, 35); // top 35 active operational priorities

    if (queueRecords.length === 0) {
      elements.operationsQueueList.innerHTML = `
        <div style="text-align: center; padding: 48px; color: #778399;">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 8px; color: #168A63;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          <p>No high-risk queue items matching the selected filters.</p>
        </div>
      `;
      return;
    }

    elements.operationsQueueList.innerHTML = queueRecords.map(c => {
      const isHigh = c.risk_band === 'High Risk';
      const scoreColor = isHigh ? 'text-danger' : 'text-warning';

      return `
        <div class="queue-item" id="queue-item-${c.customer_id}">
          <div>
            <div class="queue-company-title">${escapeHtml(c.company_name)}</div>
            <div class="queue-company-sub">${c.customer_id} &bull; ${c.plan_tier} ($${c.monthly_recurring_revenue}/mo)</div>
          </div>

          <div class="queue-score-box">
            <span class="queue-score-number ${scoreColor}">${c.churn_risk_score} <span style="font-size: 0.7rem; color: #778399;">/100</span></span>
            <span class="queue-mrr-at-risk">$${c.monthly_recurring_revenue} MRR Risk</span>
          </div>

          <div class="queue-recommendation">
            <div class="queue-recommendation-title">Recommended Playbook:</div>
            <div>${escapeHtml(c.recommended_action)}</div>
          </div>

          <div class="queue-meta-col">
            <span class="queue-meta-label">Assigned Owner</span>
            <select class="form-select form-select-sm queue-owner-select" data-id="${c.customer_id}" aria-label="Change Owner">
              <option value="Sarah Chen" ${c.assigned_owner === 'Sarah Chen' ? 'selected' : ''}>Sarah Chen</option>
              <option value="Alex Miller" ${c.assigned_owner === 'Alex Miller' ? 'selected' : ''}>Alex Miller</option>
              <option value="David Kim" ${c.assigned_owner === 'David Kim' ? 'selected' : ''}>David Kim</option>
              <option value="Elena Rodriguez" ${c.assigned_owner === 'Elena Rodriguez' ? 'selected' : ''}>Elena Rodriguez</option>
            </select>
          </div>

          <div class="queue-meta-col">
            <span class="queue-meta-label">Intervention Status</span>
            <select class="form-select form-select-sm queue-status-select" data-id="${c.customer_id}" aria-label="Update Status">
              <option value="Pending" ${c.intervention_status === 'Pending' ? 'selected' : ''}>Pending</option>
              <option value="Outreach Initiated" ${c.intervention_status === 'Outreach Initiated' ? 'selected' : ''}>Outreach Initiated</option>
              <option value="Meeting Scheduled" ${c.intervention_status === 'Meeting Scheduled' ? 'selected' : ''}>Meeting Scheduled</option>
              <option value="Offer Extended" ${c.intervention_status === 'Offer Extended' ? 'selected' : ''}>Offer Extended</option>
              <option value="Saved" ${c.intervention_status === 'Saved' ? 'selected' : ''}>Saved</option>
              <option value="Escalated" ${c.intervention_status === 'Escalated' ? 'selected' : ''}>Escalated</option>
            </select>
          </div>

          <div>
            <span class="queue-meta-label" style="display:block; margin-bottom: 2px;">SLA Due</span>
            <span style="font-size: 0.75rem; font-weight: 600; color: ${isHigh ? '#D94B55' : '#202B3C'}">${c.sla_due_date.slice(5)}</span>
          </div>
        </div>
      `;
    }).join('');

    // Attach dynamic listeners for Owner & Status updates
    document.querySelectorAll('.queue-owner-select').forEach(sel => {
      sel.addEventListener('change', (e) => {
        const cid = e.target.getAttribute('data-id');
        const newOwner = e.target.value;
        updateCustomerOwner(cid, newOwner);
      });
    });

    document.querySelectorAll('.queue-status-select').forEach(sel => {
      sel.addEventListener('change', (e) => {
        const cid = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        updateCustomerStatus(cid, newStatus);
      });
    });
  }

  function updateCustomerOwner(customerId, newOwner) {
    const cust = state.customers.find(c => c.customer_id === customerId);
    if (!cust) return;
    cust.assigned_owner = newOwner;
    showToast(`Reassigned ${cust.company_name} to ${newOwner}`);
  }

  function updateCustomerStatus(customerId, newStatus) {
    const cust = state.customers.find(c => c.customer_id === customerId);
    if (!cust) return;
    cust.intervention_status = newStatus;

    if (newStatus === 'Saved') {
      showToast(`Account Saved! $${cust.monthly_recurring_revenue}/mo MRR preserved.`);
    } else {
      showToast(`Updated ${cust.company_name} status to "${newStatus}"`);
    }

    updateOperationsStats();
  }

  function updateOperationsStats() {
    const urgentAccounts = state.customers.filter(c => c.risk_band === 'High Risk' && c.intervention_status !== 'Saved');
    const atRiskMRR = urgentAccounts.reduce((acc, c) => acc + c.monthly_recurring_revenue, 0);
    const savedAccounts = state.customers.filter(c => c.intervention_status === 'Saved');
    const savedMRR = savedAccounts.reduce((acc, c) => acc + c.monthly_recurring_revenue, 0);

    if (elements.opsHighRiskCount) elements.opsHighRiskCount.textContent = urgentAccounts.length;
    if (elements.opsAtRiskMRR) elements.opsAtRiskMRR.textContent = `$${atRiskMRR.toLocaleString()}`;
    if (elements.opsSavedMRR) elements.opsSavedMRR.textContent = `$${savedMRR.toLocaleString()}`;
  }

  // --------------------------------------------------------------------------
  // CUSTOMER INSPECTION MODAL
  // --------------------------------------------------------------------------
  function showCustomerModal(customerId) {
    const c = state.customers.find(item => item.customer_id === customerId);
    if (!c) return;

    elements.modalCustomerName.textContent = c.company_name;
    elements.modalCustomerId.textContent = `${c.customer_id} &bull; ${c.plan_tier} Tier &bull; Assigned to ${c.assigned_owner}`;

    elements.modalCustomerContent.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
        <div style="background: #F8FAFC; padding: 14px; border-radius: 8px; border: 1px solid #E2E8F0;">
          <div style="font-size: 0.72rem; color: #778399; font-weight: 600;">CONTRACT & VALUE</div>
          <div style="font-size: 1.25rem; font-weight: 700; color: #202B3C; margin: 4px 0;">$${c.monthly_recurring_revenue}/mo</div>
          <div style="font-size: 0.76rem; color: #778399;">Tenure: <strong>${c.tenure_months} months</strong> (${c.billing_cycle})</div>
          <div style="font-size: 0.76rem; color: #778399;">Next Renewal: <strong>${c.renewal_date}</strong></div>
        </div>

        <div style="background: #F8FAFC; padding: 14px; border-radius: 8px; border: 1px solid #E2E8F0;">
          <div style="font-size: 0.72rem; color: #778399; font-weight: 600;">CHURN RISK STRATIFICATION</div>
          <div style="font-size: 1.25rem; font-weight: 700; color: ${c.churn_risk_score >= 70 ? '#D94B55' : '#D99020'}; margin: 4px 0;">
            ${c.churn_risk_score} / 100 (${c.risk_band})
          </div>
          <div style="font-size: 0.76rem; color: #778399;">SLA Target: <strong>${c.sla_due_date}</strong></div>
          <div style="font-size: 0.76rem; color: #778399;">Intervention Status: <strong>${c.intervention_status}</strong></div>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <div style="font-size: 0.80rem; font-weight: 700; margin-bottom: 8px;">Telemetry & Usage Health</div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 0.78rem;">
          <div style="background: #FFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px;">
            <span style="color: #778399; display:block;">Active Seats</span>
            <strong>${c.active_users} / ${c.licensed_seats}</strong> (${c.seat_utilization_pct}%)
          </div>
          <div style="background: #FFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px;">
            <span style="color: #778399; display:block;">Engagement Delta</span>
            <strong style="color: ${c.engagement_change_pct < 0 ? '#D94B55' : '#168A63'}">${c.engagement_change_pct}%</strong>
          </div>
          <div style="background: #FFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px;">
            <span style="color: #778399; display:block;">Last Active</span>
            <strong>${c.days_since_last_login} days ago</strong>
          </div>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <div style="font-size: 0.80rem; font-weight: 700; margin-bottom: 8px;">Support & Customer Sentiment</div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 0.78rem;">
          <div style="background: #FFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px;">
            <span style="color: #778399; display:block;">CSAT Score</span>
            <strong>${c.last_csat_score.toFixed(1)} / 5.0</strong>
          </div>
          <div style="background: #FFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px;">
            <span style="color: #778399; display:block;">Critical Escalations</span>
            <strong style="color: ${c.critical_escalations > 0 ? '#D94B55' : '#202B3C'}">${c.critical_escalations}</strong>
          </div>
          <div style="background: #FFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px;">
            <span style="color: #778399; display:block;">NPS Sentiment</span>
            <strong>${c.nps_sentiment}</strong>
          </div>
        </div>
      </div>

      <div style="background: #EEF2FD; border-left: 3px solid #4263EB; padding: 12px 16px; border-radius: 6px; font-size: 0.82rem;">
        <strong style="color: #17243A; display: block; margin-bottom: 4px;">Recommended Retention Strategy:</strong>
        <p style="color: #202B3C; margin: 0;">${escapeHtml(c.recommended_action)}</p>
      </div>
    `;

    elements.customerModal.classList.add('active');
  }

  // --------------------------------------------------------------------------
  // EVENT LISTENERS & FILTERING
  // --------------------------------------------------------------------------
  function setupEventListeners() {
    // Search input
    elements.customerSearchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value.trim();
      state.currentPage = 1;
      renderCustomerTable();
    });

    // Plan Filter
    elements.filterPlanSelect.addEventListener('change', (e) => {
      state.filterPlan = e.target.value;
      state.currentPage = 1;
      renderCustomerTable();
    });

    // Risk Filter
    elements.filterRiskSelect.addEventListener('change', (e) => {
      state.filterRisk = e.target.value;
      state.currentPage = 1;
      renderCustomerTable();
    });

    // Sort Select
    elements.sortSelect.addEventListener('change', (e) => {
      state.sortBy = e.target.value;
      renderCustomerTable();
    });

    // Pagination buttons
    elements.prevPageBtn.addEventListener('click', () => {
      if (state.currentPage > 1) {
        state.currentPage--;
        renderCustomerTable();
      }
    });

    elements.nextPageBtn.addEventListener('click', () => {
      const filtered = getFilteredCustomers();
      const totalPages = Math.ceil(filtered.length / state.pageSize);
      if (state.currentPage < totalPages) {
        state.currentPage++;
        renderCustomerTable();
      }
    });

    // Operations Filters
    elements.opsOwnerFilter.addEventListener('change', (e) => {
      state.opsOwnerFilter = e.target.value;
      renderOperationsQueue();
    });

    elements.opsStatusFilter.addEventListener('change', (e) => {
      state.opsStatusFilter = e.target.value;
      renderOperationsQueue();
    });

    // Modal Close
    elements.modalCloseBtn.addEventListener('click', () => {
      elements.customerModal.classList.remove('active');
    });

    elements.customerModal.addEventListener('click', (e) => {
      if (e.target === elements.customerModal) {
        elements.customerModal.classList.remove('active');
      }
    });

    // Date Range Select
    elements.timeRangeSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      showToast(`Date range switched to: ${e.target.options[e.target.selectedIndex].text}`);
    });

    // Quick Export Button (Exports filtered table)
    elements.quickExportBtn.addEventListener('click', () => {
      exportToCsv(getFilteredCustomers(), 'churnwatch_filtered_customers.csv');
    });

    // Full Master Dataset Export
    if (elements.downloadFullDataBtn) {
      elements.downloadFullDataBtn.addEventListener('click', () => {
        exportToCsv(state.customers, 'churnwatch_master_dataset.csv');
      });
    }

    // Refresh Activity
    if (elements.refreshActivityBtn) {
      elements.refreshActivityBtn.addEventListener('click', () => {
        renderActivityFeed();
        showToast('Activity telemetry refreshed');
      });
    }
  }

  // --------------------------------------------------------------------------
  // CSV EXPORT UTILITY
  // --------------------------------------------------------------------------
  function exportToCsv(dataArray, filename) {
    if (!dataArray || dataArray.length === 0) {
      showToast('No records to export');
      return;
    }

    const headers = [
      'customer_id', 'company_name', 'plan_tier', 'monthly_recurring_revenue',
      'tenure_months', 'seat_utilization_pct', 'engagement_change_pct',
      'last_csat_score', 'critical_escalations', 'churn_risk_score',
      'risk_band', 'recommended_action', 'assigned_owner', 'sla_due_date', 'intervention_status'
    ];

    const csvRows = [];
    csvRows.push(headers.join(','));

    dataArray.forEach(row => {
      const values = headers.map(header => {
        const val = row[header] !== undefined ? row[header] : '';
        const escaped = ('' + val).replace(/"/g, '""');
        return `"${escaped}"`;
      });
      csvRows.push(values.join(','));
    });

    const csvContent = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvRows.join('\n'));
    const link = document.createElement('a');
    link.setAttribute('href', csvContent);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast(`Exported ${dataArray.length} records to ${filename}`);
  }

  // --------------------------------------------------------------------------
  // TOAST NOTIFICATION UTILITY
  // --------------------------------------------------------------------------
  function showToast(message) {
    if (!elements.toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#159D91" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      <span>${escapeHtml(message)}</span>
    `;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Run initial setup
  init();
});
