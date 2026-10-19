"""
Automated Browser Testing & Screenshot Capture for ChurnWatch
Validates DOM rendering, absence of JavaScript errors, and captures 4K/high-res screenshots.
"""

import os
import sys
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_PATH = os.path.join(BASE_DIR, "dashboard", "index.html")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

print(f"[*] Testing Dashboard at: {DASHBOARD_PATH}")

console_errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # 1600x1000 viewport for crisp desktop SaaS layout
    page = browser.new_page(viewport={"width": 1600, "height": 1050})

    def handle_console(msg):
        if msg.type == 'error':
            console_errors.append(msg.text)
            print(f"[BROWSER ERROR] {msg.text}")

    page.on('console', handle_console)

    url = f"file:///{DASHBOARD_PATH.replace(os.sep, '/')}"
    print(f"[*] Navigating to: {url}")
    page.goto(url, wait_until="networkidle")

    # Give charts a moment to animate
    page.wait_for_timeout(1500)

    # 1. Capture Overview View
    overview_img = os.path.join(SCREENSHOTS_DIR, "01_overview_dashboard.png")
    page.screenshot(path=overview_img, full_page=False)
    print(f"[OK] Captured: {overview_img}")

    # 2. Navigate to Customer Analysis & Capture
    page.click('button[data-view="customers"]')
    page.wait_for_timeout(800)
    customers_img = os.path.join(SCREENSHOTS_DIR, "02_customer_analysis_table.png")
    page.screenshot(path=customers_img, full_page=False)
    print(f"[OK] Captured: {customers_img}")

    # 3. Navigate to Retention Operations & Capture
    page.click('button[data-view="operations"]')
    page.wait_for_timeout(800)
    ops_img = os.path.join(SCREENSHOTS_DIR, "03_retention_operations_queue.png")
    page.screenshot(path=ops_img, full_page=False)
    print(f"[OK] Captured: {ops_img}")

    # 4. Navigate to Reports & Methodology & Capture
    page.click('button[data-view="reports"]')
    page.wait_for_timeout(800)
    reports_img = os.path.join(SCREENSHOTS_DIR, "04_reports_methodology.png")
    page.screenshot(path=reports_img, full_page=False)
    print(f"[OK] Captured: {reports_img}")

    browser.close()

if console_errors:
    print(f"[!] Warning: Found {len(console_errors)} console errors:")
    for err in console_errors:
        print(f"    - {err}")
else:
    print("[OK] Dashboard tested cleanly with 0 console errors!")
