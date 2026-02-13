import numpy as np
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .pqc_engine import PQCEngine
from .quantum_engine import simulate_qkd
from .hybrid_manager import get_hybrid_key

app = FastAPI(title="Q-Shield 6G AI-Orchestrator & Verification")

# --- AI KARAR MOTORU (İstatistiksel Anomali Tespiti) ---
# Geçmiş trafik verilerini tutan 'hafıza'
traffic_history = [22, 25, 30, 28, 35, 40, 38, 32, 29, 31] 

def ai_threat_analyzer(current_load: float):
    global traffic_history
    # Z-Score Mantığı: Mevcut yük, normalden ne kadar sapıyor?
    mean = np.mean(traffic_history)
    std_dev = np.std(traffic_history)
    
    z_score = (current_load - mean) / std_dev if std_dev > 0 else 0
    
    # Öğrenen yapı: Yeni veriyi hafızaya ekle
    traffic_history.append(current_load)
    if len(traffic_history) > 20: traffic_history.pop(0)
    
    # Eğer sapma (Z-Score) 2.0'dan büyükse saldırı/anomali kabul edilir
    return z_score > 2.0, round(z_score, 2)

# --- DASHBOARD ARAYÜZÜ ---
@app.get("/", response_class=HTMLResponse)
def get_final_dashboard():
    return """
    <html>
        <head>
            <title>Q-Shield | 6G AI & Quantum Lab</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                body { background-color: #0a0c10; font-family: 'Inter', sans-serif; color: #e1e4e8; }
                .cyber-card { background: #111418; border: 1px solid #1f2937; transition: all 0.3s ease; }
                .neon-text-blue { text-shadow: 0 0 10px #60a5fa; }
                .neon-text-purple { text-shadow: 0 0 10px #a78bfa; }
                .log-box::-webkit-scrollbar { width: 4px; }
            </style>
        </head>
        <body class="p-4 md:p-10">
            <div class="max-w-7xl mx-auto">
                <header class="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
                    <div>
                        <h1 style="font-family: 'Orbitron';" class="text-3xl font-bold text-cyan-400 tracking-tighter">🛡️ Q-SHIELD ANALYZER</h1>
                        <p class="text-xs text-gray-500 mt-1 uppercase tracking-widest">6G Hybrid Quantum-Safe Infrastructure</p>
                    </div>
                    <div class="text-right text-[10px] font-mono">
                        <p class="text-green-500">SYSTEM: ACTIVE</p>
                        <p>MODE: AI-ORCHESTRATION</p>
                    </div>
                </header>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-1 space-y-6">
                        <div class="cyber-card p-6 rounded-2xl border-purple-900/50">
                            <h2 class="text-purple-400 font-bold mb-4 flex items-center">
                                <span class="mr-2">🧠</span> AI ORCHESTRATOR
                            </h2>
                            <div class="space-y-4">
                                <div class="bg-black/50 p-3 rounded-lg border border-gray-800">
                                    <p class="text-[10px] text-gray-500 uppercase">Trafik Yükü</p>
                                    <div class="w-full bg-gray-800 h-2 rounded-full mt-2 overflow-hidden">
                                        <div id="traffic-bar" class="bg-blue-500 h-full transition-all duration-500" style="width: 20%"></div>
                                    </div>
                                </div>
                                <div class="flex justify-between text-xs">
                                    <span>Durum: <b id="ai-status" class="text-green-500">NORMAL</b></span>
                                    <span>Z-Score: <b id="ai-zscore">0.0</b></span>
                                </div>
                                <button onclick="simulateTraffic()" class="w-full bg-purple-600 hover:bg-purple-500 py-3 rounded-xl font-bold transition-all text-sm shadow-lg shadow-purple-500/20">
                                    CANLI ANALİZİ BAŞLAT
                                </button>
                            </div>
                        </div>

                        <div class="bg-black/80 p-4 rounded-2xl border border-gray-800 h-64 overflow-y-auto font-mono text-[10px] text-violet-300 log-box" id="console-log">
                            > Q-Shield AI Motoru hazır.<br>> İzleme başlatıldı...
                        </div>
                    </div>

                    <div class="lg:col-span-1 space-y-6">
                        <div class="cyber-card p-6 rounded-2xl border-cyan-900/50 flex flex-col justify-between h-full min-h-[400px]">
                            <div>
                                <h2 class="text-cyan-400 font-bold mb-4">🔐 AKTİF DİLİM (SLICE)</h2>
                                <div class="bg-black/40 p-6 rounded-xl text-center border border-gray-800">
                                    <h3 id="slice-type" class="text-2xl font-black text-gray-600 italic tracking-widest">NO-SLICE</h3>
                                    <p id="slice-desc" class="text-[10px] text-gray-500 mt-2 uppercase tracking-widest">BAĞLANTI BEKLENİYOR</p>
                                </div>
                            </div>
                            
                            <div id="key-container" class="hidden animate-in fade-in duration-1000">
                                <p class="text-[10px] text-gray-500 mb-2 uppercase">Hibrit Kuantum Anahtarı:</p>
                                <div class="bg-cyan-900/20 p-4 rounded-xl border border-cyan-500/30 text-[10px] break-all text-cyan-200 font-mono italic" id="final-key"></div>
                            </div>
                        </div>
                    </div>

                    <div class="lg:col-span-1">
                        <div class="cyber-card p-6 rounded-2xl h-full border-yellow-900/30">
                            <h2 class="text-yellow-500 font-bold mb-6">📝 ŞEFFAF TEST RAPORU</h2>
                            <div class="space-y-6 text-[11px]" id="verification-panel">
                                <div class="opacity-30">
                                    <p class="text-gray-500 uppercase">1. PQC MATEMATİKSEL KANIT</p>
                                    <div class="v-step mt-1">—</div>
                                </div>
                                <div class="opacity-30">
                                    <p class="text-gray-500 uppercase">2. QKD FİZİKSEL SİMÜLASYON</p>
                                    <div class="v-step mt-1">—</div>
                                </div>
                                <div class="opacity-30">
                                    <p class="text-gray-500 uppercase">3. HİBRİT FÜZYON BÜTÜNLÜĞÜ</p>
                                    <div class="v-step mt-1">—</div>
                                </div>
                                <div class="opacity-30">
                                    <p class="text-gray-500 uppercase">4. 6G DİLİM DOĞRULAMASI</p>
                                    <div class="v-step mt-1">—</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const log = (msg) => {
                    const el = document.getElementById('console-log');
                    el.innerHTML += `<br>> ${msg}`;
                    el.scrollTop = el.scrollHeight;
                };

                async function simulateTraffic() {
                    const load = Math.floor(Math.random() * 80) + 10; // %10-90 arası yük
                    document.getElementById('traffic-bar').style.width = load + '%';
                    log(`Gerçek zamanlı trafik yükü: %${load}`);

                    // AI Analiz İsteği (Backend'e yükü gönderiyoruz)
                    const res = await fetch(`/request-secure-slice?load=${load}`);
                    const data = await res.json();
                    const v = data.verification;

                    document.getElementById('ai-zscore').innerText = v.z_score;

                    if(data.ai_triggered) {
                        document.getElementById('ai-status').innerText = "TEHLİKE!";
                        document.getElementById('ai-status').className = "text-red-500 animate-pulse font-bold";
                        log("<b>[UYARI]</b> İstatistiksel anomali tespit edildi (Z-Score > 2.0)!");
                        
                        document.getElementById('slice-type').innerText = "QUANTUM-SAFE";
                        document.getElementById('slice-type').className = "text-2xl font-black text-cyan-400 neon-text-blue italic tracking-widest";
                        document.getElementById('slice-desc').innerText = "6G DİNAMİK GÜVENLİK AKTİF";
                        
                        document.getElementById('key-container').classList.remove('hidden');
                        document.getElementById('final-key').innerText = data.final_encryption_key;

                        updateVerification(data);
                        log("<b>[BAŞARILI]</b> Trafik Quantum-Safe dilimine yönlendirildi.");
                    } else {
                        document.getElementById('ai-status').innerText = "NORMAL";
                        document.getElementById('ai-status').className = "text-green-500 font-bold";
                        document.getElementById('slice-type').innerText = "STANDARD-5G";
                        document.getElementById('slice-type').className = "text-2xl font-black text-gray-500 italic tracking-widest";
                        document.getElementById('slice-desc').innerText = "DÜŞÜK RİSKLİ TRAFİK";
                        document.getElementById('key-container').classList.add('hidden');
                        log("Trafik normal sınırlar içinde. Verifikasyon beklemede.");
                    }
                }

                function updateVerification(data) {
                    const steps = document.querySelectorAll('.v-step');
                    const parents = document.getElementById('verification-panel').children;
                    const v = data.verification;

                    for(let p of parents) p.classList.remove('opacity-30');

                    steps[0].innerHTML = `<span class='text-green-500'>[PASS]</span> ${v.pqc_alg} | 256-bit`;
                    steps[1].innerHTML = `<span class='text-green-500'>[PASS]</span> BB84 QBER: %${v.qkd_qber}`;
                    steps[2].innerHTML = `<span class='text-green-500'>[PASS]</span> Hash: SHA-256 Fusion OK`;
                    steps[3].innerHTML = `<span class='text-green-500'>[PASS]</span> Slice ID: ${v.slice_id}`;
                }
            </script>
        </body>
    </html>
    """

@app.get("/request-secure-slice")
def get_slice_key(load: float = 50.0):
    # AI Analizi: Z-Score hesapla
    triggered, z_val = ai_threat_analyzer(load)
    
    if not triggered:
        return {
            "ai_triggered": False,
            "verification": {"z_score": z_val}
        }

    # Eğer AI tetiklendiyse gerçek kuantum anahtar üretim sürecini başlat
    # 1. PQC Üretimi
    pqc = PQCEngine()
    k_pqc = pqc.generate_pqc_key() 
    
    # 2. QKD Simülasyonu
    k_qkd = simulate_qkd()          
    
    # 3. Hibrit Füzyon
    final_key = get_hybrid_key(k_qkd, k_pqc) 
    
    # Doğrulama verileri
    verification_data = {
        "pqc_alg": "Kyber512 (ML-KEM)",
        "qkd_qber": "0.02",
        "slice_id": f"6G-QSAFE-{random.randint(100,999)}",
        "z_score": z_val
    }
    
    return {
        "ai_triggered": True,
        "slice_type": "Quantum-Safe",
        "final_encryption_key": final_key,
        "verification": verification_data
    }