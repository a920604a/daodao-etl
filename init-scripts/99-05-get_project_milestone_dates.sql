CREATE OR REPLACE FUNCTION public.get_project_milestone_dates(p_project_id integer DEFAULT NULL::integer)
RETURNS TABLE(
    project_id integer, 
    project_title text, 
    milestone_id integer,
    milestone_start_date date, 
    milestone_end_date date, 
    week_number integer,
    is_completed boolean 
)
LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT
        p.id AS project_id,  
        p.title::TEXT AS project_title,
        m.id AS milestone_id,
        m.start_date AS milestone_start_date,
        m.end_date AS milestone_end_date,
        ((EXTRACT(DAY FROM (m.start_date::timestamp - (SELECT MIN(m2.start_date) FROM public.milestone m2 WHERE m2.project_id = p.id))) / 7) + 1)::integer AS week_number,
        m.is_completed 
    FROM
        public.project p
    JOIN
        public.milestone m ON p.id = m.project_id
    WHERE
        (p_project_id IS NULL OR p.id = p_project_id)  
    ORDER BY
        p.id, m.start_date;
END;
$function$;
