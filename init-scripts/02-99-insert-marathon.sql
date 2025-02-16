
INSERT INTO "fee_plans" (fee_plan_type, name, discount)
VALUES
    ('low_income'::qualifications_t, 'Student Discount', 0.00),
    ('discount'::qualifications_t, 'Personal Early Plan', 6000.00),
    ('personal'::qualifications_t,  'Standard Plan', 8000.00),
    ('double'::qualifications_t, 'Couple Discount', 10000.00),
    ('three'::qualifications_t, 'Three Plan', 12000.00),
    ('four'::qualifications_t, 'Family Plan', 12000.00);

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
    "registration_end_date", 
    "is_public", 
    "created_by"
) VALUES (
    '2025S1', 
    'Daodao Marathon', 
    'Helps you create a personalized learning plan.', 
    '2025-02-09', 
    '2025-07-12', 
    'Open', 
    20, 
    '2024-12-15',
    '2025-01-19',  
    true, 
    1
);