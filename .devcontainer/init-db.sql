CREATE TABLE IF NOT EXISTS voters (
    voter_id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    has_token BOOLEAN DEFAULT FALSE,
    has_voted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS tokens (
    voter_id TEXT PRIMARY KEY REFERENCES voters(voter_id),
    token_hash TEXT,
    signature TEXT
);

CREATE TABLE IF NOT EXISTS ballots (
    ballot_id TEXT PRIMARY KEY,
    candidate TEXT,
    token_hash TEXT,
    encrypted BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS mixnet_proofs (
    id SERIAL PRIMARY KEY,
    layer INT,
    input_count INT,
    output_count INT,
    proof_hash TEXT
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    message TEXT,
    log_type TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create admin user (full privileges)
CREATE ROLE admin_user WITH LOGIN PASSWORD 'admin_secure_password';
GRANT ALL PRIVILEGES ON DATABASE voting_db TO admin_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_user;
-- Allow admin to create future tables/sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin_user;

-- Create read-only user (for read-only services, e.g., tally display or logs viewer)
CREATE ROLE read_only_user WITH LOGIN PASSWORD 'read_secure_password';
GRANT CONNECT ON DATABASE voting_db TO read_only_user;
GRANT USAGE ON SCHEMA public TO read_only_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO read_only_user;
-- For future tables/sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read_only_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO read_only_user;

-- Voter registration role (for adding/updating voters and tokens)
CREATE ROLE voter_reg_user WITH LOGIN PASSWORD 'voter_secure_password';
GRANT CONNECT ON DATABASE voting_db TO voter_reg_user;
GRANT USAGE ON SCHEMA public TO voter_reg_user;
GRANT SELECT, INSERT, UPDATE ON voters TO voter_reg_user;
GRANT SELECT, INSERT, UPDATE ON tokens TO voter_reg_user;
GRANT USAGE, SELECT ON SEQUENCE logs_id_seq TO voter_reg_user;  -- For logging
GRANT INSERT ON logs TO voter_reg_user;
-- Defaults for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO voter_reg_user;  -- Note: Limited in comment, but applied broadly for simplicity; restrict if needed

-- Ballot casting role (for VotingAuthority: verify tokens, add ballots)
CREATE ROLE ballot_cast_user WITH LOGIN PASSWORD 'ballot_secure_password';
GRANT CONNECT ON DATABASE voting_db TO ballot_cast_user;
GRANT USAGE ON SCHEMA public TO ballot_cast_user;
GRANT SELECT ON voters TO ballot_cast_user;  -- To check status
GRANT SELECT ON tokens TO ballot_cast_user;  -- To verify
GRANT INSERT ON ballots TO ballot_cast_user;
GRANT UPDATE ON voters TO ballot_cast_user;  -- To mark has_voted
GRANT USAGE, SELECT ON SEQUENCE logs_id_seq TO ballot_cast_user;
GRANT INSERT ON logs TO ballot_cast_user;

-- Mixnet role (for shuffling and proofs)
CREATE ROLE mixnet_user WITH LOGIN PASSWORD 'mixnet_secure_password';
GRANT CONNECT ON DATABASE voting_db TO mixnet_user;
GRANT USAGE ON SCHEMA public TO mixnet_user;
GRANT SELECT, UPDATE ON ballots TO mixnet_user;  -- To get/shuffle (update encrypted flag if needed)
GRANT INSERT ON mixnet_proofs TO mixnet_user;
GRANT USAGE, SELECT ON SEQUENCE mixnet_proofs_id_seq TO mixnet_user;
GRANT USAGE, SELECT ON SEQUENCE logs_id_seq TO mixnet_user;
GRANT INSERT ON logs TO mixnet_user;

-- Logging-only role (if you have a separate logging service)
CREATE ROLE logger_user WITH LOGIN PASSWORD 'log_secure_password';
GRANT CONNECT ON DATABASE voting_db TO logger_user;
GRANT USAGE ON SCHEMA public TO logger_user;
GRANT INSERT ON logs TO logger_user;
GRANT USAGE, SELECT ON SEQUENCE logs_id_seq TO logger_user;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    scopes TEXT DEFAULT 'admin'
);

-- Revoked tokens table (store jti values)
CREATE TABLE IF NOT EXISTS revoked_tokens (
    jti TEXT PRIMARY KEY,
    revoked_at TIMESTAMP DEFAULT NOW()
);