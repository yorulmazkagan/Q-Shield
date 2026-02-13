

# 🛡️ Q-Shield: Hybrid Quantum-Safe 6G Network Slicing

**Uyarı**
Bu proje, "Turkcell Yarının Teknoloji Liderleri Proje Yarışması" kapsamında geliştirilmiştir. Projenin tüm fikri ve sınai mülkiyet hakları, ilgili taahhütname hükümleri saklı kalmak kaydıyla geliştiriciye aittir. Yazılı izin alınmaksızın kopyalanması, dağıtılması veya ticari amaçla kullanılması yasaktır.

**Q-Shield**, 6G ağ ekosisteminde "Kuantum Kıyameti" (Quantum Apocalypse) olarak adlandırılan gelecekteki siber tehditlere karşı geliştirilmiş, **Hibrit Kuantum Güvenlik (PQC + QKD)** ve **AI Tabanlı Otonom Orkestrasyon** katmanlarını birleştiren vizyoner bir prototiptir.

---

## 📌 Proje Özeti ve Vizyon

Mevcut şifreleme standartları (RSA, ECC), gelişen kuantum bilgisayar işlem gücü (Shor Algoritması) karşısında savunmasız kalma riski altındadır. **Q-Shield**, Turkcell 6G vizyonuyla uyumlu olarak, ağ kaynaklarını (Slicing) dinamik ve akıllı bir şekilde koruma altına almayı hedefler.

Bu proje, akademik derinliği olan bir **"Proof-of-Concept" (Kavram Kanıtı)** simülasyonudur. Amacımız, donanım bağımlı kuantum teknolojilerini (QKD) yazılımsal esneklikle (PQC) birleştirip yapay zeka ile yönetmektir.

---

## 🚀 Temel Teknolojiler ve Hibrit Mimari

Q-Shield, güvenliği iki farklı evrenin kesişim noktasında sağlar:

1.  **Post-Quantum Cryptography (PQC):** NIST tarafından standardize edilen **ML-KEM (Kyber-512)** algoritması kullanılarak, kuantum bilgisayarların bile çözemediği karmaşık "kafes tabanlı" (lattice-based) matematiksel bariyerler kurulur.
2.  **Quantum Key Distribution (QKD):** Kuantum fiziği yasalarına (Heisenberg Belirsizlik İlkesi) dayanan **BB84 Protokolü** simüle edilerek, fiziksel katmanda dinlenmesi imkansız anahtar dağıtımı gerçekleştirilir.
3.  **Hybrid Fusion:** Üretilen anahtarlar, aşağıdaki formül ile birleştirilerek nihai şifreleme anahtarına (K-Final) dönüştürülür:
    $$K_{Final} = \text{SHA-256}(K_{QKD} \parallel K_{PQC})$$



---

## 🧠 AI-Powered Dynamic Orchestration

Proje, sadece statik bir koruma değil, **Yapay Zeka Destekli Otonom Savunma** katmanı sunar:
* **Anomali Tespiti:** Sistem, ağ trafiğini canlı olarak izleyerek **Z-Score (İstatistiksel Sapma)** analizi yapar.
* **Otonom Dilimleme:** Tehdit algılandığında, trafik standart kanaldan (Standard-5G) anında **Quantum-Safe Slice** katmanına (6G) otomatik olarak aktarılır.

---

## ⚠️ Teknik Notlar (Simülasyon Detayları)

Bu bir endüstriyel ürün değil, ileri düzey bir mühendislik simülasyonudur. Projenin prototip aşamasında olması nedeniyle aşağıdaki noktaların bilinmesi önemlidir:

* **QKD Simülasyonu:** Gerçek QKD, yüz binlerce dolarlık donanım gerektirir. Bu projede fiziksel katman, **QuNetSim** prensiplerine sadık kalınarak `os.urandom` ve baz eşleme simülasyonlarıyla modellenmiştir.
* **Yol Bağımlılığı (Hardcoded Paths):** `src/pqc_engine.py` dosyasındaki `lib_path` değişkeni, geliştirme ortamına özel olarak ayarlanmıştır. Production ortamında bu yolların ortam değişkenleri (ENV) ile güncellenmesi gerekmektedir.
* **Performans:** Sistem Python/FastAPI tabanlıdır. Gerçek 6G ağlarında (<100 $\mu$s gecikme) bu yapının C++ tabanlı düşük seviyeli kernel modülleriyle entegre edilmesi planlanmaktadır.
* **Algoritma Seçimi:** En karmaşık AI modelleri yerine, gerçek zamanlı ağ analizi için daha hızlı ve verimli olan **İstatistiksel Anomali Tespiti** tercih edilmiştir.

---

## 🤝 AI Collaborative Development Note

Bu projenin geliştirilme sürecinde, mimari tasarım, kod optimizasyonu ve teknik dokümantasyon aşamalarında **ileri seviye yapay zeka modelleriyle iş birliği yapılmıştır.** Bu iş birliği, projenin 6G vizyonuna uygun fütüristik bir yapıya kavuşmasını ve kod kalitesinin küresel standartlara yükseltilmesini sağlamıştır.

---

## 🛠️ Kurulum ve Çalıştırma

> **Not:** `liboqs` kütüphanesinin sisteminizde derlenmiş olması gerekmektedir.

1.  Repoyu klonlayın.
2.  `src/pqc_engine.py` içindeki `lib_path` yolunu kendi `.so` dosyanızın konumuyla güncelleyin.
3.  Gerekli kütüphaneleri kurun: `pip install fastapi uvicorn numpy`.
4.  Sunucuyu başlatın:
    ```bash
    PYTHONPATH=. uvicorn src.slice_api:app --reload
    ```

---

## 🗺️ Gelecek Yol Haritası (Roadmap)

* [ ] **Donanım Entegrasyonu:** Gerçek bir QKD cihazı veya QKD-as-a-Service (KaaS) API entegrasyonu.
* [ ] **Edge AI:** Anomali tespitinin baz istasyonu seviyesinde (Edge Computing) çalıştırılması.
* [ ] **TeraFlowSDN:** Yazılım Tanımlı Ağ kontrolcüleriyle tam otomasyon.

---

**Geliştirici:** Kağan Yorulmaz  
*Computer Engineering Student @ Konya Technical University*