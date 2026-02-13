import os
import ctypes

# Kütüphane dosyasının tam yerini gösteriyoruz
lib_path = "/home/yorulmazkagan/Projects/Turkcell/Q-Shield/liboqs/build/lib/liboqs.so"

if os.path.exists(lib_path):
    ctypes.CDLL(lib_path)
else:
    print(f"⚠️ KRİTİK HATA: {lib_path} bulunamadı! Derleme klasörünü kontrol et.")

import oqs

class PQCEngine:
    def __init__(self, algorithm="Kyber512"):
        self.algorithm = algorithm
    
    def generate_pqc_key(self):
        # Kuantum bilgisayarlara dirençli anahtar kapsülleme (KEM)
        with oqs.KeyEncapsulation(self.algorithm) as kem:
            kem.generate_keypair()
            # 256-bit hibrit anahtar için secret key'i alıyoruz
            return kem.export_secret_key()[:32]