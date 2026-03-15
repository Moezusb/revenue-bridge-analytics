# 🌲 PROJECT SENTINEL: REVENUE BRIDGE ANALYTICS
**Strategic Risk Framework: Cross-Functional Data Integration for Churn Mitigation**

---

### [ 01. EXECUTIVE SUMMARY ]
In high-growth B2B SaaS, the most dangerous churn is "Silent Churn"—high-value enterprise accounts that stop engaging long before they cancel. This project is a technical demonstration of a **Revenue Bridge**: a system that merges siloed data from Sales (CRM), Support (Service Cloud), and Product (Usage) to quantify revenue at risk in real-time.

### [ 02. THE OPERATIONAL PROBLEM ]
Data silos create a "blind spot" for leadership:
* **CRM (Sales):** Tracks contract value but lacks daily health visibility.
* **SUPPORT (Service):** Manages ticket volume but lacks account-level revenue context.
* **USAGE (Product):** Monitors activity but lacks customer sentiment/billing context.

**Project Sentinel** bridges these gaps by creating a unified **Customer Health Score**.

---

### [ 03. TECHNICAL ARCHITECTURE ]
This repository contains a reproducible three-stage pipeline:

1.  **DATA GENERATION (`data_generator.py`):**
    Simulates a 100-account environment with messy, departmental datasets (CSV) to mirror a real-world tech stack.

2.  **ALGORITHMIC ANALYSIS (`revenue_analysis.py`):**
    A Python/Pandas engine that performs a 3-way SQL-style join and applies a weighted health algorithm:
    * **Engagement (40%):** Login recency.
    * **Sentiment (30%):** AI-scored tone of support tickets.
    * **Adoption (30%):** Feature utilization vs. contract tier.

3.  **STRATEGIC ARTIFACT (`high_priority_risk_report.csv`):**
    The final output. An actionable report for the Executive/Success team to drive retention.

---

### [ 04. SAMPLE OUTPUT: HIGH-PRIORITY INTERVENTION ]
The engine identifies the "Critical Intersection": **High Revenue + Low Health.**
*Total Analyzed: 100 Accounts* | *Total Identified Risk: **$308,121.00***

| Customer | Tier | MRR | Health Score | Strategic Action |
| :--- | :--- | :--- | :--- | :--- |
| **Company 33** | Mid-Market | **$14,863** | 40.8 / 100 | **Immediate Exec Outreach** |
| **Company 64** | Mid-Market | **$14,836** | 32.4 / 100 | **Immediate Exec Outreach** |
| **Company 16** | Mid-Market | $14,138 | 27.0 / 100 | Technical Product Audit |
| **Company 6** | Enterprise | $13,704 | 25.6 / 100 | Success Team Wellness Check |
| **Company 92** | Mid-Market | $13,160 | 38.1 / 100 | Success Team Wellness Check |

---

### [ 05. BUSINESS IMPACT ]
* **Visibility:** Instantly quantifies over **$300k in potential churn risk** that was previously hidden in departmental silos.
* **Efficiency:** Transforms hours of manual cross-referencing between CRM and Usage logs into a 2-second automated report.
* **Proactivity:** Flags accounts like **Company 64** ($14k+ MRR) for intervention based on declining engagement before a cancellation request is ever filed.

---
**Status:** ✅ Functional / Documented  
**Stack:** Python, Pandas, SQL Logic  
**Author:** Mohamed Bah
