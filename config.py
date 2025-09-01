# TomTom API Ayarları
# API anahtarlarını config_local.py dosyasından yükle
try:
    from config_local import *
except ImportError:
    # Varsayılan değerler (güvenlik için boş)
    TOMTOM_API_KEY = "your_tomtom_api_key_here"
    OPENWEATHER_API_KEY = "your_openweather_api_key_here"
    TOMTOM_TRAFFIC_API_KEY = "your_tomtom_traffic_api_key_here"

TOMTOM_BASE_URL = "https://api.tomtom.com"

# Yol Ağırlıkları
ROAD_WEIGHTS = {
    'motorway': 1.0,      # Otoyol - En hızlı
    'trunk': 1.2,         # Ana yol
    'primary': 1.5,       # Birincil yol
    'secondary': 2.0,     # İkincil yol
    'tertiary': 2.5,      # Üçüncül yol
    'residential': 3.0,   # Yerleşim yolu - En yavaş
    'unclassified': 2.8   # Sınıflandırılmamış
}

# Varsayılan yol ağırlığı
DEFAULT_ROAD_WEIGHT = 2.0

# API Rate Limiting
MAX_REQUESTS_PER_MINUTE = 60
REQUEST_DELAY = 1.0  # saniye

# Akıllı Rota Optimizasyonu Ayarları
WEATHER_CACHE_DURATION = 300  # 5 dakika
TRAFFIC_CACHE_DURATION = 120  # 2 dakika
ROAD_CONDITION_CACHE_DURATION = 600  # 10 dakika

# Dinamik Ağırlık Çarpanları
WEATHER_MULTIPLIERS = {
    'clear': 1.0,
    'rain': 1.3,
    'snow': 2.0,
    'fog': 1.5,
    'storm': 2.5
}

TRAFFIC_MULTIPLIERS = {
    'free_flow': 1.0,
    'light': 1.1,
    'moderate': 1.3,
    'heavy': 1.6,
    'congested': 2.0
}

ROAD_CONDITION_MULTIPLIERS = {
    'normal': 1.0,
    'construction': 1.3,
    'accident': 1.8,
    'closed': 5.0,
    'poor_condition': 1.5
}
