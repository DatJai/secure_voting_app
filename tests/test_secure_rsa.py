import services.secure_rsa as sr


def test_sign_verify_roundtrip():
    rsa = sr.SecureRSA(bit_length=256)
    pub, priv = rsa.generate_keys()
    msg = "unit test message"
    sig = rsa.sign(msg)
    h = sr.SecureRSA.hash_message(msg)
    decrypted = pow(sig, rsa.public_key["e"], rsa.public_key["n"])
    assert decrypted == h % rsa.public_key["n"]


def test_blind_sign_unblind():
    rsa = sr.SecureRSA(bit_length=256)
    pub, priv = rsa.generate_keys()
    msg = "blind message"
    blinded, r = rsa.blind(msg)
    blinded_sig = rsa.sign_blind(blinded)
    signature = rsa.unblind(blinded_sig, r)
    h = sr.SecureRSA.hash_message(msg)
    decrypted = pow(signature, rsa.public_key["e"], rsa.public_key["n"])
    assert decrypted == h % rsa.public_key["n"]


def test_verify_hash():
    rsa = sr.SecureRSA(bit_length=256)
    pub, priv = rsa.generate_keys()
    msg = "hash-verify"
    sig = rsa.sign(msg)
    h = sr.SecureRSA.hash_message(msg)
    decrypted = pow(sig, rsa.public_key["e"], rsa.public_key["n"])
    assert decrypted == h % rsa.public_key["n"]
