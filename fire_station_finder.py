#!/usr/bin/env python3
"""
🔍 OTOMATİK İTFAİYE BULUCU 🔍
TomTom API kullanarak yangın noktasına en yakın itfaiyeleri otomatik bulur
"""

import asyncio
import aiohttp
from typing import Dict, List, Tuple, Optional
import config
from tomtom_api import TomTomAPI
from fire_stations import load_fire_stations
import time
import logging

logger = logging.getLogger(__name__)

class FireStationFinder:
    """Otomatik itfaiye bulucu - TomTom API entegrasyonu"""
    
    def __init__(self, tomtom_api: TomTomAPI):
        self.tomtom_api = tomtom_api
        self.cache = {}  # Basit önbellek
        self.cache_duration = 3600  # 1 saat cache
        self.last_api_call = 0  # Rate limiting için
        self.min_api_interval = 1.0  # API çağrıları arası minimum süre (saniye)
        logger.info("FireStationFinder başlatıldı")
        
    async def _rate_limit(self):
        """TomTom API rate limiting kontrolü"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call
        
        if time_since_last_call < self.min_api_interval:
            wait_time = self.min_api_interval - time_since_last_call
            logger.warning(f"Rate limit aşıldı. {wait_time:.1f} saniye bekleniyor.")
            await asyncio.sleep(wait_time)
        
        self.last_api_call = time.time()  # Son çağrı zamanını güncelle
        
    async def find_nearby_fire_stations(
        self, 
        fire_location: Tuple[float, float], 
        radius_km: float = 100.0,  # Arama yarıçapını artır
        max_results: int = 20       # Daha fazla sonuç al
    ) -> List[Dict]:
        """
        Yangın noktasına yakın itfaiyeleri bul
        
        Args:
            fire_location: (lat, lon) yangın koordinatları
            radius_km: Arama yarıçapı (km)
            max_results: Maksimum sonuç sayısı
            
        Returns:
            İtfaiye listesi: [{'name': str, 'coords': (lat, lon), 'distance': float, 'address': str}]
        """
        fire_lat, fire_lon = fire_location
        
        # Önbellekte varsa kullan
        cache_key = f"{fire_lat:.4f}_{fire_lon:.4f}_{radius_km}"
        if cache_key in self.cache:
            print(f"✅ Önbellekten itfaiye verileri alındı")
            return self.cache[cache_key]
        
        print(f"🔍 {radius_km} km yarıçapında itfaiye aranıyor...")
        
        try:
            # TomTom API ile yakındaki itfaiyeleri ara - Daha kapsamlı arama
            search_queries = [
                "itfaiye istasyonu",
                "fire station",
                "itfaiye",
                "yangın istasyonu",
                "acil servis"
            ]
            
            all_results = []
            
            for search_query in search_queries:
                # Arama parametreleri
                params = {
                    'query': search_query,
                    'limit': max_results,
                    'radius': int(radius_km * 1000),  # m cinsinden
                    'lat': fire_lat,
                    'lon': fire_lon,
                    'categorySet': '7315,7316,7317',  # Acil servis kategorileri
                    'idxSet': 'Poi,Addr',  # POI ve adres arama
                    'language': 'tr-TR,en-US'  # Türkçe ve İngilizce
                }
            
            # API çağrısı yap
            async with aiohttp.ClientSession() as session:
                url = f"https://api.tomtom.com/search/2/poiSearch/{search_query}.json"
                params['key'] = config.TOMTOM_API_KEY
                
                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'results' in data and data['results']:
                            all_results.extend(data['results'])
                    else:
                        print(f"⚠️ {search_query} araması hatası: {response.status}")
            
            # Tüm sonuçları işle
            if all_results:
                return await self._process_fire_station_results({'results': all_results}, fire_location)
            else:
                print("❌ Hiç sonuç bulunamadı, fallback kullanılıyor")
                return await self._fallback_search(fire_location, radius_km)
                        
        except Exception as e:
            print(f"❌ İtfaiye arama hatası: {e}")
            return await self._fallback_search(fire_location, radius_km)
    
    async def _process_fire_station_results(
        self, 
        api_data: Dict, 
        fire_location: Tuple[float, float]
    ) -> List[Dict]:
        """TomTom API sonuçlarını işle"""
        fire_stations = []
        fire_lat, fire_lon = fire_location
        
        if 'results' not in api_data:
            print("⚠️ API sonuçları bulunamadı")
            return []
        
        for result in api_data['results']:
            try:
                # Koordinatları al
                position = result.get('position', {})
                lat = position.get('lat')
                lon = position.get('lon')
                
                if lat is None or lon is None:
                    continue
                
                # Mesafeyi hesapla (Haversine)
                distance = self._haversine_distance(fire_lat, fire_lon, lat, lon)
                
                # Sadece itfaiye ile ilgili sonuçları filtrele
                name = result.get('poi', {}).get('name', '')
                category = result.get('poi', {}).get('categorySet', [])
                
                if self._is_fire_station(name, category):
                    fire_stations.append({
                        'name': name,
                        'coords': (lat, lon),
                        'distance': distance,
                        'address': result.get('address', {}).get('freeformAddress', 'Adres bilgisi yok'),
                        'phone': result.get('poi', {}).get('phone', ''),
                        'website': result.get('poi', {}).get('url', ''),
                        'source': 'TomTom API'
                    })
                    
            except Exception as e:
                print(f"⚠️ Sonuç işleme hatası: {e}")
                continue
        
        # Mesafeye göre sırala
        fire_stations.sort(key=lambda x: x['distance'])
        
        # Önbelleğe kaydet
        cache_key = f"{fire_lat:.4f}_{fire_lon:.4f}_50.0"
        self.cache[cache_key] = fire_stations
        
        print(f"✅ {len(fire_stations)} itfaiye bulundu")
        return fire_stations
    
    def _is_fire_station(self, name: str, category: List) -> bool:
        """Metin ve kategoriye göre itfaiye olup olmadığını kontrol et"""
        name_lower = name.lower()
        
        # İtfaiye anahtar kelimeleri
        fire_keywords = [
            'itfaiye', 'fire', 'fire station', 'fire department',
            'yangın', 'acil', 'emergency', 'kurtarma', 'rescue'
        ]
        
        # Kategori kontrolü (acil servis)
        emergency_categories = ['7315', '7316', '7317']  # Acil servis kategorileri
        
        # İsim kontrolü
        name_match = any(keyword in name_lower for keyword in fire_keywords)
        
        # Kategori kontrolü
        category_match = any(cat.get('id') in emergency_categories for cat in category)
        
        return name_match or category_match
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """İki nokta arası mesafeyi hesapla (km)"""
        import math
        
        # Dereceyi radyana çevir
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formülü
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Dünya yarıçapı (km)
        r = 6371
        
        return c * r
    
    async def _fallback_search(
        self, 
        fire_location: Tuple[float, float], 
        radius_km: float
    ) -> List[Dict]:
        """API hatası durumunda fallback arama"""
        print("🔄 Fallback arama yapılıyor...")
        
        fire_lat, fire_lon = fire_location
        
        # Basit grid arama - belirli aralıklarla itfaiye ara
        fire_stations = []
        
        # İzmir ve Manisa illerine ait doğrulanmış istasyonlar
        known_stations = load_fire_stations()
        
        for name, coords in known_stations.items():
            distance = self._haversine_distance(fire_lat, fire_lon, coords[0], coords[1])
            
            if distance <= radius_km:
                fire_stations.append({
                    'name': name,
                    'coords': coords,
                    'distance': distance,
                    'address': f"{name} - Bilinen konum",
                    'phone': '',
                    'website': '',
                    'source': 'Fallback Database'
                })
        
        # Mesafeye göre sırala
        fire_stations.sort(key=lambda x: x['distance'])
        
        print(f"✅ Fallback ile {len(fire_stations)} itfaiye bulundu")
        return fire_stations
    
    async def get_nearest_fire_station(
        self, 
        fire_location: Tuple[float, float]
    ) -> Optional[Dict]:
        """En yakın itfaiyeyi bul"""
        fire_stations = await self.find_nearby_fire_stations(fire_location)
        
        if not fire_stations:
            return None
        
        nearest = fire_stations[0]
        print(f"🎯 En yakın itfaiye: {nearest['name']} ({nearest['distance']:.1f} km)")
        return nearest
    
    async def get_multiple_fire_stations(
        self, 
        fire_location: Tuple[float, float], 
        count: int = 3
    ) -> List[Dict]:
        """En yakın birkaç itfaiyeyi bul"""
        fire_stations = await self.find_nearby_fire_stations(fire_location)
        
        if not fire_stations:
            return []
        
        # En yakın 'count' kadar itfaiyeyi döndür
        return fire_stations[:count]

# Test fonksiyonu
async def test_fire_station_finder():
    """İtfaiye bulucuyu test et"""
    print("🧪 İtfaiye Bulucu Test Ediliyor...")
    
    # TomTom API'yi başlat
    tomtom_api = TomTomAPI()
    
    # FireStationFinder'ı başlat
    finder = FireStationFinder(tomtom_api)
    
    # Test yangın noktası (İzmir Konak)
    test_fire_location = (38.4230, 27.1533)
    
    print(f"🔥 Test yangın noktası: {test_fire_location}")
    
    # En yakın itfaiyeyi bul
    nearest = await finder.get_nearest_fire_station(test_fire_location)
    
    if nearest:
        print(f"\n✅ Test başarılı!")
        print(f"   🚒 İtfaiye: {nearest['name']}")
        print(f"   📍 Konum: {nearest['coords']}")
        print(f"   📏 Mesafe: {nearest['distance']:.1f} km")
        print(f"   🏠 Adres: {nearest['address']}")
        print(f"   📱 Telefon: {nearest['phone']}")
        print(f"   🌐 Website: {nearest['website']}")
        print(f"   🔗 Kaynak: {nearest['source']}")
    else:
        print("❌ Test başarısız - itfaiye bulunamadı")
    
    # Birden fazla itfaiye bul
    print(f"\n🔍 En yakın 3 itfaiye aranıyor...")
    multiple = await finder.get_multiple_fire_stations(test_fire_location, 3)
    
    for i, station in enumerate(multiple, 1):
        print(f"   {i}. {station['name']} - {station['distance']:.1f} km")

if __name__ == "__main__":
    asyncio.run(test_fire_station_finder())
