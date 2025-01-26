CREATE TABLE "project" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- 使用 UUID 作为主键
    "user_id" int NOT NULL,
    "img_url" varchar(255),
    "topic" varchar(255),
    "description" text,
    "motivation" motivation_t[],
    "motivation_description" text,
    "goal" varchar(255),
    "content" text,
    "policy" policy_t[],
    "policy_description" text,
    "resource_name" text[],
    "resource_url" text[],
    "presentation" presentation_t[],
    "presentation_description" text,
    "is_public" boolean DEFAULT false,  -- 是否公開
    "status" varchar(50) DEFAULT 'Not Started' CHECK ("status" IN ('Ongoing', 'Completed', 'Not Started', 'Canceled')),
    "created_at" timestamp DEFAULT current_timestamp,
    "created_by" int,
    "updated_at" timestamp DEFAULT current_timestamp,
    "updated_by" int,
    "version" int,
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);

CREATE TABLE "user_project" (
    "id" serial NOT NULL UNIQUE,
    "user_external_id" UUID, -- 改为 UUID
    "project_id" UUID, -- 改为 UUID
    PRIMARY KEY("id"),
    FOREIGN KEY ("user_external_id") REFERENCES "users"("external_id") ON DELETE CASCADE,
    FOREIGN KEY ("project_id") REFERENCES "project"("id") ON DELETE CASCADE
);


CREATE TABLE "milestone"(
    "id" serial PRIMARY KEY,
    "project_id" UUID NOT NULL, -- 改为 UUID    "project_id" int NOT NULL, -- 專案 ID
    "start_date" date, -- 開始日期
    "end_date" date CHECK ("start_date" < "end_date"), -- 結束日期
    "interval" int CHECK ("interval" > 0), -- 週期間隔（單位：週，必須大於 0）
    FOREIGN KEY ("project_id") REFERENCES "project"("id") ON DELETE CASCADE
);

CREATE TABLE "task" (
    "id" serial PRIMARY KEY,
    "milestone_id" int NOT NULL, -- 對應的里程碑 ID
    "name" varchar(255), -- 任務名稱
    "description" text, -- 任務描述
    "start_date" date, -- 開始日期
    "end_date" date, -- 結束日期
    "is_completed" boolean DEFAULT false, -- 是否完成，可能需要檢查所有subtask 是否完成
    "is_deleted" boolean DEFAULT false, -- 是否已刪除，預設為 false
    "created_at" timestamp DEFAULT current_timestamp,
    "updated_at" timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id") ON DELETE CASCADE

);
CREATE INDEX idx_task_milestone_id ON "task"("milestone_id");


-- Subtask 表
CREATE TYPE "day_enum" AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

CREATE TABLE "subtask" (
    "id" serial PRIMARY KEY,
    "task_id" int NOT NULL,
    "name" varchar(255),
    "description" text,
    "days_of_week" day_enum[], -- 限定只能存 ENUM 類型值的陣列
    "is_completed" boolean DEFAULT false, -- 是否完成，預設為 false，用於進度條使用
    "is_deleted" boolean DEFAULT false, -- 是否已刪除，預設為 false
    FOREIGN KEY ("task_id") REFERENCES "task"("id")
);




