CREATE TABLE "store" (
    "id" SERIAL PRIMARY KEY,
    "external_id" UUID DEFAULT gen_random_uuid() UNIQUE, -- 使用 UUID 作为唯一标识符并添加唯一约束
    "user_id" INT UNIQUE,
    "image_url" varchar(255),
    "author_list" text,
    "tags" varchar(255),
    "created_at" timestamp DEFAULT current_timestamp,
    "ai_summary" text,
    "description" text,
    "content" text,
    "name" varchar(255),
    FOREIGN KEY ("user_id") REFERENCES "users"("id")
);