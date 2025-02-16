
1. 查詢特定 Project 的 Milestone 周數和時間起訖
    ```sql
    SELECT
        m.week AS milestone_week,
        m.start_date AS milestone_start_date,
        m.end_date AS milestone_end_date
    FROM
        public.milestone m
    WHERE
        m.project_id = 1
    ORDER BY
        m.week;
    ```
2. 計算每個 Project 的 Milestone 總周數：
    ```sql
    SELECT
        p.title AS project_title,
        COUNT(m.week) AS total_milestone_weeks
    FROM
        public.project p
    JOIN
        public.milestone m ON p.id = m.project_id
    GROUP BY
        p.id, p.title
    ORDER BY
        p.title;

    ```
3. 計算每個 Project Milestone 的最早開始日期和最晚結束日期
```sql
select
    p.id,
    p.title AS project_title,
    MIN(m.start_date) AS earliest_milestone_start_date,
    MAX(m.end_date) AS latest_milestone_end_date
FROM
    public.project p
JOIN
    public.milestone m ON p.id = m.project_id
GROUP BY
    p.id, p.title
ORDER BY
    p.title;
```

3.1 
```sql
CREATE OR REPLACE FUNCTION public.get_project_milestone_range_dates(p_project_id integer DEFAULT NULL::integer)
RETURNS TABLE(
    project_id integer, 
    project_title text, 
    earliest_milestone_start_date date, 
    latest_milestone_end_date date
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.title::TEXT AS project_title,  -- 明確轉換為 TEXT
        MIN(m.start_date) AS earliest_milestone_start_date,
        MAX(m.end_date) AS latest_milestone_end_date
    FROM
        public.project p
    JOIN
        public.milestone m ON p.id = m.project_id
    WHERE
        (p_project_id IS NULL OR p.id = p_project_id)
    GROUP BY
        p.id, p.title
    ORDER BY
        p.title;
END;
$function$;
```
```sql
SELECT * FROM public.get_project_milestone_range_dates();
SELECT * FROM public.get_project_milestone_range_dates(1);

```
4. 查詢每個專案（project）及其對應的里程碑（milestone）的起始和結束日期
```sql
SELECT
    p.id AS project_id,
    p.title AS project_title,
    m.start_date AS milestone_start_date,
    m.end_date AS milestone_end_date
FROM
    public.project p
JOIN
    public.milestone m ON p.id = m.project_id
ORDER BY
    p.id, m.start_date;
```
```sql
CREATE OR REPLACE FUNCTION public.get_project_milestone_dates(p_project_id integer DEFAULT NULL::integer)
RETURNS TABLE(
    project_id integer, 
    project_title text, 
    milestone_start_date date, 
    milestone_end_date date
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT
        p.id AS project_id,
        p.title::TEXT AS project_title,  -- 明確轉換為 TEXT
        m.start_date AS milestone_start_date,
        m.end_date AS milestone_end_date
    FROM
        public.project p
    JOIN
        public.milestone m ON p.id = m.project_id
    WHERE
        (p_project_id IS NULL OR p.id = p_project_id)  -- 如果傳入 p_project_id，則過濾相應專案
    ORDER BY
        p.id, m.start_date;
END;
$function$;

```
```sql
SELECT * FROM public.get_project_milestone_dates();
SELECT * FROM public.get_project_milestone_dates(1);

```