-- idea上有標題，文字，圖片，影片，還有多個簡易學習資源的資料，學習資源上有名稱，連結，配圖，類型(主要分類與子分類)，影響力評分，自訂tag
CREATE TABLE "idea" (
    "id" SERIAL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "content" TEXT,
    "image_urls" TEXT[],  -- 儲存圖片 URL
    "video_urls" TEXT[],  -- 儲存影片 URL
    "visibility" VARCHAR(10) DEFAULT 'private' CHECK ("visibility" IN ('public', 'private')),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE "learning_resource" (
    "id" SERIAL PRIMARY KEY,
    "idea_id" INT NOT NULL,  -- 連結到 idea
    "name" VARCHAR(255) NOT NULL,
    "url" TEXT NOT NULL,
    "image_url" TEXT,  -- 配圖
    "category_id" INT NOT NULL REFERENCES "categories"("id"),  -- 直接關聯 categories 表
    "impact_score" INT CHECK ("impact_score" BETWEEN 1 AND 100),  -- 影響力評分
    "custom_tags" TEXT[],  -- 自訂 tag
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("idea_id") REFERENCES "idea"("id") ON DELETE CASCADE
);
