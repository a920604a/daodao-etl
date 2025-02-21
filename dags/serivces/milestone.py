from sqlalchemy import text, select

def fetch_project_milestones(session, project_id: int):
    """ 調用 get_project_milestone_dates(project_id) 取得里程碑數據 """
    sql = text("SELECT * FROM public.get_project_milestone_dates(:project_id)")
    result = session.execute(sql, {"project_id": project_id})

    return [
        {
            "project_id": row[0],
            "project_title": row[1],  # 假設 project_title 可用作 milestone name
            "milestone_id": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "week": row[5],
            "is_completed": row[6]
        }
        for row in result.fetchall()
    ]
