"""
revenue_analysis.py
===================
Performs a three-way SQL-style join across CRM, Support, and Product Usage
datasets, computes a weighted Customer Health Score per account, and outputs
a prioritized intervention list for CS and executive teams.

Run data_generator.py first to generate the input datasets.

Author : Mohamed Bah
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

# ─────────────────────────────────────────────
# LOAD DATASETS
# ─────────────────────────────────────────────

crm     = pd.read_csv("data/crm_data.csv")
support = pd.read_csv("data/support_data.csv")
usage   = pd.read_csv("data/usage_data.csv")

print("Datasets loaded.")
print(f"  CRM:     {len(crm)} accounts")
print(f"  Support: {len(support)} accounts")
print(f"  Usage:   {len(usage)} accounts")

# ─────────────────────────────────────────────
# THREE-WAY JOIN
# ─────────────────────────────────────────────

df = pd.merge(crm, support, on="account_id", how="left")
df = pd.merge(df, usage,   on="account_id", how="left")

# ─────────────────────────────────────────────
# HEALTH SCORE CALCULATION
#
# Weighted algorithm:
#   Engagement (40%) -- login recency
#   Sentiment  (30%) -- support ticket tone
#   Adoption   (30%) -- feature utilization
# ─────────────────────────────────────────────

def calculate_health(row):
    # Engagement: fewer days since login = higher score
    engagement = max(0, 100 - (row["days_since_login"] * 1.1))

    # Sentiment: already on 0-100 scale from data generator
    sentiment = row["sentiment_score"]

    # Adoption: already on 0-100 scale from data generator
    adoption = row["adoption_rate_pct"]

    return round(
        (engagement * 0.40) +
        (sentiment  * 0.30) +
        (adoption   * 0.30),
        1
    )

df["health_score"] = df.apply(calculate_health, axis=1)

# ─────────────────────────────────────────────
# RISK CLASSIFICATION
# ─────────────────────────────────────────────

def classify_risk(health):
    if health < 40:
        return "Critical"
    elif health < 60:
        return "At Risk"
    elif health < 75:
        return "Watch"
    else:
        return "Healthy"

df["risk_level"] = df["health_score"].apply(classify_risk)

# ─────────────────────────────────────────────
# STRATEGIC ACTION RECOMMENDATION
# ─────────────────────────────────────────────

def recommend_action(row):
    if row["risk_level"] == "Critical" and row["tier"] == "Enterprise":
        return "Immediate Executive Outreach"
    elif row["risk_level"] == "Critical":
        return "Immediate CS Outreach"
    elif row["risk_level"] == "At Risk" and row["has_open_escalation"]:
        return "Technical Product Audit"
    elif row["risk_level"] == "At Risk":
        return "Success Team Wellness Check"
    elif row["risk_level"] == "Watch":
        return "Schedule QBR"
    else:
        return "Monitor"

df["recommended_action"] = df.apply(recommend_action, axis=1)

# ─────────────────────────────────────────────
# REVENUE AT RISK REPORT
# ─────────────────────────────────────────────

at_risk = df[df["risk_level"].isin(["Critical", "At Risk"])].sort_values(
    by=["health_score", "mrr"],
    ascending=[True, False]
)

total_mrr         = df["mrr"].sum()
at_risk_mrr       = at_risk["mrr"].sum()
at_risk_pct       = at_risk_mrr / total_mrr * 100
critical_accounts = (df["risk_level"] == "Critical").sum()

print("\n" + "=" * 55)
print("  REVENUE BRIDGE -- STRATEGIC RISK REPORT")
print("=" * 55)
print(f"\n  Total accounts analyzed : {len(df)}")
print(f"  Total portfolio MRR     : ${total_mrr:,.0f}")
print(f"  Accounts at risk        : {len(at_risk)}")
print(f"  Revenue at risk         : ${at_risk_mrr:,.0f} ({at_risk_pct:.1f}% of portfolio)")
print(f"  Critical accounts       : {critical_accounts}")

print(f"\n  Risk breakdown:")
for level, count in df["risk_level"].value_counts().items():
    mrr_sum = df[df["risk_level"] == level]["mrr"].sum()
    print(f"    {level:<12} {count:>3} accounts   ${mrr_sum:>10,.0f} MRR")

print(f"\n  Top 5 high-priority interventions:")
cols = ["company_name", "tier", "mrr", "health_score", "recommended_action"]
print(at_risk[cols].head().to_string(index=False))

# Save full report
at_risk.to_csv("high_priority_risk_report.csv", index=False)
print(f"\n  Full report saved: high_priority_risk_report.csv ({len(at_risk)} accounts)")

# ─────────────────────────────────────────────
# VISUALISATIONS
# ─────────────────────────────────────────────

forest      = "#003314"
forest_mid  = "#6b9e7e"
forest_pale = "#d4e6da"
stone       = "#f0efec"

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(
    "Revenue Bridge Analytics -- 100-Account Portfolio",
    fontsize=13, fontweight="bold", y=1.02
)

# Chart 1: Health Score Distribution
sorted_scores = df["health_score"].sort_values().values
colors = []
for s in sorted_scores:
    if s < 40:
        colors.append(forest)
    elif s < 65:
        colors.append(forest_mid)
    else:
        colors.append(forest_pale)

axes[0].bar(range(len(sorted_scores)), sorted_scores, color=colors, width=0.8)
axes[0].axhline(y=40, color=forest, linewidth=1.5, linestyle="--", alpha=0.7)
axes[0].text(102, 41, "Risk threshold", fontsize=8, color=forest, va="bottom")
axes[0].set_title("Health Score Distribution", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Accounts (sorted by score)")
axes[0].set_ylabel("Health Score (0-100)")
axes[0].set_xlim(-1, 103)
axes[0].set_ylim(0, 115)
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=forest,      label="At risk (< 40)"),
    Patch(facecolor=forest_mid,  label="Caution (40-65)"),
    Patch(facecolor=forest_pale, label="Healthy (> 65)"),
]
axes[0].legend(handles=legend_elements, loc="upper left", frameon=False, fontsize=8)

# Chart 2: Revenue at Risk by Tier
risk_by_tier = df[df["risk_level"].isin(["Critical", "At Risk"])].groupby("tier")["mrr"].sum()
risk_by_tier = risk_by_tier.reindex(["SMB", "Mid-Market", "Enterprise"]).fillna(0)
tier_colors  = [forest_pale, forest_mid, forest]

bars = axes[1].bar(
    risk_by_tier.index, risk_by_tier.values,
    color=tier_colors, width=0.5, edgecolor="white", linewidth=0.5
)
for bar, val in zip(bars, risk_by_tier.values):
    if val > 0:
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 300,
            f"${val:,.0f}",
            ha="center", va="bottom", fontsize=10,
            fontweight="bold", color=forest
        )
axes[1].set_title("Revenue at Risk by Tier", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Customer Tier")
axes[1].set_ylabel("MRR at Risk ($)")
axes[1].set_ylim(0, risk_by_tier.max() * 1.3)
axes[1].yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)

# Chart 3: Engagement vs Health Score
tier_color_map = {
    "SMB":        forest_pale,
    "Mid-Market": forest_mid,
    "Enterprise": forest,
}

for tier, group in df.groupby("tier"):
    engagement = 100 - (group["days_since_login"] * 1.1)
    engagement = engagement.clip(lower=0)
    axes[2].scatter(
        engagement,
        group["health_score"],
        c=tier_color_map[tier],
        label=tier, s=60, alpha=0.8,
        edgecolors="white", linewidths=0.4
    )

axes[2].axhline(y=40, color=forest, linewidth=1.2, linestyle="--", alpha=0.5)
axes[2].axvline(x=40, color=forest, linewidth=1.2, linestyle="--", alpha=0.5)
axes[2].text(2, 41.5, "Risk threshold", fontsize=8, color=forest, alpha=0.7)
axes[2].text(41, 2, "Low engagement", fontsize=8, color=forest, alpha=0.7)
axes[2].set_title("Engagement vs. Health Score", fontsize=11, fontweight="bold")
axes[2].set_xlabel("Engagement Score")
axes[2].set_ylabel("Health Score")
axes[2].set_xlim(-2, 105)
axes[2].set_ylim(-2, 105)
axes[2].legend(title="Tier", frameon=False, fontsize=9, title_fontsize=9)
axes[2].spines["top"].set_visible(False)
axes[2].spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("outputs/health_score_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"  Charts saved: outputs/health_score_distribution.png")
print("=" * 55)
