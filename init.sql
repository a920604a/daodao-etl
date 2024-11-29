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
CREATE TABLE "users" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid NOT NULL UNIQUE,
    "gender" gender_t,
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
    "created_by" varchar(255),
    "created_at" TIMESTAMPTZ,
    "updated_by" varchar(255),
    "updated_at" TIMESTAMPTZ,
    PRIMARY KEY("id")
);
COMMENT ON TABLE users IS '可能需要維護 熱門標籤列表 到cache';
COMMENT ON COLUMN users.role_list IS '夥伴類型';
CREATE INDEX "users_index_0" ON "users" ("education_stage");
CREATE INDEX "users_index_1" ON "users" ("role_list");
CREATE INDEX "users_index_2" ON "users" ("location_id");
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
CREATE TABLE "area" (
    "id" serial NOT NULL UNIQUE,
    "City" "City_t",
    PRIMARY KEY("id")
);
CREATE INDEX "location_index_0" ON "area" ("City");
CREATE TABLE "contact" (
    "id" serial NOT NULL UNIQUE,
    "google_id" varchar(255),
    "photo_url" text,
    "is_subscribe_email" boolean,
    "email" varchar(255),
    "ig" varchar(255),
    "discord VARCHAR(255)," varchar(255),
    "line" varchar(255),
    "fb" varchar(255),
    PRIMARY KEY("id")
);
CREATE TYPE "want_to_do_list_t" AS ENUM (
    'interaction',
    'do-project',
    'make-group-class',
    'find-student',
    'find-teacher',
    'find-group'
);
CREATE TABLE "basic_info" (
    "id" serial NOT NULL UNIQUE,
    "self_introduction" text,
    -- split('、')
    "share_list" text,
    "want_to_do_list" want_to_do_list_t,
    "user_id" uuid,
    PRIMARY KEY("id")
);
COMMENT ON COLUMN basic_info.share_list IS 'split(、)';
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
CREATE TABLE "group" (
    "id" serial NOT NULL UNIQUE,
    "title" text,
    "photoURL" varchar(255),
    "photoALT" varchar(255),
    "category" text,
    "group_type" group_type_t DEFAULT 'other',
    "partnerEducationStep" "partnerEducationStep_t" DEFAULT 'other',
    "description" varchar(255),
    -- split(',')
    "area_id" int,
    "isGrouping" boolean,
    "updatedDate" date,
    "time" time,
    "partnerStyle" text,
    "tagList" text,
    "created_at" timestamp,
    "created_by" uuid,
    "updated_at" timestamp,
    "updated_by" varchar(255),
    "motivation" text,
    "Contents" text,
    "expectation_result" text,
    "Notice" text,
    "group_daedline" date,
    "hold_time" time,
    "isOnline" boolean,
    "TBD" boolean,
    PRIMARY KEY("id"),
    FOREIGN KEY("created_by") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE "group" IS 'need to normalize 需要維護 熱門學習領域 ';
COMMENT ON COLUMN "group".category IS '學習領域 split(,)';
COMMENT ON COLUMN "group".area_id IS 'split(,)';
CREATE INDEX "activity_index_0" ON "group" ("isGrouping");
CREATE INDEX "activity_index_1" ON "group" ("partnerEducationStep");
CREATE INDEX "activity_index_2" ON "group" ("group_type");
CREATE INDEX "group_index_3" ON "group" ("area_id");
CREATE INDEX "group_index_4" ON "group" ("isOnline");
CREATE INDEX "group_index_5" ON "group" ("TBD");
CREATE TYPE "cost_t" AS ENUM ('free', 'part', 'payment');
CREATE TYPE "age_t" AS ENUM ('preschool', 'Elementary', 'high', 'University');
CREATE TABLE "resource" (
    "created_by_user_id" uuid UNIQUE,
    "image_url" varchar(255),
    "resource_name" varchar(255),
    "cost" cost_t DEFAULT 'free',
    -- split()
    "tagList" text,
    "username" varchar(255),
    "age" age_t,
    "type_list" text,
    "url_link" varchar(255),
    "filed_name_list" text,
    "video_url" varchar(255),
    "introduction" text,
    "area" varchar(255),
    "補充資料" text,
    "id" serial NOT NULL UNIQUE,
    PRIMARY KEY("id")
);
COMMENT ON TABLE resource IS '後端需要判斷 不同人剛好分享同一的資源(例如：同時分享島島主站) 標籤 與 領域名稱 需要維護';
COMMENT ON COLUMN resource."tagList" IS 'split()';
CREATE INDEX "resource_index_0" ON "resource" ("cost");
CREATE INDEX "resource_index_1" ON "resource" ("age");
CREATE TABLE "Store" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid UNIQUE,
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
CREATE TYPE "motivation_t" AS ENUM (
    'other',
    'Challenge',
    'Interested and enthusiastic',
    'curiosity',
    'Progression'
);
CREATE TYPE "policy_t" AS ENUM ('book reading', 'materials');
CREATE TYPE "qualifications_t" AS ENUM (
    'low income',
    'discount',
    'personal',
    'double',
    'three',
    'four'
);
CREATE TABLE "project" (
    "id" serial NOT NULL UNIQUE,
    "img_url" varchar(255),
    "topic" varchar(255),
    "project_description" text,
    "motivation" motivation_t [],
    "content" text,
    "goal" varchar(255),
    "policy" policy_t [],
    "milestone_id" int,
    "Presentation" text,
    "isPublic" boolean,
    "qualifications" qualifications_t,
    "qualification_file_id" int,
    "created_at" timestamp,
    "created_by" int,
    "updated_at" timestamp,
    "updated_by" int,
    PRIMARY KEY("id")
);
CREATE TYPE "freqency_t" AS ENUM ('three', 'month', 'two', 'one');
CREATE TABLE "milestone" (
    "id" serial NOT NULL UNIQUE,
    "isApply" boolean,
    "Durtation" int,
    "freqency" freqency_t DEFAULT 'one',
    "subtask_content" text,
    PRIMARY KEY("id")
);
CREATE TABLE "user_project" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid,
    "project_id" int,
    PRIMARY KEY("id"),
    FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("project_id") REFERENCES "project" ("id") ON DELETE CASCADE
);
CREATE TYPE "role_t" AS ENUM ('Initiator', 'Participant');
CREATE TABLE "user_join_group" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid,
    "group_id" int,
    "role" role_t DEFAULT 'Initiator',
    "participated_at" TIMESTAMPTZ,
    PRIMARY KEY("id"),
    FOREIGN KEY("group_id") REFERENCES "group"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE "resource_recommendations" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid,
    "resource_id" int,
    "recommended_at" TIMESTAMPTZ,
    PRIMARY KEY("id")
);
CREATE TABLE "location" (
    "id" serial NOT NULL UNIQUE,
    "area_id" int,
    "isTaiwan" boolean,
    "region" char(64),
    PRIMARY KEY("id")
);
ALTER TABLE "user_join_group"
ADD FOREIGN KEY("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "area"
ADD FOREIGN KEY("id") REFERENCES "location"("area_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "location"
ADD FOREIGN KEY("id") REFERENCES "users"("location_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "contact"
ADD FOREIGN KEY("id") REFERENCES "users"("contact_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "basic_info"
ADD FOREIGN KEY("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "resource_recommendations"
ADD FOREIGN KEY("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "resource"
ADD FOREIGN KEY("id") REFERENCES "resource_recommendations"("resource_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "resource"
ADD FOREIGN KEY("username") REFERENCES "users"("nickname") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "milestone"
ADD FOREIGN KEY("id") REFERENCES "project"("milestone_id") ON UPDATE NO ACTION ON DELETE NO ACTION;