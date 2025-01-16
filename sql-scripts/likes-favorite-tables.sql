CREATE TABLE "likes" (
    "id" serial NOT NULL UNIQUE,
    "post_id" INT REFERENCES posts(id) ON DELETE CASCADE,
    "user_id" INT REFERENCES users(id) ON DELETE CASCADE,
    "target_type" varchar(50) NOT NULL, -- 'group' 或 'resource'
    "target_id" int NOT NULL, -- group.id 或 resource.id
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY("user_id") REFERENCES "user"("id"),
    -- 注意：根據 target_type 動態檢查外鍵無法直接用外鍵約束，但可以在應用層處理
    CHECK ("target_type" IN ('group', 'resource'))
    PRIMARY KEY(post_id, user_id)

);
COMMENT ON COLUMN "likes".target_type IS '可選 group 或 resource';

CREATE TABLE "favorites" (
    "user_id" INT REFERENCES users(id) ON DELETE CASCADE,
    "target_type" varchar(50) NOT NULL, -- 'group' 或 'resource'
    "target_id" int NOT NULL, -- group.id 或 resource.id
    "favorited_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("user_id", "target_id"),
    FOREIGN KEY("user_id") REFERENCES "user"("id"),
    CHECK ("target_type" IN ('group', 'resource'))
);
COMMENT ON COLUMN "favorites".target_type IS '可選 group 或 resource';



CREATE TABLE "follows" (
    "follower_id" INT NOT NULL,
    "followee_id" INT NOT NULL,
    "followed_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("follower_id", "followee_id"),
    FOREIGN KEY("follower_id") REFERENCES "user"("id") ON DELETE CASCADE,
    FOREIGN KEY("followee_id") REFERENCES "user"("id") ON DELETE CASCADE
);
COMMENT ON TABLE "follows" IS '用於記錄使用者之間的追蹤關係';

CREATE INDEX idx_likes_user_target ON "likes" ("user_id", "target_type");
CREATE INDEX idx_favorites_user_target ON "favorites" ("user_id", "target_type");
CREATE INDEX idx_follows_followee ON "follows" ("followee_id");


-- 通用文章表，包含學習成果、便利貼、覆盤。
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    study_plan_id INT REFERENCES project(id) ON DELETE CASCADE,
    user_id  INT REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) CHECK (type IN ('learning_outcome', 'sticky_note', 'review')) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('draft', 'published')) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_posts_study_plan_status ON posts(study_plan_id, status);


CREATE TABLE learning_outcomes (
    post_id INT PRIMARY KEY REFERENCES posts(id) ON DELETE CASCADE,
    image_urls TEXT[],  -- 儲存圖片 URL
    video_urls TEXT[]   -- 儲存影片 URL
);
CREATE TABLE sticky_notes (
    post_id INT PRIMARY KEY REFERENCES posts(id) ON DELETE CASCADE,
    image_urls TEXT[],  -- 儲存圖片 URL
    video_urls TEXT[]   -- 儲存影片 URL
);

CREATE TABLE reviews (
    post_id INT PRIMARY KEY REFERENCES posts(id) ON DELETE CASCADE,
    mood VARCHAR(20) CHECK (mood IN ('happy', 'calm', 'anxious', 'tired', 'depressed')) NOT NULL,
    stress_level SMALLINT CHECK (stress_level BETWEEN 1 AND 10) NOT NULL,
    study_reflection SMALLINT CHECK (study_reflection BETWEEN 1 AND 10) NOT NULL
);


-- 儲存回覆資訊。
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
CREATE INDEX idx_comments_post_user ON comments(post_id, user_id);
