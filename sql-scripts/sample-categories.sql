-- https://docs.google.com/spreadsheets/d/1oLtML8oZtZuzk8AKD7G0_NBXGZDyBMZv3ThNSwVlXE0/edit?gid=0#gid=0

CREATE TABLE categories (
    id SERIAL PRIMARY KEY, -- 分類 ID
    name TEXT NOT NULL, -- 分類名稱 (如: "自然與環境", "褲子地球科學", "醫藥與運動")
    name_en VARCHAR(255),
    parent_id INT REFERENCES categories(id) ON DELETE CASCADE, -- 上層分類 ID (用於階層分類)
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
