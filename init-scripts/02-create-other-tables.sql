CREATE TABLE "group" (
    "id" serial NOT NULL UNIQUE,
    "title" text,
    "photoURL" varchar(255),
    "photoALT" varchar(255),
    "category" text,
    "group_type" group_type_t DEFAULT 'other',
    "partnerEducationStep" "partnerEducationStep_t" DEFAULT 'other',
    "description" varchar(255),
    "area_id" int,
    "isGrouping" boolean,
    "updatedDate" date,
    "time" time,
    "partnerStyle" text,
    "created_at" timestamp,
    "created_by" uuid,
    "updated_at" timestamp,
    "updated_by" varchar(255),
    "motivation" text,
    "Contents" text,
    "expectation_result" text,
    "Notice" text,
    "tagList" text,
    "group_daedline" date,
    "hold_time" time,
    "isOnline" boolean,
    "TBD" boolean,
    PRIMARY KEY("id"),
    FOREIGN KEY("created_by") REFERENCES "user"("uuid") ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE "group" IS 'need to normalize 需要維護 熱門學習領域 ';
COMMENT ON COLUMN "group".category IS '學習領域 split(,)';
COMMENT ON COLUMN "group".area_id IS 'split(,)';
CREATE INDEX "idx_group_isGrouping" ON "group" ("isGrouping");
CREATE INDEX "idx_group_partnerEducationStep" ON "group" ("partnerEducationStep");
CREATE INDEX "idx_group_group_type" ON "group" ("group_type");
CREATE INDEX "idx_group_area_id" ON "group" ("area_id");
CREATE INDEX "idx_group_isOnline" ON "group" ("isOnline");
CREATE INDEX "idx_group_TBD" ON "group" ("TBD");


CREATE TABLE "resource" (
    "created_by_user_id" uuid UNIQUE,
    "image_url" varchar(255),
    "resource_name" varchar(255),
    "cost" cost_t DEFAULT 'free',
    "tagList" text,
    "username" varchar(255),
    "age" age_t,
    "type_list" text,
    "url_link" varchar(255),
    "filed_name_list" text,
    "video_url" varchar(255),
    "introduction" text,
    "area" varchar(255),
    "supplement" text,
    "id" serial NOT NULL UNIQUE,
    PRIMARY KEY("id"),
    FOREIGN KEY ("created_by_user_id") REFERENCES "user"("uuid")
);

COMMENT ON TABLE resource IS '後端需要判斷 不同人剛好分享同一的資源(例如：同時分享島島主站) 標籤 與 領域名稱 需要維護, username = user table nickname';
COMMENT ON COLUMN resource."tagList" IS 'split()';
CREATE INDEX "idx_resource_cost" ON "resource" ("cost");
CREATE INDEX "idx_resource_age" ON "resource" ("age");


-- 用來紀錄分享關係的表
CREATE TABLE "resource_share" (
    "resource_id" int NOT NULL,
    "user_id" uuid NOT NULL,
    "shared_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("resource_id", "user_id"),
    FOREIGN KEY ("resource_id") REFERENCES "resource"("id"),
    FOREIGN KEY ("user_id") REFERENCES "user"("uuid")
);

-- 用來紀錄收藏關係的表
CREATE TABLE "resource_favorite" (
    "resource_id" int NOT NULL,
    "user_id" uuid NOT NULL,
    "favorited_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("resource_id", "user_id"),
    FOREIGN KEY ("resource_id") REFERENCES "resource"("id"),
    FOREIGN KEY ("user_id") REFERENCES "user"("uuid")
);

CREATE TABLE "resource_recommendations" (
    "id" serial NOT NULL UNIQUE,
    "uuid" uuid,
    "resource_id" int,
    "recommended_at" TIMESTAMPTZ,
    PRIMARY KEY("id"),
    FOREIGN KEY("uuid") REFERENCES "user"("uuid"),
    FOREIGN KEY ("resource_id" ) REFERENCES "resource"("id")
);


CREATE TABLE "Store" (
    "id" serial NOT NULL UNIQUE,
    "uuid" uuid UNIQUE,
    "image_url" varchar(255),
    "author_list" text,
    "tags" varchar(255),
    "created_at" timestamp,
    "ai_summary" text,
    "description" text,
    "content" text,
    "name" varchar(255),
    PRIMARY KEY("id")
);


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
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id")
);

