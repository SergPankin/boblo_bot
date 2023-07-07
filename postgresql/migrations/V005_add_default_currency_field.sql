ALTER TABLE users
  ADD COLUMN default_cur NOT NULL;

ALTER TABLE users 
ALTER COLUMN default_cur 
  SET DEFAULT 1;

UPDATE users
   SET
    default_cur = 1;

