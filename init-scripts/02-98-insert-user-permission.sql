
-- Guest
INSERT INTO "role_permissions" ("role_id", "permission_id") VALUES
(1, 1); -- Guest: 瀏覽頁面

-- User
INSERT INTO "role_permissions" ("role_id", "permission_id") VALUES
(2, 1), -- 瀏覽頁面
(2, 2), -- 聯繫功能
(2, 3), -- 發布揪團
(2, 4); -- 分享資源與心得

-- Participant
INSERT INTO "role_permissions" ("role_id", "permission_id") VALUES
(3, 1), -- 瀏覽頁面
(3, 2), -- 聯繫功能
(3, 3), -- 發布揪團
(3, 4), -- 分享資源與心得
(3, 5); -- 使用學習計畫功能

-- Mentor
INSERT INTO "role_permissions" ("role_id", "permission_id") VALUES
(4, 1), -- 瀏覽頁面
(4, 2), -- 聯繫功能
(4, 3), -- 發布揪團
(4, 4), -- 分享資源與心得
(4, 5), -- 使用學習計畫功能
(4, 6); -- 查詢所有馬拉松參與者資訊

-- Admin
INSERT INTO "role_permissions" ("role_id", "permission_id") VALUES
(5, 1), -- 瀏覽頁面
(5, 2), -- 聯繫功能
(5, 3), -- 發布揪團
(5, 4), -- 分享資源與心得
(5, 5), -- 使用學習計畫功能
(5, 6), -- 查詢所有馬拉松參與者資訊
(5, 7); -- 查看所有資料

-- SuperAdmin
INSERT INTO "role_permissions" ("role_id", "permission_id") VALUES
(6, 1), -- 瀏覽頁面
(6, 2), -- 聯繫功能
(6, 3), -- 發布揪團
(6, 4), -- 分享資源與心得
(6, 5), -- 使用學習計畫功能
(6, 6), -- 查詢所有馬拉松參與者資訊
(6, 7), -- 查看所有資料
(6, 8); -- 修改、刪除所有資料


INSERT INTO users (
    external_id,
    mongo_id,
    nickname,
    role_id
) VALUES (
    gen_random_uuid(),
    1,
    'SuperAdmin',
    6
);


-- insert mentor's user_id mapping player user_id