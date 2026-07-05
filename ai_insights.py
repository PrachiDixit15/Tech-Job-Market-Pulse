# ============================================================
#   TECH JOB MARKET PULSE — AI Insight Generator
#   Uses Claude AI to generate professional insights
#   and saves them as a PDF report
# ============================================================
# HOW TO RUN:
#   1. Make sure your output/ folder has all 6 Excel files
#   2. Add your API key to .env file
#   3. Run: python ai_insights.py
# ============================================================

import pandas as pd
import anthropic
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── LOAD API KEY SECURELY FROM .env ──────────────────────────
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not API_KEY:
    print("❌ ERROR: API key not found!")
    print("   Please add this line to your .env file:")
    print("   ANTHROPIC_API_KEY=your_key_here")
    exit()

print("✅ API key loaded securely from .env file")

# ── STEP 1: LOAD YOUR CLEANED DATA ───────────────────────────
print("\n" + "=" * 60)
print("  TECH JOB MARKET PULSE — AI Insight Generator")
print("=" * 60)
print("\n📂 Loading cleaned data...")

jobs     = pd.read_excel("output/01_cleaned_jobs.xlsx")
skills   = pd.read_excel("output/02_top_skills.xlsx")
salary   = pd.read_excel("output/03_salary_by_title.xlsx")
states   = pd.read_excel("output/04_jobs_by_state.xlsx")
exp      = pd.read_excel("output/05_experience_levels.xlsx")
remote   = pd.read_excel("output/06_remote_vs_onsite.xlsx")

print(f"  ✅ Loaded {len(jobs):,} jobs successfully")

# ── STEP 2: EXTRACT KEY STATISTICS ───────────────────────────
print("\n📊 Extracting key statistics...")

top5_skills = skills.head(5)[['skill_name', 'job_count']].to_string(index=False)
top5_salary = salary.head(5)[['job_title', 'avg_salary']].to_string(index=False)
top5_states = states[states['state'] != 'Unknown'].head(5)[['state', 'job_count']].to_string(index=False)
remote_stats = remote.to_string(index=False)

total_jobs      = len(jobs)
total_companies = jobs['company_name'].nunique()
remote_count    = (jobs['is_remote'] == 'Remote').sum()
onsite_count    = (jobs['is_remote'] == 'On-Site').sum()
remote_pct      = round(remote_count / total_jobs * 100, 1)

print("  ✅ Statistics extracted")

# ── STEP 3: BUILD PROMPT FOR CLAUDE AI ───────────────────────
print("\n🤖 Sending data to Claude AI...")

prompt = f"""
You are a senior data analyst specializing in job market research.
Analyze the following real LinkedIn job market data and generate
5 clear, professional, actionable insights.

Each insight should:
- Have a short bold title
- Be 2-3 sentences explaining what the data shows
- End with 1 actionable recommendation for job seekers

Here is the data:

DATASET OVERVIEW:
- Total job postings analyzed: {total_jobs:,}
- Unique companies: {total_companies:,}
- Remote jobs: {remote_count:,} ({remote_pct}%)
- On-site jobs: {onsite_count:,}

TOP 5 IN-DEMAND SKILLS:
{top5_skills}

TOP 5 HIGHEST PAYING JOB TITLES:
{top5_salary}

TOP 5 HIRING STATES:
{top5_states}

SALARY BY EXPERIENCE LEVEL:
Executive: $196,770 avg (375 jobs)
Director: $170,657 avg (1,259 jobs)
Mid-Senior: $113,131 avg (12,710 jobs)
Associate: $83,130 avg (3,806 jobs)
Entry Level: $65,258 avg (9,017 jobs)
Internship: $53,265 avg (364 jobs)

REMOTE VS ON-SITE:
{remote_stats}

Generate exactly 5 insights. Format each as:
INSIGHT [number]: [TITLE IN CAPS]
[2-3 sentence analysis]
ACTION: [one clear recommendation]

Keep language professional but easy to understand.
"""

