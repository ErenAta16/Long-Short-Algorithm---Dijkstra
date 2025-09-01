#!/usr/bin/env python3
"""
🗺️ GOOGLE MAPS KOORDİNAT BULUCU 🗺️
İtfaiye adreslerini Google Maps'te arayıp koordinatları bulur
"""

import requests
import time
import json
from typing import Dict, Tuple, Optional

class GoogleMapsCoordinateFinder:
    """Google Maps'ten koordinat bulucu"""
    
    def __init__(self):
        self.base_url = "https://www.google.com/maps/search/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_fire_station(self, query: str) -> Optional[Tuple[float, float]]:
        """İtfaiye arama sorgusu yap"""
        try:
            # Google Maps arama URL'i
            search_url = f"{self.base_url}{query.replace(' ', '+')}"
            
            print(f"🔍 Aranıyor: {query}")
            print(f"   📍 URL: {search_url}")
            
            # Google Maps'ten yanıt al
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                # HTML içeriğinden koordinatları çıkar
                content = response.text
                
                # Koordinat pattern'lerini ara
                patterns = [
                    r'@(-?\d+\.\d+),(-?\d+\.\d+)',
                    r'data-lat="(-?\d+\.\d+)" data-lng="(-?\d+\.\d+)"',
                    r'lat:(-?\d+\.\d+),lng:(-?\d+\.\d+)'
                ]
                
                for pattern in patterns:
                    import re
                    matches = re.findall(pattern, content)
                    if matches:
                        lat, lng = float(matches[0][0]), float(matches[0][1])
                        print(f"   ✅ Koordinat bulundu: ({lat}, {lng})")
                        return (lat, lng)
                
                print(f"   ❌ Koordinat bulunamadı")
                return None
                
            else:
                print(f"   ❌ HTTP Hatası: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            return None
    
    def find_all_fire_stations(self) -> Dict[str, Tuple[float, float]]:
        """Tüm itfaiyelerin koordinatlarını bul"""
        fire_stations = {
            # Bursa İlçe İtfaiyeleri
            "Bursa Merkez İtfaiye": "Bursa Büyükşehir Belediyesi İtfaiye Dairesi",
            "Nilüfer İtfaiye": "Nilüfer Belediyesi İtfaiye Müdürlüğü Bursa",
            "Osmangazi İtfaiye": "Osmangazi Belediyesi İtfaiye Müdürlüğü Bursa",
            "Yıldırım İtfaiye": "Yıldırım Belediyesi İtfaiye Müdürlüğü Bursa",
            "Mudanya İtfaiye": "Mudanya Belediyesi İtfaiye Müdürlüğü Bursa",
            "Gemlik İtfaiye": "Gemlik Belediyesi İtfaiye Müdürlüğü Bursa",
            "Karacabey İtfaiye": "Karacabey Belediyesi İtfaiye Müdürlüğü Bursa",
            "İnegöl İtfaiye": "İnegöl Belediyesi İtfaiye Müdürlüğü Bursa",
            "Orhangazi İtfaiye": "Orhangazi Belediyesi İtfaiye Müdürlüğü Bursa",
            "Kestel İtfaiye": "Kestel Belediyesi İtfaiye Müdürlüğü Bursa",
            "Gürsu İtfaiye": "Gürsu Belediyesi İtfaiye Müdürlüğü Bursa",
            "Harmancık İtfaiye": "Harmancık Belediyesi İtfaiye Müdürlüğü Bursa",
            "Büyükorhan İtfaiye": "Büyükorhan Belediyesi İtfaiye Müdürlüğü Bursa",
            "Orhaneli İtfaiye": "Orhaneli Belediyesi İtfaiye Müdürlüğü Bursa",
            
            # Balıkesir İlçe İtfaiyeleri
            "Balıkesir Merkez İtfaiye": "Balıkesir Büyükşehir Belediyesi İtfaiye Dairesi",
            "Bandırma İtfaiye": "Bandırma Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Gönen İtfaiye": "Gönen Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Erdek İtfaiye": "Erdek Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Ayvalık İtfaiye": "Ayvalık Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Edremit İtfaiye": "Edremit Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Burhaniye İtfaiye": "Burhaniye Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Havran İtfaiye": "Havran Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Dursunbey İtfaiye": "Dursunbey Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Sındırgı İtfaiye": "Sındırgı Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Bigadiç İtfaiye": "Bigadiç Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Susurluk İtfaiye": "Susurluk Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Kepsut İtfaiye": "Kepsut Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Manyas İtfaiye": "Manyas Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Savaştepe İtfaiye": "Savaştepe Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "İvrindi İtfaiye": "İvrindi Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Balya İtfaiye": "Balya Belediyesi İtfaiye Müdürlüğü Balıkesir",
            "Karesi İtfaiye": "Karesi Belediyesi İtfaiye Müdürlüğü Balıkesir",
            
            # Çanakkale İlçe İtfaiyeleri
            "Çanakkale Merkez İtfaiye": "Çanakkale Belediyesi İtfaiye Müdürlüğü",
            "Gelibolu İtfaiye": "Gelibolu Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Lapseki İtfaiye": "Lapseki Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Eceabat İtfaiye": "Eceabat Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Bozcaada İtfaiye": "Bozcaada Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Gökçeada İtfaiye": "Gökçeada Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Yenice İtfaiye": "Yenice Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Bayramiç İtfaiye": "Bayramiç Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Çan İtfaiye": "Çan Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Biga İtfaiye": "Biga Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Ayvacık İtfaiye": "Ayvacık Belediyesi İtfaiye Müdürlüğü Çanakkale",
            "Ezine İtfaiye": "Ezine Belediyesi İtfaiye Müdürlüğü Çanakkale",
            
            # Tekirdağ İlçe İtfaiyeleri
            "Tekirdağ Merkez İtfaiye": "Tekirdağ Büyükşehir Belediyesi İtfaiye Dairesi",
            "Çorlu İtfaiye": "Çorlu Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Çerkezköy İtfaiye": "Çerkezköy Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Süleymanpaşa İtfaiye": "Süleymanpaşa Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Malkara İtfaiye": "Malkara Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Saray İtfaiye": "Saray Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Ergene İtfaiye": "Ergene Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Kapaklı İtfaiye": "Kapaklı Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Şarköy İtfaiye": "Şarköy Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Hayrabolu İtfaiye": "Hayrabolu Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            "Muratlı İtfaiye": "Muratlı Belediyesi İtfaiye Müdürlüğü Tekirdağ",
            
            # Kırklareli İlçe İtfaiyeleri
            "Kırklareli Merkez İtfaiye": "Kırklareli Belediyesi İtfaiye Müdürlüğü",
            "Lüleburgaz İtfaiye": "Lüleburgaz Belediyesi İtfaiye Müdürlüğü Kırklareli",
            "Babaeski İtfaiye": "Babaeski Belediyesi İtfaiye Müdürlüğü Kırklareli",
            "Vize İtfaiye": "Vize Belediyesi İtfaiye Müdürlüğü Kırklareli",
            "Pınarhisar İtfaiye": "Pınarhisar Belediyesi İtfaiye Müdürlüğü Kırklareli",
            "Demirköy İtfaiye": "Demirköy Belediyesi İtfaiye Müdürlüğü Kırklareli",
            "Kofçaz İtfaiye": "Kofçaz Belediyesi İtfaiye Müdürlüğü Kırklareli",
            
            # Yalova İlçe İtfaiyeleri
            "Yalova Merkez İtfaiye": "Yalova Belediyesi İtfaiye Müdürlüğü",
            "Çınarcık İtfaiye": "Çınarcık Belediyesi İtfaiye Müdürlüğü Yalova",
            "Termal İtfaiye": "Termal Belediyesi İtfaiye Müdürlüğü Yalova",
            "Armutlu İtfaiye": "Armutlu Belediyesi İtfaiye Müdürlüğü Yalova",
            "Çiftlikköy İtfaiye": "Çiftlikköy Belediyesi İtfaiye Müdürlüğü Yalova",
            "Altınova İtfaiye": "Altınova Belediyesi İtfaiye Müdürlüğü Yalova"
        }
        
        results = {}
        
        print("🗺️ GOOGLE MAPS KOORDİNAT BULUCU BAŞLIYOR...")
        print("=" * 60)
        print("⚠️  NOT: Bu script Google Maps'ten koordinat çekmeye çalışır")
        print("   Ancak Google Maps API kısıtlamaları nedeniyle")
        print("   manuel olarak koordinatları girmeniz gerekebilir.")
        print("=" * 60)
        
        for name, query in fire_stations.items():
            print(f"\n🔍 {name}")
            coords = self.search_fire_station(query)
            
            if coords:
                results[name] = coords
                print(f"   ✅ {name}: {coords}")
            else:
                print(f"   ❌ {name}: Koordinat bulunamadı")
            
            # Rate limiting
            time.sleep(2)
        
        return results
    
    def save_results(self, results: Dict[str, Tuple[float, float]], filename: str = "updated_fire_stations.json"):
        """Sonuçları JSON dosyasına kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Sonuçlar kaydedildi: {filename}")
        except Exception as e:
            print(f"❌ Kaydetme hatası: {e}")

def main():
    """Ana fonksiyon"""
    finder = GoogleMapsCoordinateFinder()
    
    try:
        # Tüm itfaiyeleri ara
        results = finder.find_all_fire_stations()
        
        # Sonuçları göster
        print(f"\n📊 TOPLAM SONUÇ:")
        print(f"   ✅ Bulunan: {len(results)}")
        print(f"   ❌ Bulunamayan: {69 - len(results)}")
        
        # Sonuçları kaydet
        finder.save_results(results)
        
        # Güncellenmiş fire_stations.py için kod üret
        print(f"\n📝 GÜNCELLENMİŞ FIRE_STATIONS.PY KODU:")
        print("=" * 60)
        
        for name, coords in results.items():
            print(f'        "{name}": {coords},  # Google Maps\'ten güncellenmiş')
        
    except Exception as e:
        print(f"❌ Ana hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
