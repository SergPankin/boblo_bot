ALTER TABLE users
  ADD COLUMN default_cur BIGSERIAL;

ALTER TABLE users 
ALTER COLUMN default_cur 
  SET DEFAULT 1;

UPDATE users
   SET
    default_cur = 1;
