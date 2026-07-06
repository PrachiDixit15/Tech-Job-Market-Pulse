# 🚀 Tech Job Market Pulse
### *Turning 115,000+ LinkedIn Job Postings into Actionable Career Insights*

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![SQL](https://img.shields.io/badge/SQL-Server-red?style=flat-square&logo=microsoft-sql-server)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?style=flat-square&logo=powerbi)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)
![AI](https://img.shields.io/badge/AI%20Insights-Coming%20Soon-orange?style=flat-square)

---

## 📌 Problem Statement

Every year, thousands of freshers and job seekers apply blindly — without knowing:
- Which skills are **actually** in demand?
- Which roles pay the **highest salaries**?
- Which cities/states have the **most opportunities**?
- Is **remote work** really available or just a myth?

**Tech Job Market Pulse** solves this by analyzing **115,415 real LinkedIn job postings** to deliver data-driven career guidance — backed by facts, not opinions.

---

## 🎯 Project Workflow
```
Raw Dataset (123,849 records)
         ↓
🔵 Stage 1 — SQL Data Cleaning
         ↓
🟢 Stage 2 — Python EDA & Visualization
         ↓
🟡 Stage 3 — Power BI Dashboard (5 pages)
         ↓
🔴 Stage 4 — AI Insight Generator (Planned)
         ↓
🟣 Stage 5 — Web Deployment (Planned)
```

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python (Pandas)** | Data cleaning & merging 6 datasets |
| **SQL Server (SSMS)** | Data analysis & querying |
| **Matplotlib & Seaborn** | Exploratory data visualization |
| **Power BI** | Interactive 5-page dashboard |

---

## 📊 Dataset

- **Source:** [LinkedIn Job Postings — Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)
- **Size:** 123,849 job postings
- **Files:** 6 CSV files (postings, skills, salaries, companies, industries, mappings)
- **After Cleaning:** 115,415 quality records

---

## 💡 Key Insights Discovered

| # | Insight |
|---|---------|
| 1 | 🛠️ **Information Technology** is the most demanded skill — appearing in 18,432 job postings |
| 2 | 💰 **Executive roles** pay 3x more than Entry Level ($196,770 vs $65,258 avg) |
| 3 | 📍 **California** dominates US hiring — more jobs than TX, NY, and FL combined |
| 4 | 🏥 **Healthcare** hires the most but **Real Estate** pays the highest salaries |
| 5 | 🏠 Only **12.29%** of jobs are remote — 87.71% still require on-site presence |
| 6 | 📈 Moving from Entry to Mid-Senior level gives a **73% salary increase** |
| 7 | 💼 **79.81%** of all job postings are Full-Time positions |
| 8 | 🔒 **71%** of companies don't publicly disclose salary information |

---

## 📁 Project Structure

```
Tech-Job-Market-Pulse/
│
├── 📄 clean_data.py                → Python data cleaning script
├── 📄 eda.py                       → Exploratory data analysis & charts
├── 📄 ai_insights.py               → AI insight generator (work in progress)
├── 📄 SQL_Cleaning_Queries.sql     → SQL analysis queries
├── 📄 TechJobMarketPulse.pbix      → Power BI dashboard file
├── 📄 TechJobPulse_Theme.json      → Custom dark theme for Power BI
├── 📄 .gitignore                   → Protects sensitive files
│
└── 📁 output/
    ├── 01_cleaned_jobs.xlsx        → Master cleaned dataset
    ├── 02_top_skills.xlsx          → Skills demand analysis
    ├── 03_salary_by_title.xlsx     → Salary by job title
    ├── 04_jobs_by_state.xlsx       → Jobs by US state
    ├── 05_experience_levels.xlsx   → Experience level distribution
    ├── 06_remote_vs_onsite.xlsx    → Remote work analysis
    └── charts/                     → 5 Python generated charts
```

---

## 📈 Power BI Dashboard — 5 Pages

| Page | Content |
|------|---------|
| 🛠️ **Skills Demand** | Top 10 in-demand skills + KPI cards |
| 💰 **Salary Insights** | Salary by experience + Top paying roles |
| 📍 **Job Market Map** | Top hiring states + Remote vs On-Site |
| 🏭 **Industry Insights** | Top industries by jobs + salary |
| 💼 **Job Type Analysis** | Work type distribution + Top companies |

---

## ▶️ How to Run

### Prerequisites
```bash
pip install pandas openpyxl matplotlib seaborn python-dotenv
```

### Step 1 — Data Cleaning
```bash
python clean_data.py
```

### Step 2 — Python EDA
```bash
python eda.py
```

### Step 3 — Power BI Dashboard
Open `TechJobMarketPulse.pbix` in Power BI Desktop

---

## 🗄️ SQL Analysis

5 key queries in `SQL_Cleaning_Queries.sql`:
```sql
Query 1 → Missing value analysis
Query 2 → Data cleaning & table creation
Query 3 → Top skills in demand
Query 4 → Salary by experience level
Query 5 → Top hiring states
```

---

## 🔮 Upcoming Features (Version 2.0)

These features are currently in development and will be added soon:

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 **AI Insight Generator** | Auto-generate insights using Claude AI (Anthropic) | 🔄 In Progress |
| 💬 **Interactive Chat** | Ask any question about job market data in plain English | 📅 Planned |
| 🌐 **Web Deployment** | Deploy as a live Streamlit web app | 📅 Planned |
| 🇮🇳 **India Job Market** | Add Naukri/Indeed India data for local insights | 📅 Planned |

---

## 📬 Contact

**Prachi Dixit**
- GitHub: [@PrachiDixit15](https://github.com/PrachiDixit15)
- LinkedIn: *Add your LinkedIn URL here*

---

## ⭐ If you found this project helpful, please give it a star!

---

*Built with ❤️ using Python, SQL and Power BI*