-- Subtask 表
CREATE TABLE "subtask" (
    "id" serial PRIMARY KEY,
    "task_id" int NOT NULL,
    "name" varchar(255),
    "is_deleted" boolean DEFAULT false,
    FOREIGN KEY ("task_id") REFERENCES "task"("id")
);

-- Subtask Schedule 表
CREATE TABLE "subtask_schedule" (
    "id" serial PRIMARY KEY,
    "subtask_id" int NOT NULL,
    "day_of_week" varchar(10), -- e.g., 'Monday', 'Wednesday'
    FOREIGN KEY ("subtask_id") REFERENCES "subtask"("id")
);



CREATE TABLE "project" (
    "id" serial PRIMARY KEY,
    "user_id" int NOT NULL,
    "img_url" varchar(255),
    "topic" varchar(255),
    "project_description" text,
    "motivation" varchar(255)[],
    "motivation_description" text,
    "goal" varchar(255),
    "content" text,
    "policy" varchar(255)[],
    "policy_description" text,
    "resource_name" text[],
    "resource_url" text[],
    "milestone_id" int,
    "presentation" varchar(255)[],
    "presentation_description" text,
    "is_public" boolean DEFAULT false,  -- 是否公開
    "status" varchar(50) CHECK ("status" IN ('Ongoing', 'Completed', 'Not Started', 'Canceled')), -- 活動狀態
    "created_at" timestamp DEFAULT current_timestamp,
    "created_by" int,
    "updated_at" timestamp DEFAULT current_timestamp,
    "updated_by" int,
    FOREIGN KEY ("user_id") REFERENCES "user"("id"),
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id")
);



CREATE TABLE "eligibility" (
    "id" serial NOT NULL UNIQUE,
    "qualifications" qualifications_t,
    "qualification_file_path" VARCHAR(255),
    "partner_email" text[]
);

CREATE TABLE "marathon" (
    "id" serial PRIMARY KEY,
    "event_id" varchar(50) NOT NULL UNIQUE, -- 活動代碼，例如 "2024S1"
    "title" varchar(255) NOT NULL, -- 活動標題
    "description" text, -- 活動描述
    "start_date" date NOT NULL, -- 馬拉松的報名開始日期。
    "end_date" date NOT NULL, -- 活動結束日期
    "registration_status" varchar(50) CHECK ("registration_status" IN ('Open', 'Closed', 'Pending', 'Full')), -- 活動的整體報名狀態。
    "registration_start_date" date, -- 報名開放日期
    "eligibility_id" int, -- 收費計劃
    "is_public" boolean DEFAULT false, -- 是否公開
    "created_by" int, -- 主辦者 (可選)
    "created_at" timestamp DEFAULT current_timestamp,
    "updated_at" timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("eligibility_id") REFERENCES "eligibility"("id"),
    FOREIGN KEY ("created_by") REFERENCES "user"("id") -- 若需要記錄主辦者
);
CREATE INDEX idx_marathon_start_date ON "marathon"("start_date");



CREATE TABLE "project_marathon" (
    "id" serial PRIMARY KEY,
    "project_id" int NOT NULL, -- 專案 ID
    "marathon_id" int NOT NULL, -- 馬拉松 ID
    "project_registration_date" timestamp DEFAULT current_timestamp, -- 某個專案報名此馬拉松的日期。
    "status" varchar(50) CHECK ("status" IN ('Pending', 'Approved', 'Rejected')), -- 專案報名的審核狀態
    "feedback" text, -- 評審意見或備註
    "created_at" timestamp DEFAULT current_timestamp,
    "updated_at" timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("project_id") REFERENCES "project"("id") ON DELETE CASCADE,
    FOREIGN KEY ("marathon_id") REFERENCES "marathon"("id") ON DELETE CASCADE,
    UNIQUE ("project_id", "marathon_id") -- 保證同一專案不能重複報名同一馬拉松
);

CREATE INDEX idx_project_marathon_status ON "project_marathon"("status");

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




