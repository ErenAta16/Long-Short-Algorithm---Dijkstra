#!/usr/bin/env python3
"""
🚨 YANGIN ACİL DURUM SİSTEMİ 🚨
TomTom Haritası Üzerinden Yangın Noktası Seçimi ve En Yakın İtfaiye Yönlendirmesi
Tali yolları önceliklendiren akıllı rota sistemi
"""

import folium
from typing import Dict, List, Tuple, Optional
# from route_planner import RoutePlanner  # Artık kullanılmıyor
from tomtom_api import TomTomAPI
from fire_stations import load_fire_stations, categorize_fire_stations
from map_utils import create_interactive_map, create_emergency_route_map
import route_calculator
import config

class FireEmergencySystem:
    """Yangın acil durum sistemi - Tali yolları önceliklendir"""
    
    def __init__(self):
        """Sistemi başlat"""
        self.api = TomTomAPI(config.TOMTOM_API_KEY)
        # self.planner = RoutePlanner(self.api)  # Artık kullanılmıyor
        self.fire_stations = load_fire_stations()
        self.current_fire_location = None
        
    def create_interactive_map(self) -> str:
        """Etkileşimli harita oluştur - Yangın noktası seçimi için"""
        return create_interactive_map(self.fire_stations)
        
    async def analyze_fire_location(self, fire_lat: float, fire_lon: float) -> Dict:
        """Yangın noktasını analiz et ve en yakın itfaiyeyi bul - Tali yolları önceliklendir"""
        fire_location = (fire_lat, fire_lon)
        self.current_fire_location = fire_location
        
        print(f"🔥 Yangın noktası analiz ediliyor: {fire_lat:.6f}, {fire_lon:.6f}")
        
        # Acil durum rotasını analiz et - TomTom API ile otomatik itfaiye bulma
        route_info = await route_calculator.analyze_emergency_route(fire_location, self.fire_stations, self.api)
        
        if "error" in route_info:
            print(f"❌ Hata: {route_info['error']}")
            return route_info
        
        # Sonuçları göster
        nearest_station = route_info['nearest_station']
        distance = route_info.get('base_route', {}).get('distance', 0)
        duration = route_info.get('base_route', {}).get('duration', 0)
        route_type = route_info.get('base_route', {}).get('route_type', 'Bilinmiyor')
        terrain_type = route_info.get('terrain_type', 'Bilinmiyor')
        secondary_ratio = route_info.get('base_route', {}).get('secondary_ratio', 0)
        
        print(f"\n🎯 ANALİZ SONUÇLARI:")
        print(f"   📍 En yakın itfaiye: {nearest_station}")
        print(f"   🗺️ Arazi türü: {terrain_type}")
        print(f"   🛣️ Rota türü: {route_type}")
        print(f"   📏 Toplam mesafe: {distance/1000:.1f} km")
        print(f"   ⏱️ Tahmini süre: {duration/60:.1f} dakika")
        print(f"   🌾 Tali yol oranı: {secondary_ratio*100:.1f}%")
        
        # Yol türleri detayı
        road_types = route_info.get('road_types', {})
        if road_types:
            print(f"   🛣️ Yol türleri:")
            for rt, dist in road_types.items():
                print(f"      - {rt}: {dist/1000:.1f} km")
        
        # Arazi türüne göre özel bilgi
        if terrain_type == "mountain_forest":
            print(f"   🏔️ Dağ/orman yangını tespit edildi!")
            print(f"   💡 Tali yollar ve köy yolları önceliklendirildi")
        elif terrain_type == "rural":
            print(f"   🌾 Kırsal yangın tespit edildi!")
            print(f"   💡 Tali yollar tercih edildi")
        else:
            print(f"   🏙️ Şehir yangını tespit edildi!")
            print(f"   💡 Normal rota profilleri kullanıldı")
        
        return route_info
    
    def create_emergency_route_map(self, route_info: Dict) -> str:
        """Acil durum rota haritası oluştur - Tali yolları önceliklendir"""
        if not self.current_fire_location:
            print("❌ Önce yangın noktası belirleyin!")
            return ""
        
        if "error" in route_info:
            print(f"❌ Harita oluşturulamadı: {route_info['error']}")
            return ""
        
        nearest_station = route_info['nearest_station']
        
        print(f"\n🗺️ Acil durum rota haritası oluşturuluyor...")
        print(f"   📍 Yangın noktası: {self.current_fire_location}")
        print(f"   🚒 En yakın itfaiye: {nearest_station}")
        print(f"   🗺️ Arazi türü: {route_info.get('terrain_type', 'Bilinmiyor')}")
        print(f"   🌾 Tali yol oranı: {route_info.get('secondary_ratio', 0)*100:.1f}%")
        
        map_file = create_emergency_route_map(
            self.fire_stations,
            self.current_fire_location,
            nearest_station,
            route_info
        )
        
        print(f"✅ Harita oluşturuldu: {map_file}")
        return map_file

