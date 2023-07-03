INSERT INTO currencies (cur_id, cur_name)
VALUES
  (1, 'KZT'),
  (2, 'RUB'),
  (3, 'KGS')
ON CONFLICT (cur_id) DO UPDATE
  SET
    cur_name = EXCLUDED.cur_name;
