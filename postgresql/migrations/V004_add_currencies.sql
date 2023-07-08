INSERT INTO currencies (cur_id, cur_name)
VALUES
  (1, 'KZT'),
  (2, 'RUB'),
  (3, 'KGS'),
  (4, 'USD'),
  (5, 'EUR')
ON CONFLICT (cur_id) DO UPDATE
  SET
    cur_name = EXCLUDED.cur_name;
