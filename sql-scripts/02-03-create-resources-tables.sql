CREATE TABLE "resources" (
    "id" serial NOT NULL UNIQUE,
    "created_by_user_id" INT UNIQUE,
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
    PRIMARY KEY("id"),
    FOREIGN KEY ("created_by_user_id") REFERENCES "users"("id") 
);

COMMENT ON TABLE resources IS '後端需要判斷 不同人剛好分享同一的資源(例如：同時分享島島主站) 標籤 與 領域名稱 需要維護, username = users table nickname';
COMMENT ON COLUMN resources."tagList" IS 'split()';
CREATE INDEX "idx_resource_cost" ON "resources" ("cost");
CREATE INDEX "idx_resource_age" ON "resources" ("age");



-- 用來紀錄心得分享與評價關係的表
CREATE TABLE "resource_review" (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    resource_id INT REFERENCES resources(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    likes_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 用來紀錄分享關係的表
CREATE TABLE "resource_share" (
    "resource_id" INT NOT NULL,
    "user_id" INT NOT NULL,
    "shared_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("resource_id", "user_id"),
    FOREIGN KEY ("resource_id") REFERENCES "resources"("id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);

-- 用來紀錄收藏關係的表
CREATE TABLE "resource_favorite" (
    "resource_id" int NOT NULL,
    "user_id" INT NOT NULL,
    "favorited_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("resource_id", "user_id"),
    FOREIGN KEY ("resource_id") REFERENCES "resources"("id"),
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);

-- 用來紀錄推薦關係的表
CREATE TABLE "resource_recommendations" (
    "id" serial NOT NULL UNIQUE,
    "user_id" INT NOT NULL,
    "resource_id" int,
    "recommended_at" TIMESTAMPTZ,
    PRIMARY KEY("id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id"),
    FOREIGN KEY ("resource_id" ) REFERENCES "resources"("id")
);

CREATE TABLE "resource_post" (
    "id" serial NOT NULL UNIQUE,
    "rating_total" int,
    "rating_content_content" int,
    "rating_resources_practical" int,
    "content" text,
    "created_by" INT,
    FOREIGN KEY("created_by") REFERENCES "users"("id")
);
