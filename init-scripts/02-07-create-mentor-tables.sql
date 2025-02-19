CREATE TABLE mentor_participants (
    mentor_id INT NOT NULL, -- 指向 users 表中 role_id = 4 (Mentor) 的 id。
    participant_id INT NOT NULL, -- 指向 users 表中 role_id = 3 (Participant) 的 id。
    PRIMARY KEY (mentor_id, participant_id),
    FOREIGN KEY (mentor_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (participant_id) REFERENCES users(id) ON DELETE CASCADE
);
