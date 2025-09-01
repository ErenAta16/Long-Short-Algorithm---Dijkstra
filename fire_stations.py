#!/usr/bin/env python3
"""
🚒 İTFAİYE İSTASYONLARI VERİTABANI 🚒
Marmara Bölgesi itfaiye istasyonlarının güncel koordinatları
Google Maps'ten araştırılmıştır
"""

from typing import Dict, Tuple, List

def load_fire_stations() -> Dict[str, Tuple[float, float]]:
    """İtfaiye istasyonlarını yükle - Google Maps'ten otomatik çekilen güncel koordinatlarla"""
    return {
        # Bursa İlçe İtfaiyeleri - Google Maps'ten Güncel Koordinatlar
        "Bursa Merkez İtfaiye": (40.2000011, 29.060448),  # Google Maps'ten güncellenmiş
        "Nilüfer İtfaiye": (40.2140, 29.0280),  # Nilüfer Belediyesi İtfaiye Müdürlüğü
        "Osmangazi İtfaiye": (40.2000011, 29.060448),  # Geliştirilmiş arama ile bulundu
        "Yıldırım İtfaiye": (40.1928, 29.0650),  # Yıldırım Belediyesi İtfaiye Müdürlüğü
        "Mudanya İtfaiye": (40.3569683, 28.9115467),  # Geliştirilmiş arama ile bulundu
        "Gemlik İtfaiye": (40.4285782, 29.1697788),  # Google Maps'ten güncellenmiş
        "Karacabey İtfaiye": (40.232487, 28.373786),  # Google Maps'ten güncellenmiş (manuel)
        "İnegöl İtfaiye": (40.089967, 29.4926198),  # Google Maps'ten güncellenmiş
        "Orhangazi İtfaiye": (40.4828481, 29.3074737),  # Google Maps'ten güncellenmiş
        "Kestel İtfaiye": (40.199598, 29.214219),  # Geliştirilmiş arama ile bulundu
        "Gürsu İtfaiye": (40.2052104, 29.1894129),  # Google Maps'ten güncellenmiş
        "Harmancık İtfaiye": (39.6781189, 29.145735),  # Google Maps'ten güncellenmiş
        "Büyükorhan İtfaiye": (39.7691365, 28.8876668),  # Google Maps'ten güncellenmiş
        "Orhaneli İtfaiye": (39.903467, 28.98696),  # Google Maps'ten güncellenmiş
        
        # Balıkesir İlçe İtfaiyeleri - Google Maps'ten Güncel Koordinatlar
        "Balıkesir Merkez İtfaiye": (39.6484, 27.8826),  # Manuel koordinat (güvenilir)
        "Bandırma İtfaiye": (40.3409365, 27.9816527),  # Google Maps'ten güncellenmiş
        "Gönen İtfaiye": (40.102031, 27.662936),  # Google Maps'ten güncellenmiş
        "Erdek İtfaiye": (40.6530092, 29.2860677),  # Geliştirilmiş arama ile bulundu
        "Ayvalık İtfaiye": (39.3396125, 26.7078382),  # Geliştirilmiş arama ile bulundu
        "Edremit İtfaiye": (39.59901, 27.022079),  # Google Maps'ten güncellenmiş
        "Burhaniye İtfaiye": (39.4982286, 26.9701084),  # Google Maps'ten güncellenmiş
        "Havran İtfaiye": (39.557499, 27.102608),  # Google Maps'ten güncellenmiş
        "Dursunbey İtfaiye": (39.5959413, 28.6256328),  # Google Maps'ten güncellenmiş
        "Sındırgı İtfaiye": (39.239905, 28.178351),  # Google Maps'ten güncellenmiş
        "Bigadiç İtfaiye": (39.3956, 28.1311),  # Manuel koordinat (güvenilir)
        "Susurluk İtfaiye": (39.916821, 28.161473),  # Google Maps'ten güncellenmiş
        "Kepsut İtfaiye": (39.6865872, 28.155947),  # Google Maps'ten güncellenmiş
        "Manyas İtfaiye": (40.0473469, 27.9733073),  # Google Maps'ten güncellenmiş
        "Savaştepe İtfaiye": (39.3820146, 27.6522851),  # Google Maps'ten güncellenmiş
        "İvrindi İtfaiye": (39.5813223, 27.4920758),  # Geliştirilmiş arama ile bulundu
        "Balya İtfaiye": (39.7507956, 27.5785269),  # Google Maps'ten güncellenmiş
        "Karesi İtfaiye": (39.6584, 27.8926),  # Manuel koordinat (güvenilir)
        
        # Çanakkale İlçe İtfaiyeleri - Google Maps'ten Güncel Koordinatlar
        "Çanakkale Merkez İtfaiye": (40.1553, 26.4142),  # Manuel koordinat (güvenilir)
        "Gelibolu İtfaiye": (40.410071, 26.664286),  # Google Maps'ten güncellenmiş
        "Lapseki İtfaiye": (40.3391351, 26.6856577),  # Google Maps'ten güncellenmiş
        "Eceabat İtfaiye": (40.1856, 26.3578),  # Manuel koordinat (güvenilir)
        "Bozcaada İtfaiye": (39.834791, 26.0719448),  # Google Maps'ten güncellenmiş
        "Gökçeada İtfaiye": (40.1486594, 26.4361629),  # Google Maps'ten güncellenmiş
        "Yenice İtfaiye": (40.089255, 29.423849),  # Geliştirilmiş arama ile bulundu
        "Bayramiç İtfaiye": (39.8097, 26.6400),  # Manuel koordinat (güvenilir)
        "Çan İtfaiye": (40.02887, 27.0533041),  # Google Maps'ten güncellenmiş
        "Biga İtfaiye": (40.2399216, 27.2303106),  # Google Maps'ten güncellenmiş
        "Ayvacık İtfaiye": (39.6011, 26.4044),  # Manuel koordinat (güvenilir)
        "Ezine İtfaiye": (39.779374, 26.343783),  # Google Maps'ten güncellenmiş
        
        # Tekirdağ İlçe İtfaiyeleri - Google Maps'ten Güncel Koordinatlar
        "Tekirdağ Merkez İtfaiye": (40.972866, 27.493886),  # Google Maps'ten güncellenmiş
        "Çorlu İtfaiye": (40.1486594, 26.4361629),  # Geliştirilmiş arama ile bulundu
        "Çerkezköy İtfaiye": (41.2891903, 27.9833121),  # Google Maps'ten güncellenmiş
        "Süleymanpaşa İtfaiye": (40.9881, 27.5217),  # Manuel koordinat (güvenilir)
        "Malkara İtfaiye": (40.8841412, 26.8917293),  # Google Maps'ten güncellenmiş
        "Saray İtfaiye": (41.4356789, 27.9207106),  # Google Maps'ten güncellenmiş
        "Ergene İtfaiye": (41.2081156, 27.746867),  # Google Maps'ten güncellenmiş
        "Kapaklı İtfaiye": (41.3242921, 27.9789344),  # Geliştirilmiş arama ile bulundu
        "Şarköy İtfaiye": (40.6146896, 27.1119058),  # Google Maps'ten güncellenmiş
        "Hayrabolu İtfaiye": (41.2020831, 27.1013191),  # Google Maps'ten güncellenmiş
        "Muratlı İtfaiye": (41.178661, 27.5026283),  # Google Maps'ten güncellenmiş
        
        # Kırklareli İlçe İtfaiyeleri - Google Maps'ten Güncel Koordinatlar
        "Kırklareli Merkez İtfaiye": (41.7313784, 27.2262697),  # Google Maps'ten güncellenmiş
        "Lüleburgaz İtfaiye": (41.3966365, 27.3804081),  # Google Maps'ten güncellenmiş
        "Babaeski İtfaiye": (41.4434392, 27.0619871),  # Google Maps'ten güncellenmiş
        "Vize İtfaiye": (41.574143, 27.7620862),  # Google Maps'ten güncellenmiş
        "Pınarhisar İtfaiye": (41.6275014, 27.5154977),  # Google Maps'ten güncellenmiş
        "Demirköy İtfaiye": (41.8247695, 27.7690137),  # Google Maps'ten güncellenmiş
        "Kofçaz İtfaiye": (41.7300, 27.1500),  # Manuel koordinat (güvenilir)
        
        # Yalova İlçe İtfaiyeleri - Google Maps'ten Güncel Koordinatlar
        "Yalova Merkez İtfaiye": (40.6500, 29.2667),  # Manuel koordinat (güvenilir)
        "Çınarcık İtfaiye": (40.6464305, 29.1288721),  # Google Maps'ten güncellenmiş
        "Termal İtfaiye": (40.609357, 29.172875),  # Google Maps'ten güncellenmiş
        "Armutlu İtfaiye": (40.5142947, 28.8347951),  # Google Maps'ten güncellenmiş
        "Çiftlikköy İtfaiye": (40.661618, 29.328868),  # Google Maps'ten güncellenmiş
        "Altınova İtfaiye": (40.6983139, 29.5093341),  # Google Maps'ten güncellenmiş
        
        # Otomatik bulunan itfaiyeler (TomTom API'den)
        "Bursa Mudanya Station Social Facilities": (40.373305, 28.889496)
    }

