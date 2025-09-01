#!/usr/bin/env python3
"""
TomTom API Entegrasyonu
Harita ve rota verilerini çeker
"""

import requests
import time
import json
from typing import Dict, List, Tuple, Optional
import config

class TomTomAPI:
    """TomTom API entegrasyonu"""
    
    def __init__(self, api_key: str = None):
        """API'yi başlat"""
        self.api_key = api_key or config.TOMTOM_API_KEY
        self.base_url = "https://api.tomtom.com"
        self.last_request_time = 0
        self.request_delay = 1.0 / config.MAX_REQUESTS_PER_MINUTE  # Saniye
    
    def _rate_limit(self):
        """API rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """GET isteği gönder"""
        try:
            self._rate_limit()
            
            url = f"{self.base_url}{endpoint}"
            params = params or {}
            params['key'] = self.api_key
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ TomTom API hatası: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ TomTom API isteği hatası: {e}")
            return None
    
    def search_places(self, query: str, country: str = "TR") -> Optional[List[Dict]]:
        """Yer arama"""
        endpoint = "/search/2/search"
        params = {
            'query': query,
            'countrySet': country,
            'limit': 5
        }
        
        return self._get(endpoint, params)
    
    def get_place_coordinates(self, place_name: str) -> Optional[Tuple[float, float]]:
        """Yer adından koordinat al"""
        try:
            result = self.search_places(place_name)
            
            if result and 'results' in result and result['results']:
                position = result['results'][0]['position']
                return position['lat'], position['lon']
            
            return None
            
        except Exception as e:
            print(f"⚠️ Koordinat alma hatası: {e}")
            return None
    
    def get_route(self, start_lat: float, start_lon: float, 
                  end_lat: float, end_lon: float, 
                  route_type: str = "fastest") -> Optional[Dict]:
        """Rota al"""
        endpoint = "/routing/1/calculateRoute"
        
        # Koordinatları string olarak birleştir
        coords = f"{start_lat},{start_lon}:{end_lat},{end_lon}"
        
        params = {
            'routeType': route_type,
            'traffic': 'false',
            'avoid': 'unpavedRoads',
            'travelMode': 'car',
            'sectionType': 'traffic',
            'report': 'effectiveSettings'
        }
        
        url = f"{self.base_url}{endpoint}/{coords}/json"
        params['key'] = self.api_key
        
        try:
            self._rate_limit()
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Rota alma hatası: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Rota alma hatası: {e}")
            return None
    
    def get_road_network(self, bounds: Tuple[float, float, float, float]) -> Optional[Dict]:
        """Yol ağı verisi al"""
        # Bu özellik TomTom API'nin ücretsiz versiyonunda mevcut değil
        # Offline veri kullanılacak
        return None
    
    def extract_route_polyline(self, route_data: Dict) -> Optional[List[List[float]]]:
        """Rota verisinden koordinat listesi çıkar"""
        try:
            if 'routes' in route_data and route_data['routes']:
                route = route_data['routes'][0]
                
                if 'legs' in route and route['legs']:
                    leg = route['legs'][0]
                    
                    if 'points' in leg:
                        # Nokta listesi varsa
                        points = leg['points']
                        coords = []
                        
                        for point in points:
                            if 'latitude' in point and 'longitude' in point:
                                coords.append([point['latitude'], point['longitude']])
                        
                        return coords
                    
                    elif 'summary' in leg:
                        # Sadece özet bilgi varsa, başlangıç ve bitiş noktalarını kullan
                        start = route.get('start', {})
                        end = route.get('end', {})
                        
                        if start and end:
                            start_lat = start.get('lat', start.get('latitude'))
                            start_lon = start.get('lon', start.get('longitude'))
                            end_lat = end.get('lat', end.get('latitude'))
                            end_lon = end.get('lon', end.get('longitude'))
                            
                            if all([start_lat, start_lon, end_lat, end_lon]):
                                return [[start_lat, start_lon], [end_lat, end_lon]]
            
            return None
            
        except Exception as e:
            print(f"⚠️ Polyline çıkarma hatası: {e}")
            return None
    
    def get_traffic_info(self, lat: float, lon: float, radius: int = 5000) -> Optional[Dict]:
        """Trafik bilgisi al"""
        endpoint = "/traffic/1/incidentDetails"
        params = {
            'bbox': f"{lon-radius/1000},{lat-radius/1000},{lon+radius/1000},{lat+radius/1000}",
            'fields': 'incidents'
        }
        
        return self._get(endpoint, params)
    
    def test_api_connection(self) -> bool:
        """API bağlantısını test et"""
        try:
            # Basit bir arama yap
            result = self.search_places("Istanbul")
            return result is not None and 'results' in result
            
        except Exception as e:
            print(f"⚠️ API bağlantı testi hatası: {e}")
            return False
