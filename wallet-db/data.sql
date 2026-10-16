BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_user_id TEXT UNIQUE,
    display_name TEXT,
    email TEXT,
    phone_e164 TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS users_email_unique_idx
    ON users (lower(email))
    WHERE email IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS users_phone_unique_idx
    ON users (phone_e164)
    WHERE phone_e164 IS NOT NULL;

CREATE TABLE IF NOT EXISTS roles (
    id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id SMALLINT NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    assigned_by UUID REFERENCES users(id) ON DELETE SET NULL,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_fingerprint_hash TEXT NOT NULL UNIQUE,
    platform TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS devices_user_id_idx ON devices (user_id);

CREATE TABLE IF NOT EXISTS kyc_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_verification_id TEXT UNIQUE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status TEXT NOT NULL,
    decision TEXT,
    reviewed_by UUID REFERENCES users(id) ON DELETE SET NULL,
    review_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    decided_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS kyc_verifications_user_created_idx
    ON kyc_verifications (user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS wallets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_wallet_id TEXT UNIQUE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    kyc_verification_id UUID UNIQUE REFERENCES kyc_verifications(id) ON DELETE RESTRICT,
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS wallets_user_id_idx ON wallets (user_id);

CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_payment_id TEXT UNIQUE,
    payer_wallet_id UUID NOT NULL REFERENCES wallets(id) ON DELETE RESTRICT,
    payment_type TEXT NOT NULL CHECK (payment_type IN ('contact', 'merchant')),
    recipient_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    recipient_reference TEXT,
    recipient_name TEXT,
    merchant_reference TEXT,
    amount NUMERIC(18, 2) NOT NULL CHECK (amount > 0),
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    status TEXT NOT NULL,
    provider_reference TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS payments_wallet_created_idx
    ON payments (payer_wallet_id, created_at DESC);

CREATE INDEX IF NOT EXISTS payments_provider_reference_idx
    ON payments (provider_reference)
    WHERE provider_reference IS NOT NULL;

CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_id UUID NOT NULL REFERENCES wallets(id) ON DELETE RESTRICT,
    payment_id UUID REFERENCES payments(id) ON DELETE RESTRICT,
    provider_transaction_id TEXT UNIQUE,
    entry_type TEXT NOT NULL CHECK (
        entry_type IN ('opening', 'credit', 'debit', 'reserve', 'release', 'settlement', 'reversal')
    ),
    accounting_delta NUMERIC(18, 2) NOT NULL DEFAULT 0,
    reserved_delta NUMERIC(18, 2) NOT NULL DEFAULT 0,
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (accounting_delta <> 0 OR reserved_delta <> 0)
);

CREATE INDEX IF NOT EXISTS transactions_wallet_created_idx
    ON transactions (wallet_id, created_at DESC);

CREATE INDEX IF NOT EXISTS transactions_payment_id_idx
    ON transactions (payment_id)
    WHERE payment_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS qr_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_qr_id TEXT UNIQUE,
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    payload_sha256 CHAR(64) UNIQUE,
    merchant_reference TEXT,
    amount NUMERIC(18, 2) CHECK (amount IS NULL OR amount > 0),
    currency CHAR(3) CHECK (currency IS NULL OR currency ~ '^[A-Z]{3}$'),
    resolved_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL,
    payment_id UUID UNIQUE REFERENCES payments(id) ON DELETE RESTRICT,
    expires_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS qr_sessions_merchant_created_idx
    ON qr_sessions (merchant_reference, created_at DESC)
    WHERE merchant_reference IS NOT NULL;

CREATE TABLE IF NOT EXISTS audit_log (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    actor_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    request_id TEXT,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS audit_log_entity_idx
    ON audit_log (entity_type, entity_id, occurred_at DESC);

CREATE INDEX IF NOT EXISTS audit_log_actor_idx
    ON audit_log (actor_user_id, occurred_at DESC)
    WHERE actor_user_id IS NOT NULL;

INSERT INTO roles (code, name)
VALUES
    ('wallet_user', 'Wallet user'),
    ('merchant', 'Merchant'),
    ('kyc_reviewer', 'KYC reviewer'),
    ('admin', 'Administrator')
ON CONFLICT (code) DO NOTHING;

COMMIT;