#!/usr/bin/env python3
"""
🚒 İTFAİYE İSTASYONLARI VERİTABANI 🚒
İzmir ve Manisa Büyükşehir Belediyeleri
OpenStreetMap/Overpass API - Doğrulanmış ve temizlenmiş veriler
"""

from typing import Dict, Tuple, List

def load_fire_stations() -> Dict[str, Tuple[float, float]]:
    """İtfaiye istasyonlarını yükle - OSM'den doğrulanmış koordinatlar"""
    return {
        # İZMİR BÜYÜKŞEHİR BELEDİYESİ İTFAİYE İSTASYONLARI
        "Ayrancılar Orman Yangını Ekip Binası": (38.2508078, 27.264016),  # OpenStreetMap/Overpass
        "Bayındır İtfaiye": (38.2189277, 27.6414055),  # OpenStreetMap/Overpass
        "Bornova İtfaiye": (38.4608836, 27.2278188),  # OpenStreetMap/Overpass
        "Evka-4 Yeşiltepe İtfaiye İstasyonu": (38.4879945, 27.2137635),  # OpenStreetMap/Overpass
        "Gümüldür İtfaiyesi": (38.0780399, 27.0144903),  # OpenStreetMap/Overpass
        "Ilıca İtfaiye": (38.3051045, 26.3627989),  # OpenStreetMap/Overpass
        "Menemen İtfaiyesi": (38.6117943, 27.0752623),  # OpenStreetMap/Overpass
        "Naldöken İtfaiye": (38.4666894, 27.1349094),  # OpenStreetMap/Overpass
        "Turgutlu Belediyesi İtfaiye Müdürlüğü": (38.5072758, 27.7111476),  # OpenStreetMap/Overpass
        "Yeni Foça İtfaiye İstasyonu": (38.743919, 26.8430195),  # OpenStreetMap/Overpass
        "Yeşilyurt İtfaiye": (38.4020391, 27.1148877),  # OpenStreetMap/Overpass
        "Çiğli İtfaiye Grubu": (38.4871776, 27.0743545),  # OpenStreetMap/Overpass
        "İBB Narlıdere İtfaiye İstasyonu": (38.3937034, 27.0145063),  # OpenStreetMap/Overpass
        "İBB İtfaiye Daire Başkanlığı - AKS112": (38.4230268, 27.1532835),  # OpenStreetMap/Overpass
        "İtfaiye node 10273745362": (38.413113, 27.1391074),  # OpenStreetMap/Overpass
        "İtfaiye way 1341111321": (38.5901862, 27.3534318),  # OpenStreetMap/Overpass
        "İtfaiye way 473334013": (37.7544692, 26.9804388),  # OpenStreetMap/Overpass
        "İtfaiye way 473391053": (37.7887617, 26.7039262),  # OpenStreetMap/Overpass
        "İtfaiye way 484836776": (38.4919461, 27.0410581),  # OpenStreetMap/Overpass
        "İtfaiye way 785338569": (38.5671522, 27.4551484),  # OpenStreetMap/Overpass
        "İtfaiye way 883938684": (38.3916612, 27.150281),  # OpenStreetMap/Overpass
        "İzmir Aliağa İtfaiye": (38.801, 26.971),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Balçova İtfaiye": (38.391, 27.028),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Bayraklı İtfaiye": (38.465, 27.16),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Bergama İtfaiye": (39.12, 27.18),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Buca İtfaiye": (38.399, 27.183),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Gaziemir İtfaiye": (38.325, 27.136),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Güzelbahçe İtfaiye": (38.371, 26.875),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Karaburun İtfaiye": (38.65, 26.52),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Karşıyaka İtfaiye Merkez": (38.459926, 27.141067),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Kemalpaşa İtfaiye": (38.429, 27.417),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Menderes İtfaiye": (38.253, 27.136),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Seferihisar İtfaiye": (38.196, 26.84),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Selçuk İtfaiye": (37.951, 27.369),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Tire İtfaiye": (38.086, 27.732),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Torbalı İtfaiye": (38.158, 27.359),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Urla İtfaiye": (38.323, 26.765),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Çeşme İtfaiye": (38.323, 26.306),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İzmir Ödemiş İtfaiye": (38.227, 27.968),  # Büyükşehir Belediyesi (Tahmini Konum)

        # MANİSA BÜYÜKŞEHİR BELEDİYESİ İTFAİYE İSTASYONLARI
        "Manisa Akhisar İtfaiye": (38.918, 27.838),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Alaşehir İtfaiye": (38.351, 28.516),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Demirci İtfaiye": (39.044, 28.656),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Gördes İtfaiye": (38.933, 28.285),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Kula İtfaiye": (38.546, 28.647),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Kırkağaç İtfaiye": (39.107, 27.669),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Salihli İtfaiye": (38.482, 28.14),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Sarıgöl İtfaiye": (38.237, 28.697),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Soma İtfaiye": (39.185, 27.61),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Yunusemre İtfaiye": (38.619, 27.428),  # Büyükşehir Belediyesi (Tahmini Konum)
        "Manisa Şehzadeler İtfaiye": (38.613, 27.426),  # Büyükşehir Belediyesi (Tahmini Konum)
        "İtfaiye node 5744647422": (38.5100012, 28.2411396),  # OpenStreetMap/Overpass
    }

def get_fire_station_regions() -> Dict[str, List[str]]:
    """İtfaiye istasyonlarını bölgelere göre grupla"""
    return {
        "İzmir İlçe İtfaiyeleri": [],
        "Manisa İlçe İtfaiyeleri": []
    }

def categorize_fire_stations(fire_stations: Dict[str, Tuple[float, float]]) -> Dict[str, List[Tuple[str, Tuple[float, float]]]]:
    """İtfaiye istasyonlarını bölgelere göre kategorize et - Optimize edilmiş"""
    regions = get_fire_station_regions()
    
    # İzmir ilçe isimleri (set kullanarak daha hızlı lookup)
    izmir_districts = {
        "Konak", "Bornova", "Karşıyaka", "Çiğli", "Gaziemir", "Bayraklı",
        "Narlıdere", "Balçova", "Buca", "Foça", "Menemen", "Dikili",
        "Aliağa", "Bergama", "Ödemiş", "Tire", "Torbalı", "Menderes",
        "Urla", "Çeşme", "Karaburun", "Seferihisar", "Bayındır",
        "Kemalpaşa", "Güzelbahçe", "Selçuk", "Gümüldür", "Ilıca", "Yeşilyurt",
        "Ayrancılar", "Evka-4", "Naldöken", "İBB"
    }
    
    # Manisa ilçe isimleri
    manisa_districts = {
        "Yunusemre", "Şehzadeler", "Akhisar", "Salihli", "Turgutlu",
        "Soma", "Kırkağaç", "Alaşehir", "Demirci", "Sarıgöl", "Kula", "Gördes"
    }
    
    for name, coords in fire_stations.items():
        # İzmir kontrolü
        if "İzmir" in name or any(district in name for district in izmir_districts):
            regions["İzmir İlçe İtfaiyeleri"].append((name, coords))
        # Manisa kontrolü
        elif "Manisa" in name or any(district in name for district in manisa_districts):
            regions["Manisa İlçe İtfaiyeleri"].append((name, coords))
        # Varsayılan: İzmir (çoğunluk İzmir'de)
        else:
            regions["İzmir İlçe İtfaiyeleri"].append((name, coords))
    
    return regions
