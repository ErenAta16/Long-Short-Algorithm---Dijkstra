# Yangın Acil Durum Sistemi

## Proje Açıklaması

Bu proje, yangın acil durumlarında en yakın itfaiye istasyonunu bulmak ve en optimal rotayı hesaplamak için geliştirilmiş akıllı bir sistemdir. Sistem, TomTom harita verilerini kullanarak gerçek zamanlı rota optimizasyonu yapar ve tali yolları önceliklendirir.

## Özellikler

- **Otomatik İtfaiye Bulma**: 69 itfaiye istasyonu ile otomatik en yakın itfaiye tespiti
- **Akıllı Rota Optimizasyonu**: Tali yolları önceliklendiren rota hesaplama
- **Kırsal Yangın Tespiti**: Arazi türüne göre özel rota önerileri
- **Gerçek Zamanlı Harita**: İnteraktif harita ile görselleştirme
- **OSRM Entegrasyonu**: Gerçek yol verileri ile rota çizimi
- **TomTom API**: Güncel harita ve trafik verileri

## Teknolojiler

- **Python 3.9+**
- **TomTom API** - Harita ve rota verileri
- **OSRM** - Açık kaynak rota hesaplama
- **Folium** - İnteraktif harita oluşturma
- **aiohttp** - Asenkron HTTP istekleri
- **Google Maps** - Koordinat doğrulama

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

### Koordinat Güncelleme

```bash
python google_maps_coordinate_finder.py
```

## Proje Yapısı

```
├── fire_emergency_system.py      # Ana sistem
├── fire_stations.py              # İtfaiye koordinatları
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

## 🗺️ Desteklenen Bölgeler

- **Bursa**: 14 itfaiye istasyonu
- **Balıkesir**: 19 itfaiye istasyonu
- **Çanakkale**: 12 itfaiye istasyonu
- **Tekirdağ**: 11 itfaiye istasyonu
- **Kırklareli**: 7 itfaiye istasyonu
- **Yalova**: 6 itfaiye istasyonu

**Toplam: 69 itfaiye istasyonu**

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

- **Google Maps**: Koordinat doğrulama
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

## Geliştiriciler

- **Proje Yöneticisi**: Erena
- **Geliştirici**: AI Assistant

## İletişim

Proje hakkında sorularınız için issue açabilirsiniz.

## Teşekkürler

- TomTom API ekibine
- OSRM geliştiricilerine
- Google Maps ekibine
- Açık kaynak topluluğuna

---

**⚠️ Önemli Not**: Bu sistem acil durumlar için geliştirilmiştir. Gerçek acil durumlarda mutlaka resmi acil servisleri (112) arayın.
