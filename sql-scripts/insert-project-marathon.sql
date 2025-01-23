-- 插入 project 表
INSERT INTO "project" (
    "user_id", 
    "img_url", 
    "topic", 
    "project_description", 
    "motivation", 
    "motivation_description", 
    "goal", 
    "content", 
    "policy", 
    "policy_description", 
    "resource_name", 
    "resource_url", 
    "presentation", 
    "presentation_description", 
    "is_public", 
    "status", 
    "created_by", 
    "updated_by", 
    "version"
) VALUES (
    1, 
    'https://example.com/image.jpg', 
    'AI for Healthcare', 
    'This project aims to use AI to improve healthcare.', 
    ARRAY['driven_by_curiosity'::motivation_t, 'career_development'::motivation_t], 
    'Motivated by curiosity and career development.', 
    'Develop an AI-powered healthcare tool', 
    'Research and development on machine learning techniques for healthcare.', 
    ARRAY['data_collection_research_analysis', 'others']::policy_t[], 
    'Discounts available for students in low-income regions.', 
    ARRAY['Document 1', 'Document 2'], 
    ARRAY['https://resource1.com', 'https://resource2.com'], 
    ARRAY['building_websites'::presentation_t, 'teaching_courses'::presentation_t], 
    'Focus on building AI models and teaching healthcare professionals.', 
    true, 
    'Ongoing', 
    1, 
    2, 
    1
);

-- 插入 user_project 表
INSERT INTO "user_project" ("user_id", "project_id") VALUES (1, 1);

-- 插入 milestone 表
INSERT INTO "milestone" (
    "project_id", 
    "start_date", 
    "end_date", 
    "interval"
) VALUES (
    1, 
    '2025-01-01', 
    '2025-06-01', 
    2
);


-- 插入 task 表
INSERT INTO "task" (
    "milestone_id", 
    "name", 
    "description", 
    "start_date", 
    "end_date", 
    "is_completed", 
    "is_deleted"
) VALUES (
    1, 
    'Research AI Algorithms', 
    'Research different AI algorithms for healthcare application.', 
    '2025-01-02', 
    '2025-03-01', 
    false, 
    false
);

-- 插入 subtask 表
INSERT INTO "subtask" (
    "task_id", 
    "name", 
    "days_of_week", 
    "is_completed", 
    "is_deleted"
) VALUES (
    1, 
    'Gather Data', 
    ARRAY['Monday'::day_enum, 'Wednesday'::day_enum, 'Friday'::day_enum], 
    false, 
    false
);

-- 插入 eligibility 表
INSERT INTO "eligibility" (
    "qualifications", 
    "qualification_file_path", 
    "partner_email"
) VALUES (
    'low_income'::qualifications_t, 
    '/path/to/qualification_file.pdf', 
    ARRAY['partner1@example.com', 'partner2@example.com']
);


-- 插入 marathon 表
INSERT INTO "marathon" (
    "event_id", 
    "title", 
    "description", 
    "start_date", 
    "end_date", 
    "registration_status", 
    "people_number", 
    "registration_start_date", 
    "eligibility_id", 
    "is_public", 
    "created_by"
) VALUES (
    '2024S1', 
    'AI Healthcare Marathon', 
    'A marathon focused on healthcare solutions using AI.', 
    '2024-06-01', 
    '2024-06-30', 
    'Open', 
    100, 
    '2024-05-01', 
    1, 
    true, 
    1
);

-- 插入 project_marathon 表
INSERT INTO "project_marathon" (
    "project_id", 
    "marathon_id", 
    "project_registration_date", 
    "status", 
    "feedback"
) VALUES (
    1, 
    1, 
    current_timestamp, 
    'Pending', 
    'Waiting for approval.'
);