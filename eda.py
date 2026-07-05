# ============================================================
#   TECH JOB MARKET PULSE — Python EDA Script
#   Generates 5 professional charts from your cleaned data
# ============================================================
# HOW TO RUN:
#   1. Open VS Code in TechJobMarketPulse folder
#   2. Run: python eda.py
#   3. Charts will be saved in output/charts/ folder
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── SETUP ────────────────────────────────────────────────────
print("=" * 60)
print("  TECH JOB MARKET PULSE — Python EDA")
print("=" * 60)

# Create charts folder
os.makedirs("output/charts", exist_ok=True)

# Style settings
sns.set_theme(style="whitegrid")
COLORS = sns.color_palette("Blues_r", 10)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'sans-serif'

# ── LOAD DATA ────────────────────────────────────────────────
print("\n📂 Loading cleaned data...")

jobs      = pd.read_excel("output/01_cleaned_jobs.xlsx")
skills    = pd.read_excel("output/02_top_skills.xlsx")
salary    = pd.read_excel("output/03_salary_by_title.xlsx")
states    = pd.read_excel("output/04_jobs_by_state.xlsx")
exp       = pd.read_excel("output/05_experience_levels.xlsx")
remote    = pd.read_excel("output/06_remote_vs_onsite.xlsx")

print(f"  ✅ Loaded {len(jobs):,} jobs")

# ── CHART 1: TOP 10 SKILLS IN DEMAND ─────────────────────────
print("\n📊 Chart 1: Top 10 Skills in Demand...")

top_skills = skills.head(10)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(
    top_skills['skill_name'][::-1],
    top_skills['job_count'][::-1],
    color=COLORS
)

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 100, bar.get_y() + bar.get_height()/2,
            f'{int(width):,}', va='center', fontsize=9)

ax.set_title('Top 10 Most In-Demand Skills on LinkedIn',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Job Postings', fontsize=12)
ax.set_ylabel('Skill', fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'{int(x):,}'))
plt.tight_layout()
plt.savefig("output/charts/01_top_skills.png")
plt.close()
print("  ✅ Saved: output/charts/01_top_skills.png")

# ── CHART 2: SALARY BY EXPERIENCE LEVEL ──────────────────────
print("\n📊 Chart 2: Salary by Experience Level...")

# Manual data from SQL Query 4 results
exp_data = pd.DataFrame({
    'experience_level': ['Executive', 'Director', 'Mid-Senior',
                         'Associate', 'Entry Level', 'Internship'],
    'avg_salary': [196770, 170657, 113131, 83130, 65258, 53265],
    'total_jobs': [375, 1259, 12710, 3806, 9017, 364]
})

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(
    exp_data['experience_level'],
    exp_data['avg_salary'],
    color=COLORS[:6]
)

# Add value labels on bars
for bar, val in zip(bars, exp_data['avg_salary']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 1000,
            f'${val:,.0f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_title('Average Salary by Experience Level',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Experience Level', fontsize=12)
ax.set_ylabel('Average Salary (USD)', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'${int(x):,}'))
plt.tight_layout()
plt.savefig("output/charts/02_salary_by_experience.png")
plt.close()
print("  ✅ Saved: output/charts/02_salary_by_experience.png")

# ── CHART 3: REMOTE VS ON-SITE ────────────────────────────────
print("\n📊 Chart 3: Remote vs On-Site...")

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    remote['job_count'],
    labels=remote['is_remote'],
    autopct='%1.1f%%',
    colors=['#2196F3', '#90CAF9'],
    startangle=90,
    explode=[0.05, 0],
    textprops={'fontsize': 13}
)
for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_fontsize(14)

ax.set_title('Remote vs On-Site Job Distribution',
             fontsize=16, fontweight='bold', pad=20)

# Add total count annotation
total = remote['job_count'].sum()
ax.annotate(f'Total Jobs: {total:,}',
            xy=(0, -1.2), ha='center', fontsize=11,
            color='gray')
plt.tight_layout()
plt.savefig("output/charts/03_remote_vs_onsite.png")
plt.close()
print("  ✅ Saved: output/charts/03_remote_vs_onsite.png")

# ── CHART 4: TOP 10 HIRING STATES ────────────────────────────
print("\n📊 Chart 4: Top 10 Hiring States...")

# Filter out Unknown
top_states = states[states['state'] != 'Unknown'].head(10)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(
    top_states['state'][::-1],
    top_states['job_count'][::-1],
    color=COLORS
)

for bar in bars:
    width = bar.get_width()
    ax.text(width + 50, bar.get_y() + bar.get_height()/2,
            f'{int(width):,}', va='center', fontsize=9)

ax.set_title('Top 10 US States by Job Openings',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Job Postings', fontsize=12)
ax.set_ylabel('State', fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'{int(x):,}'))
plt.tight_layout()
plt.savefig("output/charts/04_top_states.png")
plt.close()
print("  ✅ Saved: output/charts/04_top_states.png")

# ── CHART 5: SALARY DISTRIBUTION ─────────────────────────────
print("\n📊 Chart 5: Salary Distribution...")

# Filter salary data
salary_data = jobs['avg_salary'].dropna()
salary_data = salary_data[
    (salary_data >= 20000) & (salary_data <= 500000)
]

fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(salary_data, bins=50, color='#2196F3',
        edgecolor='white', alpha=0.85)

# Add median line
median = salary_data.median()
ax.axvline(median, color='red', linestyle='--',
           linewidth=2, label=f'Median: ${median:,.0f}')

ax.set_title('Salary Distribution Across All Job Postings',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Annual Salary (USD)', fontsize=12)
ax.set_ylabel('Number of Jobs', fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'${int(x):,}'))
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig("output/charts/05_salary_distribution.png")
plt.close()
print("  ✅ Saved: output/charts/05_salary_distribution.png")

# ── FINAL SUMMARY ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  🎉 ALL CHARTS GENERATED!")
print("=" * 60)
print("\n  📁 Find your charts in: output/charts/")
print("\n  Charts created:")
print("  01_top_skills.png")
print("  02_salary_by_experience.png")
print("  03_remote_vs_onsite.png")
print("  04_top_states.png")
print("  05_salary_distribution.png")
print("\n  👉 Next step: Power BI Dashboard!\n")
