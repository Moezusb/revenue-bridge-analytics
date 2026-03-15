import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────
# PROJECT SENTINEL — Data Generator
# Generates three synthetic siloed datasets
# mimicking a real B2B SaaS tech stack:
#   - CRM (Salesforce)
#   - Support (Service Cloud / Intercom)
#   - Product Usage
# ─────────────────────────────────────────────

np.random.seed(42)
NUM_ACCOUNTS = 100

# ── REALISTIC SYNTHETIC COMPANY NAMES ──
COMPANY_NAMES = [
    "Meridian Technologies", "Northgate Financial", "Crestview Solutions",
    "Harlow Logistics", "Pinnacle Analytics", "Ashford Capital",
    "Beacon Systems", "Ridgeline Software", "Clearwater Ventures",
    "Summit Operations", "Ironwood Consulting", "Driftwood Media",
    "Halcyon Health", "Stonegate Partners", "Vantage Point AI",
    "Orion Data Services", "Cobalt Dynamics", "Whitmore Group",
    "Elevate Commerce", "Fieldstone Advisory", "Nexus Platforms",
    "Arborview Networks", "Cascade Digital", "Trident Analytics",
    "Helix Solutions", "Broadmoor Strategies", "Latitude Systems",
    "Keystone Insights", "Wavecrest Technologies", "Aldgate Partners",
    "Spruce Capital", "Forefront Logistics", "Elm Street Analytics",
    "Redwood Operations", "Monarch Consulting", "Cypress Group",
    "Silverline Media", "Bridgeport Systems", "Falconer Labs",
    "Greywood Financial", "Anchor Point Solutions", "Hillcrest Digital",
    "Veritas Platforms", "Stormlight Advisory", "Openfield Commerce",
    "Dawnridge Networks", "Paragon Data", "Cloudmere Technologies",
    "Thornwood Ventures", "Blueprint Analytics", "Granite Consulting",
    "Windfall Systems", "Starboard Insights", "Lighthouse Partners",
    "Ironside Solutions", "Cottonwood Advisory", "Pathway Logistics",
    "Clearpath Dynamics", "Edgewood Financial", "Sandstone Operations",
    "Goldleaf Technologies", "Rosewood Platforms", "Foxgate Consulting",
    "Riverstone Media", "Highmark Systems", "Birchwood Ventures",
    "Cornerstone Analytics", "Westpoint Advisory", "Oakdale Solutions",
    "Meadowbrook Digital", "Sagebrush Networks", "Pebble Creek Labs",
    "Northbrook Capital", "Eastgate Partners", "Sunridge Commerce",
    "Fairview Insights", "Lakewood Systems", "Millstone Group",
    "Pinecrest Technologies", "Hillside Platforms", "Bayside Consulting",
    "Valleyfield Analytics", "Springbrook Advisory", "Hawthorne Solutions",
    "Maplewood Operations", "Fernhill Digital", "Willow Creek Labs",
    "Kestrel Networks", "Ashwood Ventures", "Terrace Point Consulting",
    "Cloverleaf Systems", "Lantern Analytics", "Overture Platforms",
    "Shoreline Advisory", "Crossroads Commerce", "Greenbelt Solutions",
    "Foxwood Media", "Coldwater Insights", "Riverbend Partners",
    "Sapphire Systems", "Thornfield Analytics", "Cloudbase Ventures"
]

TIERS = ["SMB", "Mid-Market", "Enterprise"]
TIER_MRR_RANGES = {
    "SMB":        (500,   3000),
    "Mid-Market": (3001,  15000),
    "Enterprise": (15001, 50000),
}

# ── ASSIGN TIERS ──
tier_weights = [0.45, 0.40, 0.15]
tiers = np.random.choice(TIERS, size=NUM_ACCOUNTS, p=tier_weights)

# ── GENERATE MRR ──
mrr = [
    round(np.random.uniform(*TIER_MRR_RANGES[t]), 2)
    for t in tiers
]

# ── RENEWAL MONTHS (1-12 months out) ──
renewal_months = np.random.randint(1, 13, size=NUM_ACCOUNTS)

# ── DATASET 1: CRM (Salesforce) ──
crm_df = pd.DataFrame({
    "account_id":       [f"ACC-{str(i+1).zfill(3)}" for i in range(NUM_ACCOUNTS)],
    "company_name":     COMPANY_NAMES[:NUM_ACCOUNTS],
    "tier":             tiers,
    "mrr":              mrr,
    "renewal_in_months": renewal_months,
    "account_owner":    np.random.choice(
                            ["Sarah Chen", "James Okafor", "Priya Mehta",
                             "Tom Bergmann", "Aisha Diallo"],
                            size=NUM_ACCOUNTS
                        ),
})

# ── DATASET 2: SUPPORT (Service Cloud / Intercom) ──
# Tickets filed in last 90 days, avg resolution time, sentiment score
# Sentiment: rule-based score from 0-100 (100 = very positive)
# Higher ticket volume + slower resolution = lower sentiment likely
ticket_volume     = np.random.randint(0, 25, size=NUM_ACCOUNTS)
avg_resolution_hr = np.random.uniform(1, 72, size=NUM_ACCOUNTS).round(1)

# Rule-based sentiment: penalise high volume and slow resolution
raw_sentiment = (
    100
    - (ticket_volume * 1.8)
    - (avg_resolution_hr * 0.4)
    + np.random.normal(0, 8, size=NUM_ACCOUNTS)
)
sentiment_score = np.clip(raw_sentiment, 10, 100).round(1)

support_df = pd.DataFrame({
    "account_id":          crm_df["account_id"],
    "tickets_last_90d":    ticket_volume,
    "avg_resolution_hrs":  avg_resolution_hr,
    "sentiment_score":     sentiment_score,  # Rule-based, not AI-scored
    "has_open_escalation": np.random.choice([True, False], size=NUM_ACCOUNTS, p=[0.15, 0.85]),
})

# ── DATASET 3: PRODUCT USAGE ──
# Days since last login, features used vs available
days_since_login  = np.random.randint(0, 90, size=NUM_ACCOUNTS)
features_available = np.random.randint(8, 20, size=NUM_ACCOUNTS)
features_used      = np.array([
    np.random.randint(1, avail + 1)
    for avail in features_available
])
adoption_rate = (features_used / features_available * 100).round(1)

usage_df = pd.DataFrame({
    "account_id":          crm_df["account_id"],
    "days_since_login":    days_since_login,
    "features_available":  features_available,
    "features_used":       features_used,
    "adoption_rate_pct":   adoption_rate,
    "monthly_active_users": np.random.randint(1, 50, size=NUM_ACCOUNTS),
})

# ── SAVE TO CSV ──
os.makedirs("data", exist_ok=True)
crm_df.to_csv("data/crm_data.csv", index=False)
support_df.to_csv("data/support_data.csv", index=False)
usage_df.to_csv("data/usage_data.csv", index=False)

print("Data generation complete.")
print(f"  CRM:     {len(crm_df)} accounts saved to data/crm_data.csv")
print(f"  Support: {len(support_df)} accounts saved to data/support_data.csv")
print(f"  Usage:   {len(usage_df)} accounts saved to data/usage_data.csv")
print(f"\n  Tier breakdown:")
for tier in TIERS:
    count = (crm_df["tier"] == tier).sum()
    print(f"    {tier}: {count} accounts")
