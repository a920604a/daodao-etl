CREATE TABLE "Store" (
    "id" serial NOT NULL UNIQUE,
    "uuid" uuid UNIQUE,
    "image_url" varchar(255),
    "author_list" text,
    "tags" varchar(255),
    "created_at" timestamp,
    "ai_summary" text,
    "description" text,
    "content" text,
    "name" varchar(255),
    PRIMARY KEY("id")
);
