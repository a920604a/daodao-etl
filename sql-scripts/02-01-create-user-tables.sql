-- Misc TABLE 
CREATE TABLE "area" (
    "id" serial NOT NULL UNIQUE,
    "city" "city_t",
    PRIMARY KEY("id")
);
CREATE INDEX "idx_area_city" ON "area" ("city");
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
    "want_to_do_list" want_to_do_list_t [],
    PRIMARY KEY("id")
);
COMMENT ON COLUMN basic_info.share_list IS 'split(、)';
-- main tables
-- 等待 找夥伴 與 個人名片 resume 規格明確 在作拆分。
CREATE TABLE "user" (
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
    "role" VARCHAR(20) CHECK (role IN ('student', 'assistant', 'backend', 'admin')) NOT NULL,
    "is_open_profile" boolean,
    "birthDay" date,
    "basic_info_id" int,
    "createdDate" TIMESTAMPTZ,
    "updatedDate" TIMESTAMPTZ,
    "created_by" varchar(255),
    "created_at" TIMESTAMPTZ,
    "updated_by" varchar(255),
    "updated_at" TIMESTAMPTZ,
    PRIMARY KEY("id", "uuid"),
    FOREIGN KEY("location_id") REFERENCES "location"("id"),
    FOREIGN KEY("contact_id") REFERENCES "contact"("id"),
    FOREIGN KEY("basic_info_id") REFERENCES "basic_info"("id")
);

COMMENT ON TABLE "user" IS '可能需要維護 熱門標籤列表 到cache';
COMMENT ON COLUMN "user".role_list IS '夥伴類型';
CREATE INDEX "idx_users_education_stage" ON "user" ("education_stage");
CREATE INDEX "idx_users_role_list" ON "user" ("role_list");
CREATE INDEX "idx_users_location_id" ON "user" ("location_id");


-- 找夥伴功能
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user(id) ON DELETE CASCADE,
    nickname VARCHAR(100),
    bio TEXT,
    skills TEXT [],
    interests TEXT [],
    learning_needs TEXT [],
    contact_info JSONB,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 使用者管理, 訂閱方案相關功能, 免費/標準/進階/專業。只會有四筆紀錄
CREATE TABLE subscription_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    features JSONB,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 使用者管理，哪位使用者訂閱了甚麼方案，何時到期
CREATE TABLE user_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user(id) ON DELETE CASCADE,
    plan_id INT REFERENCES subscription_plans(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);