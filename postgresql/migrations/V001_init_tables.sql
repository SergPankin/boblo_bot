CREATE TABLE IF NOT EXISTS users (
   user_id     BIGSERIAL PRIMARY KEY,
   tg_login    TEXT
);
 
CREATE TABLE IF NOT EXISTS currencies (
   cur_id     BIGSERIAL PRIMARY KEY,
   cur_name   TEXT
);
 
CREATE TABLE IF NOT EXISTS pairs (
  pair_id       BIGSERIAL PRIMARY KEY,
  main_id       BIGSERIAL,
  secondary_id  BIGSERIAL,
  balance       NUMERIC(9, 2),
  currency_id   BIGSERIAL,
  FOREIGN KEY (main_id) REFERENCES users(user_id),
  FOREIGN KEY (secondary_id) REFERENCES users(user_id),
  FOREIGN KEY (currency_id) REFERENCES currencies(cur_id) 
);
 
CREATE TABLE IF NOT EXISTS transactions (
  transaction_id  BIGSERIAL PRIMARY KEY,
  timestamp       TIMESTAMPTZ,
  from_tp         BIGSERIAL,
  to_tp           BIGSERIAL,
  sum             NUMERIC(9, 2),
  currency_id     BIGSERIAL,
  comment         TEXT,
  FOREIGN KEY (from_tp) REFERENCES users(user_id),
  FOREIGN KEY (to_tp) REFERENCES users(user_id),
  FOREIGN KEY (currency_id) REFERENCES currencies(cur_id) 
);
