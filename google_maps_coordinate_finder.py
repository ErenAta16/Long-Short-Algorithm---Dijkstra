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
            # İzmir İlçe İtfaiyeleri
            "İzmir Konak İtfaiye": "İzmir Büyükşehir Belediyesi İtfaiye Dairesi Başkanlığı Konak İzmir",
            "İzmir Bornova İtfaiye": "Bornova Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Karşıyaka İtfaiye": "Karşıyaka Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Çiğli İtfaiye": "Çiğli Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Gaziemir İtfaiye": "Gaziemir Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Bayraklı İtfaiye": "Bayraklı Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Narlıdere İtfaiye": "Narlıdere Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Balçova İtfaiye": "Balçova Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Buca İtfaiye": "Buca Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Foça İtfaiye": "Foça Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Menemen İtfaiye": "Menemen Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Dikili İtfaiye": "Dikili Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Aliağa İtfaiye": "Aliağa Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Bergama İtfaiye": "Bergama Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Ödemiş İtfaiye": "Ödemiş Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Tire İtfaiye": "Tire Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Torbalı İtfaiye": "Torbalı Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Menderes İtfaiye": "Menderes Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Urla İtfaiye": "Urla Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Çeşme İtfaiye": "Çeşme Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Karaburun İtfaiye": "Karaburun Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Seferihisar İtfaiye": "Seferihisar Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Bayındır İtfaiye": "Bayındır Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Kiraz İtfaiye": "Kiraz Belediyesi İtfaiye Müdürlüğü İzmir",
            "İzmir Kemalpaşa İtfaiye": "Kemalpaşa Belediyesi İtfaiye Müdürlüğü İzmir",
            
            # Manisa İlçe İtfaiyeleri
            "Manisa Merkez İtfaiye": "Manisa Büyükşehir Belediyesi İtfaiye Dairesi Başkanlığı",
            "Manisa Yunusemre İtfaiye": "Yunusemre Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Şehzadeler İtfaiye": "Şehzadeler Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Akhisar İtfaiye": "Akhisar Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Salihli İtfaiye": "Salihli Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Turgutlu İtfaiye": "Turgutlu Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Soma İtfaiye": "Soma Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Kırkağaç İtfaiye": "Kırkağaç Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Alaşehir İtfaiye": "Alaşehir Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Demirci İtfaiye": "Demirci Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Sarıgöl İtfaiye": "Sarıgöl Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Kula İtfaiye": "Kula Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Gördes İtfaiye": "Gördes Belediyesi İtfaiye Müdürlüğü Manisa",
            "Manisa Ahmetli İtfaiye": "Ahmetli Belediyesi İtfaiye Müdürlüğü Manisa"
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
        print(f"   ❌ Bulunamayan: {39 - len(results)}")
        
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
