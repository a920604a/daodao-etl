-- Misc TABLE 
CREATE TABLE "city" (
    "id" SERIAL PRIMARY KEY,  
    "name" "city_t"
);
CREATE INDEX "idx_city_name" ON "city" ("name");
CREATE TABLE "country" (
    id SERIAL PRIMARY KEY,          -- 唯一識別碼
    alpha2 CHAR(2) ,        -- ISO 3166-1 alpha-2 代碼
    alpha3 CHAR(3) ,        -- ISO 3166-1 alpha-3 代碼
    name VARCHAR(100) NOT NULL     -- 國家名稱
);
-- 確保唯一性約束
CREATE UNIQUE INDEX idx_country_alpha2 ON country(alpha2);
CREATE UNIQUE INDEX idx_country_alpha3 ON country(alpha3);


CREATE TABLE "location" (
    "id" SERIAL PRIMARY KEY,
    "city_id" INT,
    "country_id" INT,
    "isTaiwan" BOOLEAN,
    FOREIGN KEY ("city_id") REFERENCES "city"("id"),
    FOREIGN KEY ("country_id") REFERENCES "country"("id")
);

-- 添加索引以提高查詢性能
CREATE INDEX idx_location_city_id ON "location"("city_id");
CREATE INDEX idx_location_country_id ON "location"("country_id");


CREATE TABLE "contacts" (
    "id" SERIAL PRIMARY KEY,
    "google_id" VARCHAR(255),
    "photo_url" TEXT,
    "is_subscribe_email" BOOLEAN,
    "email" VARCHAR(255),
    "ig" VARCHAR(255),
    "discord" VARCHAR(255),
    "line" VARCHAR(255),
    "fb" VARCHAR(255)
);
CREATE TABLE "basic_info" (
    "id" SERIAL PRIMARY KEY,
    "self_introduction" TEXT,
    "share_list" TEXT,
    "want_to_do_list" want_to_do_list_t []
);
COMMENT ON COLUMN basic_info.share_list IS 'split(、)';


-- main tables
-- 等待 找夥伴 與 個人名片 resume 規格明確 在作拆分。
CREATE TABLE "users" (
    "id" SERIAL PRIMARY KEY,
    "external_id" UUID DEFAULT gen_random_uuid() UNIQUE, -- 使用 UUID 作为唯一标识符并添加唯一约束
    "mongo_id" TEXT NOT NULL UNIQUE,
    "gender" gender_t,
    "language" VARCHAR(255),
    "education_stage" education_stage_t DEFAULT 'other',
    "tag_list" TEXT[],
    "contact_id" INT,
    "is_open_location" BOOLEAN,
    "location_id" INT,
    "nickname" VARCHAR(255),
    "role_id" INT NOT NULL,   -- 關聯角色ID
    "is_open_profile" BOOLEAN,
    "birth_date" DATE,
    "basic_info_id" INT,
    "createdDate" TIMESTAMPTZ,
    "updatedDate" TIMESTAMPTZ,
    "created_by" VARCHAR(255),
    "created_at" TIMESTAMPTZ,
    "updated_by" VARCHAR(255),
    "updated_at" TIMESTAMPTZ,
    FOREIGN KEY("location_id") REFERENCES "location"("id"),
    FOREIGN KEY("contact_id") REFERENCES "contacts"("id"),
    FOREIGN KEY("basic_info_id") REFERENCES "basic_info"("id"),
    FOREIGN KEY ("role_id") REFERENCES "roles" ("id") -- 關聯角色表
);

COMMENT ON TABLE "users" IS '可能需要維護 熱門標籤列表 到cache';
-- COMMENT ON COLUMN "users".identity_list IS '夥伴類型';
CREATE INDEX "idx_users_education_stage" ON "users" ("education_stage");
-- CREATE INDEX "idx_users_on_identity_list" ON "users" ("identity_list");
CREATE INDEX "idx_users_location_id" ON "users" ("location_id");

CREATE TABLE "role_permissions" (
    "role_id" INT NOT NULL,                  -- 關聯角色ID
    "permission_id" INT NOT NULL,            -- 關聯權限ID
    PRIMARY KEY("role_id", "permission_id"),
    FOREIGN KEY("role_id") REFERENCES "roles"("id"),
    FOREIGN KEY("permission_id") REFERENCES "permissions"("id")
);


-- 新增用戶和身份的聯接表
CREATE TABLE "user_positions" (
    "user_id" INT NOT NULL,
    "position_id" INT NOT NULL,
    PRIMARY KEY ("user_id", "position_id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    FOREIGN KEY ("position_id") REFERENCES "position"("id")
);

-- 用於管理 個別用戶 的 額外權限 或 限制權限，即覆蓋預設角色權限的功能。
CREATE TABLE "user_permissions" ( 
    "user_id" INT NOT NULL,                  -- 關聯用戶ID
    "permission_id" INT NOT NULL,            -- 關聯權限ID
    PRIMARY KEY("user_id", "permission_id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id"),
    FOREIGN KEY("permission_id") REFERENCES "permissions"("id")
);



-- 找夥伴功能
-- 雖然數組設計簡潔，但對於需要精細化查詢的情況可能會有性能問題
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
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

CREATE INDEX "idx_user_profiles_is_public" ON user_profiles(is_public);



-- 使用者管理, 訂閱方案相關功能, 免費/標準/進階/專業。只會有四筆紀錄
CREATE TABLE subscription_plan (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    features JSONB,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TYPE subscription_status AS ENUM ('active', 'inactive', 'canceled');
-- 使用者管理，哪位使用者訂閱了甚麼方案，何時到期
CREATE TABLE user_subscription (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    plan_id INT REFERENCES subscription_plan(id) ON DELETE SET NULL,
    status subscription_status NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_user_subscription_user_status ON user_subscription (user_id, status);

-- 增加臨時註冊使用者，儲存第一次註冊登入的資料
CREATE TABLE temp_users (
    id SERIAL PRIMARY KEY,
    google_id VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    photo_url VARCHAR(255),
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP 
);