def get_fire_station_regions() -> Dict[str, List[str]]:
    """İtfaiye istasyonlarını bölgelere göre grupla"""
    return {
        "Marmara Bölgesi Ana İtfaiyeler": [],
        "Bursa İlçe İtfaiyeleri": [],
        "Balıkesir İlçe İtfaiyeleri": [],
        "Çanakkale İlçe İtfaiyeleri": [],
        "Tekirdağ İlçe İtfaiyeleri": [],
        "Kırklareli İlçe İtfaiyeleri": [],
        "Yalova İlçe İtfaiyeleri": []
    }

def categorize_fire_stations(fire_stations: Dict[str, Tuple[float, float]]) -> Dict[str, List[Tuple[str, Tuple[float, float]]]]:
    """İtfaiye istasyonlarını bölgelere göre kategorize et"""
    regions = get_fire_station_regions()
    
    for name, coords in fire_stations.items():
        if "Büyükşehir" in name:
            regions["Marmara Bölgesi Ana İtfaiyeler"].append((name, coords))
        elif "Bursa" in name or name in ["Mudanya İtfaiye", "Gemlik İtfaiye", "Karacabey İtfaiye", "İnegöl İtfaiye", "Orhangazi İtfaiye", "Kestel İtfaiye", "Gürsu İtfaiye", "Keles İtfaiye", "Harmancık İtfaiye", "Büyükorhan İtfaiye", "Orhaneli İtfaiye"]:
            regions["Bursa İlçe İtfaiyeleri"].append((name, coords))
        elif "Balıkesir" in name or name in ["Bandırma İtfaiye", "Gönen İtfaiye", "Erdek İtfaiye", "Ayvalık İtfaiye", "Edremit İtfaiye", "Burhaniye İtfaiye", "Havran İtfaiye", "Dursunbey İtfaiye", "Sındırgı İtfaiye", "Bigadiç İtfaiye", "Susurluk İtfaiye", "Kepsut İtfaiye", "Manyas İtfaiye", "Savaştepe İtfaiye", "İvrindi İtfaiye", "Balya İtfaiye", "Karesi İtfaiye"]:
            regions["Balıkesir İlçe İtfaiyeleri"].append((name, coords))
        elif "Çanakkale" in name or name in ["Gelibolu İtfaiye", "Lapseki İtfaiye", "Eceabat İtfaiye", "Bozcaada İtfaiye", "Gökçeada İtfaiye", "Yenice İtfaiye", "Bayramiç İtfaiye", "Çan İtfaiye", "Biga İtfaiye", "Ayvacık İtfaiye", "Ezine İtfaiye"]:
            regions["Çanakkale İlçe İtfaiyeleri"].append((name, coords))
        elif "Tekirdağ" in name or name in ["Çorlu İtfaiye", "Çerkezköy İtfaiye", "Süleymanpaşa İtfaiye", "Malkara İtfaiye", "Saray İtfaiye", "Ergene İtfaiye", "Kapaklı İtfaiye", "Şarköy İtfaiye", "Hayrabolu İtfaiye", "Muratlı İtfaiye"]:
            regions["Tekirdağ İlçe İtfaiyeleri"].append((name, coords))
        elif "Kırklareli" in name or name in ["Lüleburgaz İtfaiye", "Babaeski İtfaiye", "Vize İtfaiye", "Pınarhisar İtfaiye", "Demirköy İtfaiye", "Kofçaz İtfaiye", "Pehlivanköy İtfaiye", "Sergen İtfaiye"]:
            regions["Kırklareli İlçe İtfaiyeleri"].append((name, coords))
        elif "Yalova" in name or name in ["Çınarcık İtfaiye", "Termal İtfaiye", "Armutlu İtfaiye", "Çiftlikköy İtfaiye", "Altınova İtfaiye"]:
            regions["Yalova İlçe İtfaiyeleri"].append((name, coords))
    
    return regions
