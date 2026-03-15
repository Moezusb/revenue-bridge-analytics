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

| Customer | Tier | MRR | Health Score | Strategic Action |
| :--- | :--- | :--- | :--- | :--- |
| **Company 42** | Enterprise | **$14,500** | 32 / 100 | **Exec-Level Intervention** |
| **Company 12** | Enterprise | **$12,000** | 41 / 100 | CSM Wellness Check |
| **Company 88** | Mid-Market | $8,500 | 28 / 100 | Technical Product Audit |

---

### [ 05. BUSINESS IMPACT ]
* **Visibility:** Transforms 3+ hours of manual data-pulling into a 2-second automated report.
* **Proactivity:** Identifies "Silent Churn" risks 60-90 days before the renewal date.
* **Scalability:** The logic is vendor-agnostic and can be deployed across Salesforce, HubSpot, or Snowflake.

---
**Status:** ✅ Functional / Documented  
**Stack:** Python, Pandas, SQL Logic  
**Author:** Mohamed Bah