async def main():
    """Ana program"""
    system = FireEmergencySystem()
    
    print("🚨 YANGIN ACİL DURUM SİSTEMİ 🚨")
    print("🌾 Tali Yolları Önceliklendiren Akıllı Rota Sistemi")
    print("🔍 Otomatik İtfaiye Bulma Sistemi Aktif")
    print("=" * 60)
    
    while True:
        print("\n📋 MENÜ:")
        print("1. Etkileşimli harita oluştur")
        print("2. Koordinat ile yangın analizi")
        print("3. İtfaiye istasyonlarını listele")
        print("4. Çıkış")
        
        choice = input("\nSeçiminizi yapın (1-4): ").strip()
        
        if choice == "1":
            print("\n🗺️ Etkileşimli harita oluşturuluyor...")
            map_file = system.create_interactive_map()
            print(f"✅ Harita oluşturuldu: {map_file}")
            print("🌐 Tarayıcınızda açarak yangın noktası seçebilirsiniz!")
            
        elif choice == "2":
            print("\n🔥 Koordinat ile yangın analizi")
            print("💡 Sistem otomatik olarak arazi türünü belirler ve tali yolları önceliklendirir!")
            try:
                fire_lat = float(input("Yangın noktası enlem (latitude): "))
                fire_lon = float(input("Yangın noktası boylam (longitude): "))
                
                route_info = await system.analyze_fire_location(fire_lat, fire_lon)
                
                if "error" not in route_info:
                    # Harita oluştur
                    map_file = system.create_emergency_route_map(route_info)
                    if map_file:
                        print(f"\n🎯 Acil durum analizi tamamlandı!")
                        print(f"📊 Detaylı sonuçlar: {map_file}")
                        print(f"🌾 Tali yol oranı: {route_info.get('secondary_ratio', 0)*100:.1f}%")
                
            except ValueError:
                print("❌ Geçersiz koordinat! Sayısal değer girin.")
            except Exception as e:
                print(f"❌ Hata: {e}")
                
        elif choice == "3":
            print("\n🚒 İTFAİYE İSTASYONLARI:")
            print("-" * 50)
            print(f"📊 Toplam {len(system.fire_stations)} itfaiye istasyonu bulundu!")
            print("-" * 50)
            
            # Bölgelere göre grupla
            regions = categorize_fire_stations(system.fire_stations)
            
            # Her bölgeyi ayrı ayrı göster
            for region_name, stations in regions.items():
                if stations:
                    print(f"\n📍 {region_name} ({len(stations)} istasyon):")
                    print("-" * 40)
                    for i, (name, coords) in enumerate(stations, 1):
                        print(f"  {i:2d}. {name:<25} {coords[0]:.6f}, {coords[1]:.6f}")
                        
        elif choice == "4":
            print("\n👋 Sistem kapatılıyor...")
            break
            
        else:
            print("❌ Geçersiz seçim! 1-4 arası bir sayı girin.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
