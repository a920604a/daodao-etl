-- 插入主分類
INSERT INTO categories (name, name_en, description, parent_id) VALUES
('自然與環境', 'Nature and Environment', '涉及自然科學、生物學、環境保護等領域，提供了解地球與生態系統運作的學習資源。', NULL),
('數理邏輯', 'Math and Logic', '包括數學、邏輯學、統計學等基礎知識，助於提升解決問題的能力，並應用於各領域。', NULL),
('人文史地', 'Humanities, History, and Geography', '探索人類歷史、地理及文化的資源，了解各地的發展、傳統和全球社會結構。', NULL);


-- 插入子分類
INSERT INTO categories (name, name_en, description, parent_id) VALUES
-- 自然與環境子分類
('地球科學', 'Earth Science', '涉及地球的結構、氣候、地質等，學習地球的運作與演變過程，理解自然災害與全球變化。', 1),
('物理', 'Physics', '研究物質與能量的相互作用，涵蓋力學、熱力學、光學、電磁學等基礎理論與應用。', 1),
('生物', 'Biology', '涉及生命科學的各個方面，學習生物的結構、功能、演化與生態系統的運作。', 1),
('化學', 'Chemistry', '研究物質的性質、結構及變化，學習化學反應、元素與化合物的相互作用。', 1),
('環境', 'Environment', '探討環境問題、可持續發展與生態保護，學習如何維護自然環境與生物多樣性。', 1),
('自然資源與保育', 'Natural Resources and Conservation', '研究自然資源的利用與保護，涵蓋水資源、土地、能源等的可持續管理與保護措施。', 1),
('農業', 'Agriculture', '涉及農作物栽培、農業技術及可持續農業發展，探索提高農業生產力與資源利用效率的方法。', 1);
