
-- 學習相關大分類
---學習相關小分類
---分類可以用在學習資源、揪團、學習計畫

CREATE TABLE "category" (
    "id" SERIAL PRIMARY KEY,       -- 分類唯一 ID
    "name" TEXT NOT NULL,          -- 分類名稱
    "parent_id" INT DEFAULT NULL,  -- 指向父分類的 ID
    "level" INT NOT NULL DEFAULT 1,-- 分類層級，1: 第一層, 2: 第二層
    "created_at" TIMESTAMP DEFAULT NOW(), -- 創建時間
    "updated_at" TIMESTAMP DEFAULT NOW()  -- 更新時間
);

