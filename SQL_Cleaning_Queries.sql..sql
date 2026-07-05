-- ── QUERY 1: CHECK MISSING VALUES ───────────────────────────
-- See how many nulls exist in important columns

SELECT
    COUNT(*)                                    AS total_jobs,
    SUM(CASE WHEN title          IS NULL THEN 1 ELSE 0 END) AS missing_title,
    SUM(CASE WHEN location       IS NULL THEN 1 ELSE 0 END) AS missing_location,
    SUM(CASE WHEN company_name   IS NULL THEN 1 ELSE 0 END) AS missing_company,
    SUM(CASE WHEN normalized_salary IS NULL THEN 1 ELSE 0 END) AS missing_salary,
    SUM(CASE WHEN formatted_experience_level IS NULL THEN 1 ELSE 0 END) AS missing_experience
FROM postings;


-- Drop old table first
DROP TABLE IF EXISTS postings_clean;

-- Now recreate it cleanly
SELECT
    job_id,
    title                            AS job_title,
    company_name,
    location,
    CASE
        WHEN location LIKE '%, %'
        THEN LTRIM(SUBSTRING(location, CHARINDEX(',', location) + 1, LEN(location)))
        ELSE 'Unknown'
    END                              AS state,
    formatted_experience_level       AS experience_level,
    formatted_work_type              AS work_type,
    CASE
        WHEN remote_allowed = '1'   OR
             remote_allowed = '1.0' THEN 'Remote'
        ELSE 'On-Site'
    END                              AS is_remote,
    normalized_salary                AS avg_salary,
    views,
    applies
INTO postings_clean
FROM postings
WHERE title IS NOT NULL
  AND company_name IS NOT NULL;

-- Verify
SELECT COUNT(*) AS clean_jobs FROM postings_clean;


-- ── QUERY 3: TOP SKILLS IN DEMAND ───────────────────────────

SELECT
    s.skill_name,
    COUNT(js.job_id)                 AS job_count,
    ROUND(COUNT(js.job_id) * 100.0
        / (SELECT COUNT(*) FROM job_skills), 2) AS percentage
FROM job_skills js
JOIN skills s ON js.skill_abr = s.skill_abr
GROUP BY s.skill_name
ORDER BY job_count DESC;

-- ── QUERY 4: SALARY ANALYSIS BY EXPERIENCE LEVEL ────────────

SELECT
    formatted_experience_level       AS experience_level,
    COUNT(*)                         AS total_jobs,
    ROUND(AVG(normalized_salary), 0) AS avg_salary,
    ROUND(MIN(normalized_salary), 0) AS min_salary,
    ROUND(MAX(normalized_salary), 0) AS max_salary
FROM postings
WHERE normalized_salary IS NOT NULL
  AND normalized_salary BETWEEN 20000 AND 500000
  AND formatted_experience_level IS NOT NULL
GROUP BY formatted_experience_level
ORDER BY avg_salary DESC;


-- ── QUERY 5: TOP HIRING STATES ───────────────────────────────

SELECT TOP 15
    CASE
        WHEN location LIKE '%, %'
        THEN LTRIM(SUBSTRING(location, CHARINDEX(',', location) + 1, LEN(location)))
        ELSE 'Unknown'
    END                              AS state,
    COUNT(*)                         AS job_count,
    ROUND(AVG(normalized_salary), 0) AS avg_salary,
    SUM(CASE WHEN remote_allowed = '1' OR
             remote_allowed = '1.0'
        THEN 1 ELSE 0 END)           AS remote_jobs
FROM postings
WHERE title IS NOT NULL
GROUP BY
    CASE
        WHEN location LIKE '%, %'
        THEN LTRIM(SUBSTRING(location, CHARINDEX(',', location) + 1, LEN(location)))
        ELSE 'Unknown'
    END
ORDER BY job_count DESC

--✅ Query 1 → 71% jobs hide salary data
--✅ Query 2 → 1,23,849 clean jobs created
--✅ Query 3 → IT, Sales, Management = top skills
--✅ Query 4 → Entry→Mid-Senior = 73% salary jump
--✅ Query 5 → CA, TX, NY, FL = top hiring states