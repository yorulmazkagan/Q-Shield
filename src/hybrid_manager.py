import hashlib

def get_hybrid_key(qkd_key, pqc_key):
    # KFinal = SHA-256(KQKD || KPQC)
    combined = qkd_key + pqc_key
    return hashlib.sha256(combined).hexdigest()