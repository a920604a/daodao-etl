CREATE TABLE "groups" (
    "id" SERIAL PRIMARY KEY,
    "external_id" UUID DEFAULT gen_random_uuid() UNIQUE, -- 使用 UUID 作为唯一标识符并添加唯一约束
    "title" TEXT,
    "photo_url" VARCHAR(255),
    "photo_alt" VARCHAR(255),
    "category" group_category_t[],
    "group_type" group_type_t[] ,
    "partner_education_step" partner_education_step_t[],
    "description" VARCHAR(255),
    "city_id" INT, -- 需改成 city_id, FOREIGN key city
    "is_grouping" BOOLEAN,
    "created_date" TIMESTAMPTZ,
    "updated_date" TIMESTAMPTZ,
    "time" TEXT,
    "partner_style" TEXT,
    "created_at" TIMESTAMPTZ,
    "created_by" INT,
    "updated_at" TIMESTAMPTZ,
    "updated_by" VARCHAR(255),
    "motivation" TEXT,
    "contents" TEXT,
    "expectation_result" TEXT,
    "notice" TEXT,
    "tag_list" TEXT[],
    "group_deadline" TIMESTAMPTZ,
    "is_need_deadline" BOOLEAN,
    "participator" INT,
    "hold_time" time,
    "is_online" BOOLEAN,
    "TBD" BOOLEAN,
    FOREIGN KEY("created_by") REFERENCES "users"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY("city_id") REFERENCES "city"("id") ON UPDATE CASCADE ON DELETE SET NULL
    
);
COMMENT ON TABLE "groups" IS 'need to normalize 需要維護 熱門學習領域 ';
COMMENT ON COLUMN "groups".category IS '學習領域 split(,)';
COMMENT ON COLUMN "groups".city_id IS 'split(,)';
CREATE INDEX "idx_group_is_grouping" ON "groups" ("is_grouping");
CREATE INDEX "idx_group_partner_education_step" ON "groups" ("partner_education_step");
CREATE INDEX "idx_group_group_type" ON "groups" ("group_type");
CREATE INDEX "idx_group_city_id" ON "groups" ("city_id");
CREATE INDEX "idx_group_is_online" ON "groups" ("is_online");
CREATE INDEX "idx_group_TBD" ON "groups" ("TBD");

CREATE TABLE "user_join_group" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT,
    "group_id" INT,
    "group_participation_role_t" group_participation_role_t DEFAULT 'Initiator',
    "participated_at" TIMESTAMPTZ,
    FOREIGN KEY("group_id") REFERENCES "groups"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX idx_user_group ON "user_join_group" ("user_id", "group_id");
