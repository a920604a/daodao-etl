 CREATE TABLE "eligibility" (
    "id" serial NOT NULL UNIQUE,
    "qualifications" qualifications_t,
    "qualification_file_path" VARCHAR(255),
    "partner_email" text[]
);

CREATE TABLE "marathon" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- 使用 UUID 作为主键
    "event_id" varchar(50) NOT NULL UNIQUE, -- 活動代碼，例如 "2024S1"
    "title" varchar(255) NOT NULL, -- 活動標題
    "description" text, -- 活動描述
    "start_date" date NOT NULL, -- 馬拉松的報名開始日期。
    "end_date" date NOT NULL, -- 活動結束日期
    "registration_status" varchar(50) CHECK ("registration_status" IN ('Open', 'Closed', 'Pending', 'Full')), -- 活動的整體報名狀態。
    "people_number" INT, -- 報名人數上限 
    "registration_start_date" date, -- 報名開放日期
    "eligibility_id" int, -- 收費計劃
    "is_public" boolean DEFAULT false, -- 是否公開
    "created_by" int, -- 主辦者 (可選)
    "created_at" timestamp DEFAULT current_timestamp,
    "updated_at" timestamp DEFAULT current_timestamp,
    FOREIGN KEY ("eligibility_id") REFERENCES "eligibility"("id"),
    FOREIGN KEY ("created_by") REFERENCES "users"("id") -- 若需要記錄主辦者
);
CREATE INDEX idx_marathon_start_date ON "marathon"("start_date");



CREATE TABLE "project_marathon" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- 使用 UUID 作为主键
    "project_id" UUID NOT NULL, -- 專案 ID，改为 UUID
    "marathon_id" UUID NOT NULL, -- 馬拉松 ID，改为 UUID
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
