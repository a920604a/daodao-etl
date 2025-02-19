CREATE TABLE "project" (
    "id" SERIAL PRIMARY KEY,
    "external_id" UUID DEFAULT gen_random_uuid() UNIQUE, -- 使用 UUID 作为唯一标识符并添加唯一约束
    "user_id" int NOT NULL,
    "img_url" varchar(255),
    "title" varchar(255),
    "description" text,
    "motivation" motivation_t[],
    "motivation_description" text,
    "goal" varchar(255),
    "content" text,
    "strategy" strategy_t[],
    "strategy_description" text,
    -- "resource_name" text[],
    -- "resource_url" text[],
    "resourceName" TEXT,  -- 這邊之後要跟找資源的resource資料表串一起
    "outcome" outcome_t[],
    "outcome_description" text,
    "is_public" boolean DEFAULT false,  -- 是否公開
    "status" varchar(50) DEFAULT 'Not Started' CHECK ("status" IN ('Ongoing', 'Completed', 'Not Started', 'Canceled')),
    "start_date" date, -- 開始日期
    "end_date" date CHECK ("start_date" < "end_date"), -- 結束日期
    "interval" int CHECK ("interval" > 0), -- 週期間隔（單位：週，必須大於 0）
    "created_at" timestamp DEFAULT current_timestamp,
    "created_by" int,
    "updated_at" timestamp DEFAULT current_timestamp,
    "updated_by" int,
    "version" int,
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    UNIQUE ("user_id", "title", "version")
);

CREATE TABLE "user_project" (
    "id" SERIAL PRIMARY KEY,
    "user_external_id" UUID, -- 改为 UUID
    "project_id" int, -- 改为 UUID
    FOREIGN KEY ("user_external_id") REFERENCES "users"("external_id") ON DELETE CASCADE,
    FOREIGN KEY ("project_id") REFERENCES "project"("id") ON DELETE CASCADE
);


-- 創建 milestone 表
CREATE TABLE "milestone" (
    "id" serial PRIMARY KEY,
    "project_id" int, -- 對應的專案 ID
    "week" int , -- 第幾週
    "name" varchar(255), -- 里程碑名稱
    "description" text, -- 里程碑描述
    "start_date" date, -- 開始日期
    "end_date" date CHECK ("start_date" < "end_date"),
    "is_completed" boolean DEFAULT false, -- 是否完成
    "is_deleted" boolean DEFAULT false, -- 是否已刪除
    "created_at" timestamp DEFAULT current_timestamp,
    "updated_at" timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("project_id") REFERENCES "project"("id") ON DELETE CASCADE
);

CREATE INDEX idx_milestone_project_id ON "milestone"("project_id");

-- 創建 task 表
CREATE TYPE "day_enum" AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

CREATE TABLE "task" (
    "id" serial PRIMARY KEY,
    "milestone_id" int NOT NULL, -- 對應的里程碑 ID
    "name" varchar(255), -- 任務名稱
    "description" text, -- 任務描述
    "days_of_week" day_enum[], -- 限定只能存 ENUM 類型值的陣列
    "is_completed" boolean DEFAULT false, -- 是否完成
    "is_deleted" boolean DEFAULT false, -- 是否已刪除
    "created_at" timestamp DEFAULT current_timestamp,
    "updated_at" timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id") ON DELETE CASCADE
);

CREATE INDEX idx_task_milestone_id ON "task"("milestone_id");

-- 通用文章表，包含學習成果、便利貼、覆盤。
CREATE TABLE post (
    "id" SERIAL PRIMARY KEY,
    "study_plan_id" INT REFERENCES project(id) ON DELETE CASCADE,
    "user_id"  INT REFERENCES users(id) ON DELETE CASCADE,
    "type" VARCHAR(20) CHECK (type IN ('outcome', 'note', 'review')) NOT NULL,
    "content" TEXT NOT NULL,
    "date" date NOT NULL, 
    "visibility" VARCHAR(10) CHECK (visibility IN ('public', 'private')) DEFAULT 'private',
    "status" VARCHAR(20) CHECK (status IN ('draft', 'published')) DEFAULT 'draft',
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_posts_study_plan_status ON post(study_plan_id, status);

-- 學習成果(outcome)表
CREATE TABLE outcome (
    id SERIAL PRIMARY KEY,
    post_id INT,
    image_urls TEXT[],  -- 儲存圖片 URL
    video_urls TEXT[] ,  -- 儲存影片 URL
    visibility VARCHAR(10) CHECK (visibility IN ('public', 'private')) DEFAULT 'private',
    created_at timestamp DEFAULT current_timestamp,
    updated_at timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("post_id") REFERENCES "post"("id") ON DELETE CASCADE
);
CREATE INDEX idx_outcome_post_id ON outcome(post_id);


-- 便利貼(note)表。目前便利貼是針對專案相關。
CREATE TABLE note (
    id SERIAL PRIMARY KEY,
    post_id INT,
    image_urls TEXT[],  -- 儲存圖片 URL
    video_urls TEXT[],   -- 儲存影片 URL
    visibility VARCHAR(10) CHECK (visibility IN ('public', 'private')) DEFAULT 'private',
    created_at timestamp DEFAULT current_timestamp,
    updated_at timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("post_id") REFERENCES "post"("id") ON DELETE CASCADE
);
CREATE INDEX idx_note_post_id ON note(post_id);

-- 覆盤
CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    post_id INT,
    mood VARCHAR(20) CHECK (mood IN ('happy', 'calm', 'anxious', 'tired', 'frustrated')) NOT NULL,
    stress_level SMALLINT CHECK (stress_level BETWEEN 1 AND 10) NOT NULL,
    learning_review SMALLINT CHECK (learning_review BETWEEN 1 AND 10) NOT NULL,
    adjustment_plan text, -- 調整與規劃
    visibility VARCHAR(10) CHECK (visibility IN ('public', 'private')) DEFAULT 'private',
    created_at timestamp DEFAULT current_timestamp,
    updated_at timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("post_id") REFERENCES "post"("id") ON DELETE CASCADE
);
CREATE INDEX idx_review_post_id ON review(post_id);

-- 儲存回覆資訊。
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES post(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    visibility VARCHAR(10) CHECK (visibility IN ('public', 'private')) DEFAULT 'private',
    created_at timestamp DEFAULT current_timestamp,
    updated_at timestamp DEFAULT current_timestamp
);
CREATE INDEX idx_comments_post_user ON comments(post_id, user_id);

