CREATE TABLE "groups" (
    "id" SERIAL PRIMARY KEY,
    "external_id" UUID DEFAULT gen_random_uuid() UNIQUE, -- 使用 UUID 作为唯一标识符并添加唯一约束
    "title" text,
    "photo_url" varchar(255),
    "photo_alt" varchar(255),
    "category" group_category_t[],
    "group_type" group_type_t[] ,
    "partner_education_step" partner_education_step_t[],
    "description" varchar(255),
    "city_id" int[], -- 需改成 city_id, FOREIGN key city
    "is_grouping" boolean,
    "created_date" TIMESTAMPTZ,
    "updated_date" TIMESTAMPTZ,
    "time" text,
    "partner_style" text,
    "created_at" TIMESTAMPTZ,
    "created_by" INT,
    "updated_at" TIMESTAMPTZ,
    "updated_by" varchar(255),
    "motivation" text,
    "contents" text,
    "expectation_result" text,
    "notice" text,
    "tag_list" text,
    "group_deadline" TIMESTAMPTZ,
    "hold_time" time,
    "is_online" boolean,
    "TBD" boolean,
    FOREIGN KEY("created_by") REFERENCES "users"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
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
    "user_id" int,
    "group_id" int,
    "group_participation_role_t" group_participation_role_t DEFAULT 'Initiator',
    "participated_at" TIMESTAMPTZ,
    FOREIGN KEY("group_id") REFERENCES "groups"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX idx_user_group ON "user_join_group" ("user_id", "group_id");
