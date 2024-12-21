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

