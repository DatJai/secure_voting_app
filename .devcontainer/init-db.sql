CREATE TABLE IF NOT EXISTS voters (
    voter_id TEXT PRIMARY KEY,
    name TEXT,
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
