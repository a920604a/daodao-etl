CREATE TABLE "likes" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid NOT NULL,
    "target_type" varchar(50) NOT NULL, -- 'group' 或 'resource'
    "target_id" int NOT NULL, -- group.id 或 resource.id
    "liked_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id"),
    FOREIGN KEY("user_id") REFERENCES "user"("uuid"),
    -- 注意：根據 target_type 動態檢查外鍵無法直接用外鍵約束，但可以在應用層處理
    CHECK ("target_type" IN ('group', 'resource'))
);
COMMENT ON COLUMN "likes".target_type IS '可選 group 或 resource';

CREATE TABLE "favorites" (
    "id" serial NOT NULL UNIQUE,
    "user_id" uuid NOT NULL,
    "target_type" varchar(50) NOT NULL, -- 'group' 或 'resource'
    "target_id" int NOT NULL, -- group.id 或 resource.id
    "favorited_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id"),
    FOREIGN KEY("user_id") REFERENCES "user"("uuid"),
    CHECK ("target_type" IN ('group', 'resource'))
);
COMMENT ON COLUMN "favorites".target_type IS '可選 group 或 resource';



CREATE TABLE "follows" (
    "follower_id" uuid NOT NULL,
    "followee_id" uuid NOT NULL,
    "followed_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("follower_id", "followee_id"),
    FOREIGN KEY("follower_id") REFERENCES "user"("uuid") ON DELETE CASCADE,
    FOREIGN KEY("followee_id") REFERENCES "user"("uuid") ON DELETE CASCADE
);
COMMENT ON TABLE "follows" IS '用於記錄使用者之間的追蹤關係';

CREATE INDEX idx_likes_user_target ON "likes" ("user_id", "target_type");
CREATE INDEX idx_favorites_user_target ON "favorites" ("user_id", "target_type");
CREATE INDEX idx_follows_followee ON "follows" ("followee_id");
