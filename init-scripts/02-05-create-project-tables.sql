-- 專案表，使用 UUID 作為外部識別碼，並針對必要欄位加上 NOT NULL 限制
CREATE TABLE "project" (
    "id" SERIAL PRIMARY KEY,
    "external_id" UUID DEFAULT gen_random_uuid() UNIQUE, -- 使用 UUID 作為全局唯一標識符
    "user_id" INT NOT NULL,
    "img_url" VARCHAR(255),
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "motivation" motivation_t[],
    "motivation_description" TEXT,
    "goal" VARCHAR(255),
    "content" TEXT,
    "strategy" strategy_t[],
    "strategy_description" TEXT,
    "resource" TEXT,  -- 未來可與資源資料表串接
    "outcome" outcome_t[],
    "outcome_description" TEXT,
    "is_public" BOOLEAN DEFAULT false,  -- 是否公開
    "status" VARCHAR(50) DEFAULT 'Not Started' CHECK ("status" IN ('Ongoing', 'Completed', 'Not Started', 'Canceled')),
    "start_date" DATE,
    "end_date" DATE CHECK ("start_date" < "end_date"),
    "interval" INT CHECK ("interval" > 0),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "created_by" INT,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_by" INT,
    "version" INT,
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    UNIQUE ("user_id", "title", "version")
);

-- 使用者與專案關聯表，採用id作為使用者與專案的外部識別碼
CREATE TABLE "user_project" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,  -- 參照 users 表的 id
    "project_id" INT NOT NULL,  -- 參照 project 表的 id
    FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
    FOREIGN KEY ("project_id") REFERENCES "project"("id") ON DELETE CASCADE,
    UNIQUE ("user_id", "project_id")
);

-- 里程碑表，規範必要欄位並加上外鍵約束
CREATE TABLE "milestone" (
    "id" SERIAL PRIMARY KEY,
    "project_id" INT NOT NULL, -- 對應的專案 ID
    "week" INT NOT NULL, -- 第幾週（必須為正數）
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL CHECK ("start_date" < "end_date"),
    "is_completed" BOOLEAN DEFAULT false,
    "is_deleted" BOOLEAN DEFAULT false,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("project_id") REFERENCES "project"("id") ON DELETE CASCADE
);

CREATE INDEX idx_milestone_project_id ON "milestone"("project_id");

-- 建立 ENUM 類型，限制天數存入特定星期值
CREATE TYPE "day_enum" AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

-- 任務表，規範必要欄位及外鍵參照
CREATE TABLE "task" (
    "id" SERIAL PRIMARY KEY,
    "milestone_id" INT NOT NULL, -- 對應的里程碑 ID
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "days_of_week" day_enum[] NOT NULL, -- 限定只能存 ENUM 類型值的陣列
    "is_completed" BOOLEAN DEFAULT false,
    "is_deleted" BOOLEAN DEFAULT false,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("milestone_id") REFERENCES "milestone"("id") ON DELETE CASCADE
);

CREATE INDEX idx_task_milestone_id ON "task"("milestone_id");

-- 通用文章表，包含學習成果、便利貼，統一以 project_id 表示所屬專案。
CREATE TABLE "post" (
    "id" SERIAL PRIMARY KEY,
    "project_id" INT NOT NULL REFERENCES "project"("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users"("id") ON DELETE CASCADE,
    "type" VARCHAR(20) NOT NULL CHECK ("type" IN ('outcome', 'note', 'review')),
    "week" INT NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "date" DATE NOT NULL, 
    "visibility" VARCHAR(10) DEFAULT 'private' CHECK ("visibility" IN ('public', 'private')),
    "status" VARCHAR(20) DEFAULT 'draft' CHECK ("status" IN ('draft', 'published')),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_project_status ON "post"("project_id", "status");

-- 學習成果表，針對 post 表類型為 outcome 的文章
CREATE TABLE "outcome" (
    "id" SERIAL PRIMARY KEY,
    "post_id" INT NOT NULL,
    "content" TEXT NOT NULL,
    "image_urls" TEXT[],  -- 儲存圖片 URL
    "video_urls" TEXT[],  -- 儲存影片 URL
    "visibility" VARCHAR(10) DEFAULT 'private' CHECK ("visibility" IN ('public', 'private')),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("post_id") REFERENCES "post"("id") ON DELETE CASCADE
);

CREATE INDEX idx_outcome_post_id ON "outcome"("post_id");

-- 便利貼表，適用於專案相關的便利貼文章
CREATE TABLE "note" (
    "id" SERIAL PRIMARY KEY,
    "post_id" INT NOT NULL,
    "content" TEXT NOT NULL,
    "image_urls" TEXT[],  -- 儲存圖片 URL
    "video_urls" TEXT[],  -- 儲存影片 URL
    "visibility" VARCHAR(10) DEFAULT 'private' CHECK ("visibility" IN ('public', 'private')),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("post_id") REFERENCES "post"("id") ON DELETE CASCADE
);

CREATE INDEX idx_note_post_id ON "note"("post_id");

-- 覆盤表，針對專案進行回顧與調整
CREATE TABLE "review" (
    "id" SERIAL PRIMARY KEY,
    "post_id" INT NOT NULL, 
    "mood" VARCHAR(20) NOT NULL CHECK ("mood" IN ('happy', 'calm', 'anxious', 'tired', 'frustrated')),
    "mood_description" TEXT,
    "stress_level" SMALLINT NOT NULL CHECK ("stress_level" BETWEEN 1 AND 10),
    "learning_review" SMALLINT NOT NULL CHECK ("learning_review" BETWEEN 1 AND 10),
    "learning_feedback" TEXT,
    "adjustment_plan" TEXT, -- 調整與規劃
    "visibility" VARCHAR(10) DEFAULT 'private' CHECK ("visibility" IN ('public', 'private')),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("post_id") REFERENCES "post"("id") ON DELETE CASCADE
);

CREATE INDEX idx_review_project_id ON "review"("project_id");

-- 回覆評論表，存放針對文章的使用者評論
CREATE TABLE "comments" (
    "id" SERIAL PRIMARY KEY,
    "post_id" INT NOT NULL REFERENCES "post"("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users"("id") ON DELETE CASCADE,
    "content" TEXT NOT NULL,
    "visibility" VARCHAR(10) DEFAULT 'private' CHECK ("visibility" IN ('public','private')),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_post_user ON "comments"("post_id", "user_id");
CREATE INDEX idx_comments_visibility ON "comments"("visibility");


CREATE TABLE "likes" (
    "id" SERIAL PRIMARY KEY,
    "post_id" INT REFERENCES posts(id) ON DELETE CASCADE,
    "user_id" INT REFERENCES users(id) ON DELETE CASCADE,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);
CREATE INDEX idx_likes_post_user ON "likes"("post_id", "user_id");
