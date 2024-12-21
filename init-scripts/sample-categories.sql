CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,      -- 商品 ID
    name VARCHAR(255) NOT NULL,        -- 商品名稱
    description TEXT,                  -- 商品描述
    price DECIMAL(10, 2) NOT NULL,     -- 價格
    stock INT DEFAULT 0,               -- 庫存數量
    created_at TIMESTAMP DEFAULT NOW(),-- 創建時間
    updated_at TIMESTAMP DEFAULT NOW() -- 更新時間
);
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,    -- 分類 ID
    name VARCHAR(255) UNIQUE NOT NULL, -- 分類名稱 (如: "藍色", "褲子", "牛子")
    parent_id INT DEFAULT NULL,        -- 上層分類 ID (用於階層分類)
    FOREIGN KEY (parent_id) REFERENCES categories(category_id)
);

CREATE TABLE product_categories (
    product_id INT NOT NULL,           -- 商品 ID
    category_id INT NOT NULL,          -- 分類 ID
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);
