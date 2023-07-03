CREATE INDEX IF NOT EXISTS from_user_idx ON transactions (from_tp);
CREATE INDEX IF NOT EXISTS to_user_idx ON transactions (to_tp);

CREATE INDEX IF NOT EXISTS currency_idx ON transactions (currency_id);
