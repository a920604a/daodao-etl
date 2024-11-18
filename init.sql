CREATE TYPE "education_stage_t" AS ENUM ('university', 'other', 'high');
CREATE TYPE "tagList_t" AS ENUM ();
CREATE TYPE "role_list_t" AS ENUM (
    'citizen',
    'other',
    'experimental-educator',
    'normal-student',
    'experimental-education-student',
    'parents'
);
CREATE TYPE "recommend_resource_id_list_t" AS ENUM ();
CREATE TYPE "activity_id_list_t" AS ENUM ();
CREATE TABLE "users" (
    "user_id" uuid NOT NULL UNIQUE,
    "birthDay" date,
    "gender" int,
    "education_stage" education_stage_t DEFAULT 'other',
    "tagList" tagList_t [],
    "contact_id" int,
    "location_id" int NOT NULL,
    "nickname" varchar(255),
    "role_list" role_list_t [],
    "is_open_profile" boolean,
    "basic_info_id" int,
    "created_at" TIMESTAMPTZ,
    "created_by" varchar(255),
    "updated_at" TIMESTAMPTZ,
    "updated_by" varchar(255),
    "recommend_resource_id_list" recommend_resource_id_list_t [],
    "activity_id_list" activity_id_list_t [],
    "id" serial UNIQUE,
    PRIMARY KEY(
        "user_id",
        "contact_id",
        "location_id",
        "basic_info_id",
        "id"
    )
);
CREATE TABLE "location" (
    "id" serial NOT NULL UNIQUE,
    "text" varchar(255),
    "is_open_location" boolean,
    PRIMARY KEY("id")
);
CREATE TABLE "contact" (
    "id" serial NOT NULL UNIQUE,
    "google_id" varchar(255),
    "photo_url" text(65535),
    "is_subscribe_email" boolean,
    "email" varchar(255),
    "ig" varchar(255),
    "discord VARCHAR(255)," varchar(255),
    "line" varchar(255),
    "fb" varchar(255),
    PRIMARY KEY("id")
);
CREATE TYPE "interest_list_t" AS ENUM ();
CREATE TYPE "want_to_do_list_t" AS ENUM (
    'interaction ',
    'do-project',
    'find-teacher',
    'find-student',
    'find-group',
    'make-group-class'
);
CREATE TABLE "basic_info" (
    "id" serial NOT NULL UNIQUE,
    "self_introduction" text(65535),
    "interest_list" interest_list_t [],
    "want_to_do_list" want_to_do_list_t,
    PRIMARY KEY("id")
);
CREATE TYPE "category_t" AS ENUM ();
CREATE TYPE "partnerEducationStep_t" AS ENUM ();
CREATE TYPE "partnerStyle_t" AS ENUM ();
CREATE TYPE "tagList_t" AS ENUM ();
CREATE TABLE "activity" (
    "id" serial NOT NULL UNIQUE,
    "title" text(65535),
    "photoURL" varchar(255),
    "photoALT" varchar(255),
    "category" category_t,
    "partnerEducationStep" partnerEducationStep_t,
    "description" varchar(255),
    "area" varchar(255),
    "isGrouping" boolean,
    "updatedDate" date,
    "time" time,
    "partnerStyle" partnerStyle_t,
    "tagList" tagList_t [],
    "createdDate" date,
    "created_at" timestamp,
    "created_by" varchar(255),
    "updated_at" timestamp,
    "updated_by" varchar(255),
    PRIMARY KEY("id")
);
CREATE TYPE "cost_t" AS ENUM ();
CREATE TYPE "tagList_t" AS ENUM ();
CREATE TYPE "age_list_t" AS ENUM ();
CREATE TYPE "type_list_t" AS ENUM ();
CREATE TYPE "filed_name_list_t" AS ENUM ();
CREATE TABLE "resource" (
    "id" serial NOT NULL UNIQUE,
    "image_url" varchar(255),
    "resource_name" varchar(255),
    "cost" cost_t,
    "tagList" tagList_t [],
    "username" varchar(255),
    "age_list" age_list_t [],
    "type_list" type_list_t [],
    "url_link" varchar(255),
    "filed_name_list" filed_name_list_t [],
    "video_url" varchar(255),
    "introduction" text(65535),
    "area" varchar(255),
    "補充資料" text(65535),
    -- 可以為空
    "user_id" uuid,
    PRIMARY KEY("id", "user_id")
);
COMMENT ON COLUMN resource.user_id IS '可以為空';
CREATE TYPE "author_list_t" AS ENUM ();
CREATE TABLE "Store" (
    "id" serial NOT NULL UNIQUE,
    "name" varchar(255),
    "image" blob,
    "author_list" author_list_t [],
    "tags" varchar(255),
    "created_at" timestamp,
    "ai_summary" text(65535),
    "description" text(65535),
    "content" text(65535),
    PRIMARY KEY("id")
);
CREATE TYPE "motivation_t" AS ENUM ();
CREATE TYPE "content_t" AS ENUM ();
CREATE TYPE "goal_t" AS ENUM ();
CREATE TYPE "qualifications_t" AS ENUM ();
CREATE TABLE "project" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid,
    "img_url" varchar(255),
    "topic" varchar(255),
    "project_description" text(65535),
    "motivation" motivation_t [],
    "content" content_t [],
    "goal" goal_t [],
    "policy" text(65535),
    "milestone_id" int,
    "Presentation" text(65535),
    "isPublic" boolean,
    "qualifications" qualifications_t,
    "qualification_file_id" int,
    PRIMARY KEY("id", "user_id", "milestone_id")
);
CREATE TYPE "freqency_t" AS ENUM ();
CREATE TABLE "milestone" (
    "id" serial NOT NULL UNIQUE,
    "isApply" boolean,
    "Durtation" int,
    "freqency" freqency_t,
    "subtask_content" text(65535),
    PRIMARY KEY("id")
);
CREATE TABLE "resource_recommendations" (
    "id" serial NOT NULL UNIQUE,
    "resource_id" int,
    "user_id" uuid,
    "recommended_at" TIMESTAMPTZ,
    PRIMARY KEY("id")
);
CREATE TYPE "role_t" AS ENUM ('Initiator', 'Participant');
CREATE TABLE "user_activities" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid,
    "activity_id" int,
    "role" role_t DEFAULT 'initiator',
    "participated_at" TIMESTAMPTZ,
    PRIMARY KEY("id", "user_id", "activity_id")
);
ALTER TABLE "users"
ADD FOREIGN KEY("location_id") REFERENCES "location"("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "users"
ADD FOREIGN KEY("location_id") REFERENCES "contact"("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "users"
ADD FOREIGN KEY("user_id") REFERENCES "project"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "project"
ADD FOREIGN KEY("milestone_id") REFERENCES "milestone"("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "resource_recommendations"
ADD FOREIGN KEY("resource_id") REFERENCES "resource"("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "users"
ADD FOREIGN KEY("user_id") REFERENCES "resource_recommendations"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "users"
ADD FOREIGN KEY("basic_info_id") REFERENCES "basic_info"("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "user_activities"
ADD FOREIGN KEY("activity_id") REFERENCES "activity"("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "users"
ADD FOREIGN KEY("user_id") REFERENCES "user_activities"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "users"
ADD FOREIGN KEY("nickname") REFERENCES "resource"("username") ON UPDATE NO ACTION ON DELETE NO ACTION;