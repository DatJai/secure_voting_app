import crypto.hashing as ch
import crypto.rng as cr


def test_sha256_hex_matches_utils():
    s = "test-string-123"
    # hashing.sha256_hex should match direct hashlib behavior
    assert ch.sha256_hex(s) == __import__(
        "hashlib").sha256(s.encode()).hexdigest()


def test_get_random_hex_length():
    h = cr.get_random_hex(16)
    # token_hex(16) returns 32 hex chars
    assert isinstance(h, str)
    assert len(h) == 32