# ── STEP 4: CALL CLAUDE AI API ────────────────────────────────
client = anthropic.Anthropic(api_key=API_KEY)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1500,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

ai_response = message.content[0].text
print("  ✅ AI insights generated successfully!")
print("\n" + "=" * 60)
print("  📋 PREVIEW OF AI INSIGHTS:")
print("=" * 60)
print(ai_response[:500] + "...")

# ── STEP 5: GENERATE PDF REPORT ───────────────────────────────
print("\n📄 Generating PDF report...")

os.makedirs("output", exist_ok=True)
pdf_path = "output/AI_Insights_Report.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch
)

# Colors
DARK_BG    = HexColor('#0f1117')
CARD_BG    = HexColor('#1a1d27')
BLUE       = HexColor('#3b4fd8')
GREEN      = HexColor('#34d399')
WHITE      = HexColor('#f9fafb')
GREY       = HexColor('#9ca3af')
LIGHT_GREY = HexColor('#e5e7eb')

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=24,
    textColor=WHITE,
    backColor=DARK_BG,
    alignment=TA_CENTER,
    spaceAfter=6,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=GREY,
    backColor=DARK_BG,
    alignment=TA_CENTER,
    spaceAfter=4,
    fontName='Helvetica'
)

stats_style = ParagraphStyle(
    'Stats',
    parent=styles['Normal'],
    fontSize=10,
    textColor=GREEN,
    backColor=DARK_BG,
    alignment=TA_CENTER,
    spaceAfter=20,
    fontName='Helvetica-Bold'
)

insight_title_style = ParagraphStyle(
    'InsightTitle',
    parent=styles['Normal'],
    fontSize=13,
    textColor=BLUE,
    spaceAfter=6,
    spaceBefore=16,
    fontName='Helvetica-Bold'
)

insight_body_style = ParagraphStyle(
    'InsightBody',
    parent=styles['Normal'],
    fontSize=10,
    textColor=LIGHT_GREY,
    spaceAfter=6,
    leading=16,
    fontName='Helvetica'
)

action_style = ParagraphStyle(
    'Action',
    parent=styles['Normal'],
    fontSize=10,
    textColor=GREEN,
    spaceAfter=12,
    fontName='Helvetica-Bold',
    leftIndent=10
)

footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=9,
    textColor=GREY,
    alignment=TA_CENTER,
    fontName='Helvetica'
)

# Build PDF Content
content = []

content.append(Spacer(1, 0.2*inch))
content.append(Paragraph("TECH JOB MARKET PULSE", title_style))
content.append(Paragraph("AI Generated Insights Report", subtitle_style))
content.append(Paragraph(
    f"Analyzed {total_jobs:,} LinkedIn job postings across {total_companies:,} companies",
    stats_style
))
content.append(HRFlowable(width="100%", thickness=1, color=BLUE))
content.append(Spacer(1, 0.2*inch))

lines = ai_response.strip().split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith('INSIGHT'):
        content.append(Paragraph(line, insight_title_style))
    elif line.startswith('ACTION:'):
        content.append(Paragraph(f"→ {line}", action_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=CARD_BG))
    else:
        content.append(Paragraph(line, insight_body_style))

content.append(Spacer(1, 0.3*inch))
content.append(HRFlowable(width="100%", thickness=1, color=BLUE))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    "Generated by Tech Job Market Pulse | Powered by Claude AI (Anthropic)",
    footer_style
))
content.append(Paragraph(
    "Data Source: LinkedIn Job Postings Dataset (Kaggle) | 115,415 job records",
    footer_style
))

doc.build(content)
print(f"  ✅ PDF saved: {pdf_path}")

# ── FINAL SUMMARY ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  🎉 AI INSIGHT GENERATOR COMPLETE!")
print("=" * 60)
print(f"\n  📄 Report saved: output/AI_Insights_Report.pdf")
print(f"  🤖 Powered by: Claude AI (Anthropic)")
print(f"  📊 Data analyzed: {total_jobs:,} job postings")
print("\n  Open the PDF to see your AI generated insights!\n")