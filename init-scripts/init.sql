
-- TYPE

CREATE TYPE "gender_t" AS ENUM ('male', 'female', 'other');
CREATE TYPE "education_stage_t" AS ENUM ('university', 'high', 'other');
CREATE TYPE "role_list_t" AS ENUM (
    'normal-student',
    'citizen',
    'experimental-educator',
    'other',
    'parents',
    'experimental-education-student'
);

CREATE TYPE "City_t" AS ENUM (
    'Taipei City',
    'Keelung City',
    'New Taipei City',
    'Lianjiang County',
    'Taoyuan City',
    'Hsinchu City',
    'Hsinchu County',
    'Miaoli County',
    'Taichung City',
    'Changhua County',
    'Yunlin County',
    'Chiayi County',
    'Chiayi City',
    'Tainan City',
    'nantou county',
    'kaohsiung city',
    'Pingtung County',
    'Hainan Island',
    'Penghu County',
    'Kinmen County',
    'Yilan County',
    'Hualien County',
    'Taitung County',
    'Other'
);


CREATE TYPE "want_to_do_list_t" AS ENUM (
    'interaction',
    'do-project',
    'make-group-class',
    'find-student',
    'find-teacher',
    'find-group'
);

CREATE TYPE "group_type_t" AS ENUM (
    'reading club',
    'workshop',
    'project',
    'competition',
    'Activity',
    'Societies',
    'course',
    'practice',
    'other'
);
CREATE TYPE "partnerEducationStep_t" AS ENUM ('high school', 'other', 'University');


CREATE TYPE "cost_t" AS ENUM ('free', 'part', 'payment');
CREATE TYPE "age_t" AS ENUM ('preschool', 'Elementary', 'high', 'University');


CREATE TYPE "freqency_t" AS ENUM ( 'two', 'one', 'three', 'month');

CREATE TYPE "qualifications_t" AS ENUM (
    'low_income',
    'discount',
    'personal',
    'double',
    'three',
    'four'
    
);
CREATE TABLE "eligibility" (
    "id" serial NOT NULL UNIQUE,
    "qualifications" qualifications_t,
    "qualification_file_path" VARCHAR(255)

);

CREATE TYPE "role_t" AS ENUM ('Initiator', 'Participant');


CREATE TYPE "motivation_t" AS ENUM (
    'driven_by_curiosity',
    'interest_and_passion',
    'self_challenge',
    'personal_growth',
    'career_development',
    'pursuing_education_or_qualifications',
    'social_recognition',
    'exploring_possibilities',
    'preparing_for_the_future',
    'innovation_and_development',
    'practical_needs',
    'inspired_by_events',
    'interpersonal_connections',
    'life_changes',
    'impact_on_society',
    'influenced_by_a_group',
    'others'
);

CREATE TYPE "policy_t" AS ENUM (
    'data_collection_research_analysis',
    'book_reading',
    'watching_videos',
    'listening_to_podcasts',
    'examinations',
    'participating_in_competitions',
    'finding_study_partners',
    'joining_communities',
    'consulting_experts_and_scholars',
    'doing_projects',
    'initiating_actions',
    'field_internship',
    'organizing_events_or_courses',
    'attending_events_or_courses',
    'field_research',
    'conducting_interviews',
    'conducting_surveys',
    'others'
);
CREATE TYPE "presentation_t" AS ENUM (
    'building_websites',
    'managing_social_media',
    'writing_research_reports',
    'artistic_creation',
    'initiating_projects_or_organizations',
    'making_videos',
    'organizing_events',
    'teaching_courses',
    'participating_in_competitions',
    'others'
);


-- Misc TABLE 
CREATE TABLE "area" (
    "id" serial NOT NULL UNIQUE,
    "City" "City_t",
    PRIMARY KEY("id")
);
CREATE INDEX "idx_area_city" ON "area" ("City");

CREATE TABLE "location" (
    "id" serial NOT NULL UNIQUE,
    "area_id" int,
    "isTaiwan" boolean,
    "region" char(64),
    PRIMARY KEY("id"),
    FOREIGN KEY ("area_id") REFERENCES "area"("id")
);

CREATE TABLE "contact" (
    "id" serial NOT NULL UNIQUE,
    "google_id" varchar(255),
    "photo_url" text,
    "is_subscribe_email" boolean,
    "email" varchar(255),
    "ig" varchar(255),
    "discord" varchar(255),
    "line" varchar(255),
    "fb" varchar(255),
    PRIMARY KEY("id")
);
CREATE TABLE "basic_info" (
    "id" serial NOT NULL UNIQUE,
    "self_introduction" text,
    "share_list" text,
    "want_to_do_list" want_to_do_list_t[],
    "uuid" uuid,
    PRIMARY KEY("id")
);
COMMENT ON COLUMN basic_info.share_list IS 'split(、)';


