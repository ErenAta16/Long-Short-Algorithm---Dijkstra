#!/usr/bin/env python3
"""
🔥 TOMTOM API İTFAİYE VERİ ÇEKİCİ 🔥
TomTom API kullanarak itfaiye verilerini çeken basit ve etkili sistem
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Tuple, Optional
import config

class TomTomFireStationAPI:
    """TomTom API ile itfaiye verilerini çeken sistem"""
    
    def __init__(self):
        self.api_key = config.TOMTOM_API_KEY
        self.base_url = "https://api.tomtom.com"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_fire_stations_nearby(
        self, 
        lat: float, 
        lon: float, 
        radius_km: int = 50
    ) -> List[Dict]:
        """Belirli bir nokta etrafında itfaiye ara"""
        
        print(f"🔍 ({lat}, {lon}) etrafında {radius_km} km yarıçapında itfaiye aranıyor...")
        
        # TomTom POI Search API endpoint
        endpoint = f"{self.base_url}/search/2/poiSearch/itfaiye.json"
        
        params = {
            'key': self.api_key,
            'lat': lat,
            'lon': lon,
            'radius': radius_km * 1000,  # m cinsinden
            'limit': 50,
            'idxSet': 'Poi',
            'language': 'tr-TR'
        }
        
        try:
            async with self.session.get(endpoint, params=params, timeout=30) as response:
                print(f"📡 API Yanıt Kodu: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API yanıtı başarılı")
                    return self._parse_poi_results(data)
                else:
                    error_text = await response.text()
                    print(f"❌ API Hatası: {response.status}")
                    print(f"📄 Hata Detayı: {error_text}")
                    return []
                    
        except Exception as e:
            print(f"❌ Bağlantı Hatası: {e}")
            return []
    
    async def search_fire_stations_by_query(
        self, 
        query: str, 
        lat: float = None, 
        lon: float = None
    ) -> List[Dict]:
        """Sorgu ile itfaiye ara"""
        
        print(f"🔍 '{query}' sorgusu ile itfaiye aranıyor...")
        
        # URL encoding yap
        encoded_query = query.replace(' ', '%20')
        endpoint = f"{self.base_url}/search/2/poiSearch/{encoded_query}.json"
        
        params = {
            'key': self.api_key,
            'limit': 50,
            'idxSet': 'Poi',
            'language': 'tr-TR'
        }
        
        # Eğer koordinat verilmişse ekle
        if lat and lon:
            params['lat'] = lat
            params['lon'] = lon
            params['radius'] = 100000  # 100 km
        
        try:
            async with self.session.get(endpoint, params=params, timeout=30) as response:
                print(f"📡 API Yanıt Kodu: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API yanıtı başarılı")
                    return self._parse_poi_results(data)
                else:
                    error_text = await response.text()
                    print(f"❌ API Hatası: {response.status}")
                    print(f"📄 Hata Detayı: {error_text}")
                    return []
                    
        except Exception as e:
            print(f"❌ Bağlantı Hatası: {e}")
            return []
    
    async def search_emergency_services(
        self, 
        lat: float, 
        lon: float, 
        radius_km: int = 100
    ) -> List[Dict]:
        """Acil servis kategorisinde itfaiye ara"""
        
        print(f"🚨 ({lat}, {lon}) etrafında acil servis aranıyor...")
        
        # TomTom POI Search API endpoint - sadece acil servis kategorisi
        endpoint = f"{self.base_url}/search/2/poiSearch.json"
        
        params = {
            'key': self.api_key,
            'lat': lat,
            'lon': lon,
            'radius': radius_km * 1000,  # m cinsinden
            'limit': 100,
            'categorySet': '7315,7316,7317',  # Acil servis kategorileri
            'idxSet': 'Poi',
            'language': 'tr-TR'
        }
        
        try:
            async with self.session.get(endpoint, params=params, timeout=30) as response:
                print(f"📡 API Yanıt Kodu: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API yanıtı başarılı")
                    return self._parse_emergency_results(data)
                else:
                    error_text = await response.text()
                    print(f"❌ API Hatası: {response.status}")
                    print(f"📄 Hata Detayı: {error_text}")
                    return []
                    
        except Exception as e:
            print(f"❌ Bağlantı Hatası: {e}")
            return []
    
    async def search_specific_fire_stations(
        self, 
        lat: float, 
        lon: float, 
        radius_km: int = 100
    ) -> List[Dict]:
        """Spesifik itfaiye arama terimleri ile ara"""
        
        print(f"🔥 ({lat}, {lon}) etrafında spesifik itfaiye araması...")
        
        all_stations = []
        
        # Spesifik arama terimleri
        search_terms = [
            "itfaiye istasyonu",
            "fire station",
            "yangın istasyonu",
            "acil servis istasyonu"
        ]
        
        for term in search_terms:
            try:
                stations = await self.search_fire_stations_by_query(term, lat, lon)
                if stations:
                    all_stations.extend(stations)
                    print(f"   🔍 '{term}': {len(stations)} sonuç")
                
                await asyncio.sleep(0.5)  # Rate limit
                
            except Exception as e:
                print(f"   ⚠️ '{term}' araması hatası: {e}")
                continue
        
        return all_stations
    
    def _parse_poi_results(self, data: Dict) -> List[Dict]:
        """POI arama sonuçlarını işle"""
        fire_stations = []
        
        if 'results' not in data:
            print("⚠️ Sonuç bulunamadı")
            return fire_stations
        
        results = data['results']
        print(f"📊 {len(results)} sonuç bulundu")
        
        for result in results:
            try:
                # Koordinatları al
                position = result.get('position', {})
                lat = position.get('lat')
                lon = position.get('lon')
                
                if lat is None or lon is None:
                    continue
                
                # İtfaiye olup olmadığını kontrol et
                poi = result.get('poi', {})
                name = poi.get('name', '')
                
                if not self._is_fire_station(name):
                    continue
                
                # Adres bilgisini al
                address = result.get('address', {})
                freeform_address = address.get('freeformAddress', '')
                
                # Telefon ve website bilgilerini al
                phone = poi.get('phone', '')
                website = poi.get('url', '')
                
                fire_stations.append({
                    'name': name,
                    'coords': (lat, lon),
                    'address': freeform_address,
                    'phone': phone,
                    'website': website,
                    'source': 'TomTom API'
                })
                
            except Exception as e:
                continue
        
        print(f"✅ {len(fire_stations)} itfaiye bulundu")
        return fire_stations
    
    def _parse_emergency_results(self, data: Dict) -> List[Dict]:
        """Acil servis arama sonuçlarını işle"""
        fire_stations = []
        
        if 'results' not in data:
            print("⚠️ Sonuç bulunamadı")
            return fire_stations
        
        results = data['results']
        print(f"📊 {len(results)} acil servis sonucu bulundu")
        
        for result in results:
            try:
                # Koordinatları al
                position = result.get('position', {})
                lat = position.get('lat')
                lon = position.get('lon')
                
                if lat is None or lon is None:
                    continue
                
                # İtfaiye olup olmadığını kontrol et
                poi = result.get('poi', {})
                name = poi.get('name', '')
                categories = poi.get('categorySet', [])
                
                if not self._is_real_fire_station(name, categories):
                    continue
                
                # Adres bilgisini al
                address = result.get('address', {})
                freeform_address = address.get('freeformAddress', '')
                
                # Telefon ve website bilgilerini al
                phone = poi.get('phone', '')
                website = poi.get('url', '')
                
                fire_stations.append({
                    'name': name,
                    'coords': (lat, lon),
                    'address': freeform_address,
                    'phone': phone,
                    'website': website,
                    'source': 'TomTom API - Emergency Services'
                })
                
            except Exception as e:
                continue
        
        print(f"✅ {len(fire_stations)} gerçek itfaiye bulundu")
        return fire_stations
    
    def _is_fire_station(self, name: str) -> bool:
        """İsim itfaiye ile ilgili mi kontrol et (eski yöntem)"""
        if not name:
            return False
            
        name_lower = name.lower()
        
        fire_keywords = [
            'itfaiye', 'fire', 'fire station', 'fire department',
            'yangın', 'acil', 'emergency', 'kurtarma', 'rescue'
        ]
        
        return any(keyword in name_lower for keyword in fire_keywords)
    
    def _is_real_fire_station(self, name: str, categories: List) -> bool:
        """Gerçek itfaiye istasyonu mu kontrol et (gelişmiş yöntem)"""
        if not name:
            return False
            
        name_lower = name.lower()
        
        # Restoran, kafe gibi yanlış sonuçları filtrele
        false_positive_keywords = [
            'restaurant', 'cafe', 'bar', 'pub', 'grill', 'bbq',
            'pizza', 'wok', 'flavor', 'house', 'kitchen', 'food',
            'dining', 'eatery', 'bistro', 'tavern', 'lounge',
            'aperatif', 'büfe', 'snack', 'fast food'
        ]
        
        # Eğer restoran/kafe gibi kelimeler varsa, itfaiye değil
        if any(keyword in name_lower for keyword in false_positive_keywords):
            return False
        
        # Gerçek itfaiye anahtar kelimeleri
        real_fire_keywords = [
            'itfaiye istasyonu', 'fire station', 'fire department',
            'yangın istasyonu', 'acil servis', 'emergency service',
            'kurtarma istasyonu', 'rescue station'
        ]
        
        # Tam eşleşme kontrolü
        for keyword in real_fire_keywords:
            if keyword in name_lower:
                return True
        
        # Kategori kontrolü - acil servis kategorilerinde olmalı
        emergency_categories = ['7315', '7316', '7317']
        category_ids = [cat.get('id') for cat in categories if cat.get('id')]
        
        if any(cat_id in emergency_categories for cat_id in category_ids):
            # Kategori doğru ama isim kontrolü de yap
            if any(keyword in name_lower for keyword in ['itfaiye', 'fire', 'emergency', 'acil']):
                return True
        
        return False
    
    async def test_api_connection(self):
        """API bağlantısını test et"""
        print("🧪 TOMTOM API BAĞLANTI TESTİ")
        print("=" * 40)
        
        # Test 1: Spesifik itfaiye arama
        print("\n1️⃣ Spesifik itfaiye arama testi...")
        test_coords = (40.1926, 29.0766)  # Bursa
        results = await self.search_specific_fire_stations(test_coords[0], test_coords[1], 100)
        
        if results:
            print("✅ Spesifik itfaiye araması başarılı")
            for i, station in enumerate(results[:5], 1):
                print(f"   {i}. {station['name']} - {station['coords']}")
        else:
            print("❌ Spesifik itfaiye araması başarısız")
        
        # Test 2: Acil servis kategorisinde arama
        print("\n2️⃣ Acil servis kategorisinde arama testi...")
        emergency_results = await self.search_emergency_services(test_coords[0], test_coords[1], 100)
        
        if emergency_results:
            print("✅ Acil servis araması başarılı")
            for i, station in enumerate(emergency_results[:5], 1):
                print(f"   {i}. {station['name']} - {station['coords']}")
        else:
            print("❌ Acil servis araması başarısız")

async def main():
    """Ana test fonksiyonu"""
    print("🚀 TomTom API İtfaiye Veri Çekici Test Ediliyor...")
    
    async with TomTomFireStationAPI() as api:
        await api.test_api_connection()

if __name__ == "__main__":
    asyncio.run(main())
