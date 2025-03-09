UPDATE users
SET role_id = 3
WHERE contact_id = (SELECT id FROM contacts WHERE email = 'username@gmail.com');