from qunetsim.components import Host
from qunetsim.objects import Qubit

def simulate_qkd():
    # Fiziksel foton dağıtımı simülasyonu
    # Basit bir 256-bit kuantum anahtarı simüle edelim
    import os
    return os.urandom(32) # Gerçekte QuNetSim BB84 protokolü çalıştırır