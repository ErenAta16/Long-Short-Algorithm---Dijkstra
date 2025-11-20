#  Yangın Acil Durum Sistemi - Gelişmiş Rota Bulma

##  Proje Açıklaması

Bu proje, yangın acil durumlarında en yakın itfaiye istasyonunu bulmak ve **matematiksel olarak garantili** en optimal rotayı hesaplamak için geliştirilmiş akıllı bir sistemdir. 

### Özellikler (v2.0)

**3 Gelişmiş Algoritma:** Dijkstra, A*, Bidirectional Search
**Gerçek Veriler:** OpenStreetMap entegrasyonu
**İzmir & Manisa:** 53 itfaiye istasyonu ile çalışır
**Graph Teorisi** 

## Özellikler

- **Otomatik İtfaiye Bulma**: İzmir ve Manisa genelinde doğrulanmış 53 istasyon ile en yakın noktanın tespiti
- **Akıllı Rota Optimizasyonu**: Tali yolları önceliklendiren rota hesaplama
- **Kırsal Yangın Tespiti**: Arazi türüne göre özel rota önerileri
- **Gerçek Zamanlı Harita**: İnteraktif harita ile görselleştirme
- **OSRM Entegrasyonu**: Gerçek yol verileri ile rota çizimi
- **TomTom API**: Güncel harita ve trafik verileri
- **Overpass/OSM Tabanlı Koordinatlar**: Açık veri ile doğrulanmış istasyon konumları


- **Python 3.9+**
- **TomTom API** - Harita ve rota verileri
- **OSRM** - Açık kaynak rota hesaplama
- **Folium** - İnteraktif harita oluşturma
- **aiohttp** - Asenkron HTTP istekleri
- **OpenStreetMap / Overpass API** - İtfaiye koordinatları
- **Google Maps** - Opsiyonel manuel doğrulama

## Kurulum

### Gereksinimler

```bash
pip install -r requirements.txt
```

### API Anahtarları

1. `config_local.py.example` dosyasını `config_local.py` olarak kopyalayın:
```bash
cp config_local.py.example config_local.py
```

2. `config_local.py` dosyasında gerçek API anahtarlarınızı girin:
```python
TOMTOM_API_KEY = "your_real_tomtom_api_key"
OPENWEATHER_API_KEY = "your_real_openweather_api_key"  # Opsiyonel
```

**Önemli**: `config_local.py` dosyası `.gitignore`'da olduğu için Git'e commit edilmez.

## Kullanım

### Ana Sistem

```bash
python fire_emergency_system.py
```

### Benchmark ve Test

```bash
# Kapsamlı sistem testi
python comprehensive_benchmark.py
```
## Proje Yapısı

```
🎯 YENİ ALGORİTMA MODÜLLERİ
├── advanced_pathfinding.py      #  Dijkstra, A*, Bidirectional algoritmaları
├── network_builder.py            #  Graph network oluşturucu
  ├── comprehensive_benchmark.py   #  Doğruluk testleri
└── ALGORITHM_DOCUMENTATION.md    # Teknik döküman

📱 ESKI SİSTEM (Hala çalışır)
├── fire_emergency_system.py      # Ana sistem
├── fire_stations.py              # İtfaiye koordinatları (İzmir & Manisa)
├── fire_station_finder.py        # İtfaiye bulma sistemi
├── route_calculator.py           # Rota hesaplama
├── smart_route_optimizer.py      # Akıllı optimizasyon
├── map_utils.py                  # Harita yardımcıları
├── config.py                     # Konfigürasyon
├── google_maps_coordinate_finder.py  # Koordinat bulucu
├── tomtom_fire_station_api.py    # TomTom API
├── tomtom_api.py                 # TomTom yardımcıları
└── requirements.txt              # Bağımlılıklar
```

### Temel Kullanım

```python
from network_builder import build_izmir_manisa_network
from advanced_pathfinding import DijkstraPathfinder, AStarPathfinder

# 1. Network oluştur
network = build_izmir_manisa_network()

# 2. Algoritma seç ve çalıştır
pathfinder = DijkstraPathfinder(network)  # veya AStarPathfinder
result = pathfinder.find_shortest_path(start_id, end_id)

# 3. Sonuçları göster
print(f"Mesafe: {result['distance']:.2f} km")
print(f"Süre: {result['estimated_time']:.1f} dakika")
```

### Benchmark Testleri

```bash
python comprehensive_benchmark.py
```

**Sonuçlar:**
- Koordinat Doğrulama: %100 (53/53 istasyon geçerli)
- Algoritma Doğruluk: %100 (30/30 test başarılı)
- Sistem Sağlığı: %100 (Tüm modüller çalışıyor)
-  A* algoritması %57 daha az node inceliyor
-  Detaylı rapor: `comprehensive_benchmark_report.json`

Daha fazla bilgi için: `ALGORITHM_DOCUMENTATION.md`

## Sistem Özellikleri

### Rota Optimizasyonu
- **Ana Yollar**: Hızlı ulaşım için
- **Tali Yollar**: Kırsal yangınlar için
- **Köy Yolları**: Uzak bölgeler için
- **Yaya Yolları**: Araçsız erişim için

### Akıllı Özellikler
- Gerçek zamanlı hava durumu entegrasyonu
- Trafik durumu analizi
- Arazi türü tespiti
- Dinamik rota ağırlıklandırması

## Veri Kaynakları

- **OpenStreetMap (Overpass API)**: İtfaiye koordinatlarının doğrulanması
- **Google Maps**: Opsiyonel koordinat karşılaştırmaları
- **TomTom API**: Harita ve rota verileri
- **OSRM**: Açık kaynak rota hesaplama
- **OpenWeatherMap**: Hava durumu verileri

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

