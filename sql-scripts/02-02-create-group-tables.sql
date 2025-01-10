CREATE TABLE "group" (
    "id" serial NOT NULL UNIQUE,
    "title" text,
    "photoURL" varchar(255),
    "photoALT" varchar(255),
    "category" text,
    "group_type" group_type_t DEFAULT 'other',
    "partnerEducationStep" "partnerEducationStep_t" DEFAULT 'other',
    "description" varchar(255),
    "area_id" int,
    "isGrouping" boolean,
    "updatedDate" date,
    "time" time,
    "partnerStyle" text,
    "created_at" timestamp,
    "created_by" uuid,
    "updated_at" timestamp,
    "updated_by" varchar(255),
    "motivation" text,
    "Contents" text,
    "expectation_result" text,
    "Notice" text,
    "tagList" text,
    "group_daedline" date,
    "hold_time" time,
    "isOnline" boolean,
    "TBD" boolean,
    PRIMARY KEY("id"),
    FOREIGN KEY("created_by") REFERENCES "user"("uuid") ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE "group" IS 'need to normalize 需要維護 熱門學習領域 ';
COMMENT ON COLUMN "group".category IS '學習領域 split(,)';
COMMENT ON COLUMN "group".area_id IS 'split(,)';
CREATE INDEX "idx_group_isGrouping" ON "group" ("isGrouping");
CREATE INDEX "idx_group_partnerEducationStep" ON "group" ("partnerEducationStep");
CREATE INDEX "idx_group_group_type" ON "group" ("group_type");
CREATE INDEX "idx_group_area_id" ON "group" ("area_id");
CREATE INDEX "idx_group_isOnline" ON "group" ("isOnline");
CREATE INDEX "idx_group_TBD" ON "group" ("TBD");



CREATE TABLE "user_join_group" (
    "id" serial NOT NULL UNIQUE,
    "uuid" uuid,
    "group_id" int,
    "role" role_t DEFAULT 'Initiator',
    "participated_at" TIMESTAMPTZ,
    PRIMARY KEY("id"),
    FOREIGN KEY("group_id") REFERENCES "group"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
    FOREIGN KEY("uuid") REFERENCES "user"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);