CREATE TABLE "users" (
    "id" serial NOT NULL UNIQUE,
    "_id" text NOT NULL UNIQUE,
    "uuid" uuid NOT NULL UNIQUE,
    "gender" gender_t,
    "language" VARCHAR(255),
    "education_stage" education_stage_t DEFAULT 'other',
    "tagList" text,
    "contact_id" int,
    "is_open_location" boolean,
    "location_id" int,
    "nickname" varchar(255),
    "role_list" role_list_t [],
    "is_open_profile" boolean,
    "birthDay" date,
    "basic_info_id" int,
    "createdDate" TIMESTAMPTZ,
    "updatedDate" TIMESTAMPTZ,
    "created_by" varchar(255),
    "created_at" TIMESTAMPTZ,
    "updated_by" varchar(255),
    "updated_at" TIMESTAMPTZ,
    PRIMARY KEY("uuid"),
    FOREIGN KEY("location_id") REFERENCES "location"("id"),
    FOREIGN KEY("contact_id") REFERENCES "contact"("id"),
    FOREIGN KEY("basic_info_id") REFERENCES "basic_info"("id")
);

COMMENT ON TABLE users IS '可能需要維護 熱門標籤列表 到cache';
COMMENT ON COLUMN users.role_list IS '夥伴類型';

CREATE INDEX "idx_users_education_stage" ON "users" ("education_stage");
CREATE INDEX "idx_users_role_list" ON "users" ("role_list");
CREATE INDEX "idx_users_location_id" ON "users" ("location_id");



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
    FOREIGN KEY("created_by") REFERENCES "users"("uuid") ON UPDATE NO ACTION ON DELETE NO ACTION
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
    FOREIGN KEY ("created_by_user_id") REFERENCES "users"("uuid")
);

COMMENT ON TABLE resource IS '後端需要判斷 不同人剛好分享同一的資源(例如：同時分享島島主站) 標籤 與 領域名稱 需要維護, username = users table nickname';
COMMENT ON COLUMN resource."tagList" IS 'split()';
CREATE INDEX "idx_resource_cost" ON "resource" ("cost");
CREATE INDEX "idx_resource_age" ON "resource" ("age");
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
    "is_public" boolean DEFAULT false,
    "eligibility_id" int,
    "created_at" timestamp DEFAULT current_timestamp,
    "created_by" int,
    "updated_at" timestamp DEFAULT current_timestamp,
    "updated_by" int,
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id"),
    FOREIGN KEY ("eligibility_id") REFERENCES "eligibility"("id")
);


CREATE TABLE "marathon" (
    "id" serial PRIMARY KEY,
    "event_id" varchar(50) NOT NULL UNIQUE, -- 活動代碼，例如 "2024S1"
    "title" varchar(255) NOT NULL, -- 活動標題
    "description" text, -- 活動描述
    "start_date" date NOT NULL, -- 活動開始日期
    "end_date" date NOT NULL, -- 活動結束日期
    "status" varchar(50) CHECK ("status" IN ('Ongoing', 'Completed', 'Not Started', 'Canceled')), -- 活動狀態
    "registration_status" varchar(50) CHECK ("registration_status" IN ('Open', 'Closed', 'Pending', 'Full')), -- 報名狀態
    "registration_date" date, -- 報名開放日期
    "pricing" jsonb, -- 收費計劃，JSON 格式
    "is_public" boolean DEFAULT false, -- 是否公開
    "created_at" timestamp DEFAULT current_timestamp,
    "updated_at" timestamp DEFAULT current_timestamp
);



CREATE TABLE "user_project" (
    "id" serial NOT NULL UNIQUE,
    "user_uuid" uuid,
    "project_id" int,
    PRIMARY KEY("id"),
    FOREIGN KEY ("user_uuid") REFERENCES "users" ("uuid") ON DELETE CASCADE,
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
CREATE TABLE "resource_recommendations" (
    "id" serial NOT NULL UNIQUE,
    "uuid" uuid,
    "resource_id" int,
    "recommended_at" TIMESTAMPTZ,
    PRIMARY KEY("id"),
    FOREIGN KEY("uuid") REFERENCES "users"("uuid"),
    FOREIGN KEY ("resource_id" ) REFERENCES "resource"("id")
);




