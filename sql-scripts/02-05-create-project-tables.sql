-- Milestone 表
CREATE TABLE "milestone" (
    "id" serial PRIMARY KEY,
    "is_apply" boolean,
    "start_date" date,
    "end_date" date
   );

-- Task 表
CREATE TABLE "task" (
    "id" serial PRIMARY KEY,
    "milestone_id" int NOT NULL,
    "name" varchar(255),
    "start_date" date,
    "end_date" date,
    "is_completed" boolean DEFAULT false,
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id")
);

-- Subtask 表
CREATE TYPE "day_enum" AS ENUM ('周一', '周二', '周三', '周四', '周五', '周六', '周日');

CREATE TABLE "subtask" (
    "id" serial PRIMARY KEY,
    "task_id" int NOT NULL,
    "name" varchar(255),
    "days_of_week" day_enum[], -- 限定只能存 ENUM 類型值的陣列
    FOREIGN KEY ("task_id") REFERENCES "task"("id")
);


CREATE TABLE "project" (
    "id" serial PRIMARY KEY,
    "user_id" int NOT NULL,
    "img_url" varchar(255),
    "topic" varchar(255),
    "project_description" text,
    "motivation" motivation_t[],
    "motivation_description" text,
    "goal" varchar(255),
    "content" text,
    "policy" policy_t[],
    "policy_description" text,
    "resource_name" text[],
    "resource_url" text[],
    "milestone_id" int UNIQUE, -- 確保里程碑 ID 只與一個專案關聯
    "presentation" presentation_t[],
    "presentation_description" text,
    "is_public" boolean DEFAULT false,  -- 是否公開
    "status" varchar(50) DEFAULT 'Not Started' CHECK ("status" IN ('Ongoing', 'Completed', 'Not Started', 'Canceled')),
    "created_at" timestamp DEFAULT current_timestamp,
    "created_by" int,
    "updated_at" timestamp DEFAULT current_timestamp,
    "updated_by" int,
    FOREIGN KEY ("user_id") REFERENCES "user"("id"),
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id")
);


CREATE TABLE "user_project" (
    "id" serial NOT NULL UNIQUE,
    "user_uuid" uuid,
    "project_id" int,
    PRIMARY KEY("id"),
    FOREIGN KEY ("user_uuid") REFERENCES "user" ("uuid") ON DELETE CASCADE,
    FOREIGN KEY ("project_id") REFERENCES "project" ("id") ON DELETE CASCADE
);

CREATE TABLE "user_join_group" (
    "id" serial NOT NULL UNIQUE,
    "uuid" uuid,
    "group_id" int,
    "role" role_t DEFAULT 'Initiator',
    "participated_at" TIMESTAMPTZ,
    PRIMARY KEY("id"),
    FOREIGN KEY("group_id") REFERENCES "group"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);




