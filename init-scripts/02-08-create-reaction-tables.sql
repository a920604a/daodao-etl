
-- 定義 reaction_type ENUM，未來可透過 ALTER TYPE 新增值（例如：'happy', 'angry' 等）
CREATE TYPE reaction_type AS ENUM ('like');

-- 互動表
CREATE TABLE "reaction" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "target_type" VARCHAR(50) NOT NULL,
    "target_id" INT NOT NULL,
    "reaction_type" reaction_type NOT NULL,
    "weight" INT DEFAULT 1,  -- 為不同反應賦予不同權重
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE ("user_id", "target_type", "target_id", "reaction_type"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);
CREATE INDEX idx_reaction_user_target ON "reaction"("user_id", "target_type", "target_id");
CREATE INDEX idx_reaction_target ON "reaction"("target_type", "target_id", "reaction_type");

-- 收藏表 (Favorite)
CREATE TABLE "favorite" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "target_type" VARCHAR(50) NOT NULL,
    "target_id" INT NOT NULL,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE ("user_id", "target_type", "target_id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);
CREATE INDEX idx_favorite_user_target ON "favorite"("user_id", "target_type", "target_id");
CREATE INDEX idx_favorite_target ON "favorite"("target_type", "target_id");


-- 瀏覽表 (View)
CREATE TABLE "view" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "target_type" VARCHAR(50) NOT NULL,
    "target_id" INT NOT NULL,
    "duration" INT,  -- 停留時間（秒）
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    UNIQUE ("user_id", "target_type", "target_id")
    -- 此表允許同一使用者對同一對象有多筆記錄
);
CREATE INDEX idx_view_user_target ON "view"("user_id", "target_type", "target_id");
CREATE INDEX idx_view_target ON "view"("target_type", "target_id");


-- 分享表 (Share )
CREATE TABLE "share" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "target_type" VARCHAR(50) NOT NULL,
    "target_id" INT NOT NULL,
    "share_channel" VARCHAR(50),  -- 分享渠道，如社交平台名稱
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    UNIQUE ("user_id", "target_type", "target_id")
);
CREATE INDEX idx_share_user_target ON "share"("user_id", "target_type", "target_id");
CREATE INDEX idx_share_target ON "share"("target_type", "target_id");
CREATE INDEX idx_share_channel ON "share"("share_channel");


-- 點擊表 (Click)
CREATE TABLE "click" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "target_type" VARCHAR(50) NOT NULL,
    "target_id" INT NOT NULL,
    "click_position" VARCHAR(50),  -- 如點擊區域、元素名稱等
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("user_id") REFERENCES "users"("id"),
    UNIQUE ("user_id", "target_type", "target_id")
);

CREATE INDEX idx_click_user_target ON "click"("user_id", "target_type", "target_id");
CREATE INDEX idx_click_target ON "click"("target_type", "target_id");
CREATE INDEX idx_click_position ON "click"("click_position");



-- 主表：記錄整體評分
CREATE TABLE "rating" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "target_type" VARCHAR(50) NOT NULL,
    "target_id" INT NOT NULL,
    "overall_rating" NUMERIC(3,1) NOT NULL CHECK (overall_rating BETWEEN 0 AND 10),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE ("user_id", "target_type", "target_id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);
CREATE INDEX idx_rating_user_target ON "rating"("user_id", "target_type", "target_id");
CREATE INDEX idx_rating_target ON "rating"("target_type", "target_id");

-- 子表：記錄各細項評分，category 可以是 'detail1', 'detail2', 'detail3'
CREATE TABLE "rating_detail" (
    "id" SERIAL PRIMARY KEY,
    "rating_id" INT NOT NULL,  -- 參照主表
    "category" VARCHAR(50) NOT NULL,
    "rating_value" NUMERIC(3,1) NOT NULL CHECK (rating_value BETWEEN 0 AND 10),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("rating_id") REFERENCES "rating"("id")
);
CREATE INDEX idx_rating_detail_rating_id ON "rating_detail"("rating_id");
CREATE INDEX idx_rating_detail_category ON "rating_detail"("category");
