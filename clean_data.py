# ============================================================
#   TECH JOB MARKET PULSE — Data Cleaning & Analysis Script
#   Works with your exact Kaggle LinkedIn dataset
# ============================================================
# HOW TO RUN:
#   python clean_data.py
# ============================================================

import pandas as pd
import os

os.makedirs("output", exist_ok=True)

print("=" * 60)
print("  TECH JOB MARKET PULSE — Data Cleaning")
print("=" * 60)

# ── STEP 1: LOAD ALL FILES ────────────────────────────────────
print("\n📂 Loading all dataset files...")

postings      = pd.read_csv("postings.csv", low_memory=False)
job_skills    = pd.read_csv("jobs/job_skills.csv")
skills_map    = pd.read_csv("mappings/skills.csv")
salaries      = pd.read_csv("jobs/salaries.csv")
companies     = pd.read_csv("companies/companies.csv", low_memory=False)
job_industries= pd.read_csv("jobs/job_industries.csv")
industries_map= pd.read_csv("mappings/industries.csv")

print(f"  ✅ postings        → {len(postings):,} rows")
print(f"  ✅ job_skills       → {len(job_skills):,} rows")
print(f"  ✅ skills_map       → {len(skills_map):,} skills")
print(f"  ✅ salaries         → {len(salaries):,} rows")
print(f"  ✅ companies        → {len(companies):,} rows")
print(f"  ✅ job_industries   → {len(job_industries):,} rows")

# ── STEP 2: CLEAN POSTINGS ────────────────────────────────────
print("\n🧹 Cleaning postings...")

# Keep only relevant columns
df = postings[[
    'job_id', 'company_id', 'title', 'location',
    'formatted_experience_level', 'formatted_work_type',
    'remote_allowed', 'normalized_salary', 'views', 'applies'
]].copy()

df.rename(columns={
    'title': 'job_title',
    'formatted_experience_level': 'experience_level',
    'formatted_work_type': 'work_type',
    'remote_allowed': 'is_remote'
}, inplace=True)

# Drop rows with no job title
df.dropna(subset=['job_title'], inplace=True)

# Clean experience level
df['experience_level'] = df['experience_level'].fillna('Not Specified')

# Remote flag
df['is_remote'] = df['is_remote'].fillna(0).astype(int)
df['is_remote'] = df['is_remote'].map({1: 'Remote', 0: 'On-Site'})

# Extract state from location (e.g. "New York, NY" → "NY")
df['state'] = df['location'].astype(str).apply(
    lambda x: x.split(',')[-1].strip() if ',' in x else 'Unknown'
)

# Drop duplicates
df.drop_duplicates(subset=['job_title', 'company_id', 'location'], inplace=True)
print(f"  ✅ Cleaned postings: {len(df):,} rows")

# ── STEP 3: MERGE SKILLS ─────────────────────────────────────
print("\n🔗 Merging skills...")

# Join skill abbreviations with full names
skills_full = job_skills.merge(skills_map, on='skill_abr', how='left')

# Count how many jobs need each skill
skill_demand = (
    skills_full.groupby('skill_name')['job_id']
    .count()
    .reset_index()
    .rename(columns={'job_id': 'job_count'})
    .sort_values('job_count', ascending=False)
)
print(f"  ✅ Skill demand table: {len(skill_demand)} skills ranked")

# ── STEP 4: MERGE SALARY ─────────────────────────────────────
print("\n💰 Merging salary data...")

sal = salaries[['job_id', 'min_salary', 'med_salary', 'max_salary', 'pay_period']].copy()
sal = sal[sal['pay_period'] == 'YEARLY']   # Keep only annual salaries
sal['avg_salary'] = sal[['min_salary', 'max_salary']].mean(axis=1)

df = df.merge(sal[['job_id', 'avg_salary']], on='job_id', how='left')
salary_available = df['avg_salary'].notna().sum()
print(f"  ✅ Salary data available for {salary_available:,} jobs")

# ── STEP 5: MERGE COMPANY INFO ───────────────────────────────
print("\n🏢 Merging company info...")

comp = companies[['company_id', 'name', 'company_size', 'state', 'country']].copy()
comp.rename(columns={'name': 'company_name', 'state': 'company_state'}, inplace=True)

df = df.merge(comp, on='company_id', how='left')
print(f"  ✅ Company info merged")

# ── STEP 6: MERGE INDUSTRY ───────────────────────────────────
print("\n🏭 Merging industry info...")

ind = job_industries.merge(industries_map, on='industry_id', how='left')
ind = ind.groupby('job_id')['industry_name'].first().reset_index()
df = df.merge(ind, on='job_id', how='left')
df['industry_name'] = df['industry_name'].fillna('Other')
print(f"  ✅ Industry info merged")

# ── STEP 7: EXPORT OUTPUTS ───────────────────────────────────
print("\n💾 Exporting files...")

# 1. Main cleaned dataset
df.to_excel("output/01_cleaned_jobs.xlsx", index=False)
print(f"  ✅ output/01_cleaned_jobs.xlsx  ({len(df):,} rows)")

# 2. Top skills in demand
skill_demand.to_excel("output/02_top_skills.xlsx", index=False)
print(f"  ✅ output/02_top_skills.xlsx")

# 3. Salary by job title (top 20 roles with salary data)
salary_by_title = (
    df.groupby('job_title')['avg_salary']
    .agg(['mean', 'count'])
    .reset_index()
    .rename(columns={'mean': 'avg_salary', 'count': 'job_count'})
    .query('job_count >= 5')
    .sort_values('avg_salary', ascending=False)
    .head(30)
)
salary_by_title.to_excel("output/03_salary_by_title.xlsx", index=False)
print(f"  ✅ output/03_salary_by_title.xlsx")

# 4. Jobs by state
jobs_by_state = (
    df.groupby('state')['job_id']
    .count()
    .reset_index()
    .rename(columns={'job_id': 'job_count'})
    .sort_values('job_count', ascending=False)
    .head(30)
)
jobs_by_state.to_excel("output/04_jobs_by_state.xlsx", index=False)
print(f"  ✅ output/04_jobs_by_state.xlsx")

# 5. Experience level distribution
exp_dist = (
    df.groupby('experience_level')['job_id']
    .count()
    .reset_index()
    .rename(columns={'job_id': 'job_count'})
    .sort_values('job_count', ascending=False)
)
exp_dist.to_excel("output/05_experience_levels.xlsx", index=False)
print(f"  ✅ output/05_experience_levels.xlsx")

# 6. Remote vs On-site
remote_dist = (
    df.groupby('is_remote')['job_id']
    .count()
    .reset_index()
    .rename(columns={'job_id': 'job_count'})
)
remote_dist.to_excel("output/06_remote_vs_onsite.xlsx", index=False)
print(f"  ✅ output/06_remote_vs_onsite.xlsx")

# ── FINAL SUMMARY ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  🎉 ALL DONE! Summary of your clean data:")
print("=" * 60)
print(f"  Total jobs cleaned     : {len(df):,}")
print(f"  Jobs with salary data  : {salary_available:,}")
print(f"  Unique job titles      : {df['job_title'].nunique():,}")
print(f"  Unique companies       : {df['company_name'].nunique():,}")
print(f"  Unique states          : {df['state'].nunique():,}")
print(f"  Remote jobs            : {(df['is_remote']=='Remote').sum():,}")
print(f"  On-site jobs           : {(df['is_remote']=='On-Site').sum():,}")
print("\n  📁 6 Excel files saved in output/ folder")
print("  👉 Next step: Open these in Power BI!\n")
