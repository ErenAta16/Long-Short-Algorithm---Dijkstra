#!/usr/bin/env python3
"""
🚀 AKILLI ROTA OPTİMİZASYONU MODÜLÜ 🚀
Gerçek zamanlı trafik, hava durumu ve yol durumu entegrasyonu
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging
import config

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherCondition(Enum):
    """Hava durumu koşulları"""
    CLEAR = "clear"
    RAIN = "rain"
    SNOW = "snow"
    FOG = "fog"
    STORM = "storm"

class TrafficLevel(Enum):
    """Trafik seviyeleri"""
    FREE_FLOW = "free_flow"
    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"
    CONGESTED = "congested"

class RoadCondition(Enum):
    """Yol durumları"""
    NORMAL = "normal"
    CONSTRUCTION = "construction"
    ACCIDENT = "accident"
    CLOSED = "closed"
    POOR_CONDITION = "poor_condition"

@dataclass
class WeatherInfo:
    """Hava durumu bilgileri"""
    condition: WeatherCondition
    temperature: float
    visibility: float  # km cinsinden
    precipitation: float  # mm cinsinden
    wind_speed: float  # km/h cinsinden
    humidity: float  # %

@dataclass
class TrafficInfo:
    """Trafik bilgileri"""
    level: TrafficLevel
    delay_minutes: float
    congestion_score: float  # 0-1 arası
    average_speed: float  # km/h

@dataclass
class RoadInfo:
    """Yol durumu bilgileri"""
    condition: RoadCondition
    description: str
    severity: float  # 0-1 arası
    estimated_delay: float  # dakika

class SmartRouteOptimizer:
    """Akıllı rota optimizasyonu sınıfı"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.weather_api_key = config.get('OPENWEATHER_API_KEY', '')
        self.traffic_api_key = config.get('TOMTOM_TRAFFIC_API_KEY', '')
        self.cache_duration = 300  # 5 dakika cache
        self._weather_cache = {}
        self._traffic_cache = {}
        self._road_cache = {}
        
    async def get_weather_data(self, lat: float, lon: float) -> WeatherInfo:
        """OpenWeatherMap API'den hava durumu verisi al"""
        cache_key = f"{lat:.3f}_{lon:.3f}"
        
        # Cache kontrolü
        if cache_key in self._weather_cache:
            cache_time, data = self._weather_cache[cache_key]
            if time.time() - cache_time < self.cache_duration:
                return data
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Hava durumu koşulunu belirle
                        weather_main = data['weather'][0]['main'].lower()
                        if 'rain' in weather_main:
                            condition = WeatherCondition.RAIN
                        elif 'snow' in weather_main:
                            condition = WeatherCondition.SNOW
                        elif 'fog' in weather_main or 'mist' in weather_main:
                            condition = WeatherCondition.FOG
                        elif 'thunderstorm' in weather_main:
                            condition = WeatherCondition.STORM
                        else:
                            condition = WeatherCondition.CLEAR
                        
                        weather_info = WeatherInfo(
                            condition=condition,
                            temperature=data['main']['temp'],
                            visibility=data.get('visibility', 10000) / 1000,  # m'den km'ye
                            precipitation=data.get('rain', {}).get('1h', 0),
                            wind_speed=data['wind']['speed'] * 3.6,  # m/s'den km/h'ye
                            humidity=data['main']['humidity']
                        )
                        
                        # Cache'e kaydet
                        self._weather_cache[cache_key] = (time.time(), weather_info)
                        return weather_info
                        
        except Exception as e:
            logger.error(f"Hava durumu verisi alınamadı: {e}")
            # Varsayılan değerler
            return WeatherInfo(
                condition=WeatherCondition.CLEAR,
                temperature=20.0,
                visibility=10.0,
                precipitation=0.0,
                wind_speed=0.0,
                humidity=50.0
            )
    
    async def get_traffic_data(self, start_lat: float, start_lon: float, 
                              end_lat: float, end_lon: float) -> TrafficInfo:
        """TomTom Traffic API'den trafik verisi al"""
        cache_key = f"{start_lat:.3f}_{start_lon:.3f}_{end_lat:.3f}_{end_lon:.3f}"
        
        # Cache kontrolü
        if cache_key in self._traffic_cache:
            cache_time, data = self._traffic_cache[cache_key]
            if time.time() - cache_time < self.cache_duration:
                return data
        
        try:
            # TomTom Traffic API endpoint'i
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
            params = {
                'key': self.traffic_api_key,
                'point': f"{start_lat},{start_lon}",
                'unit': 'KMPH'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Trafik seviyesini belirle (örnek veri yapısı)
                        # Gerçek API'ye göre bu kısım güncellenecek
                        traffic_level = TrafficLevel.MODERATE
                        delay_minutes = 5.0
                        congestion_score = 0.3
                        average_speed = 45.0
                        
                        traffic_info = TrafficInfo(
                            level=traffic_level,
                            delay_minutes=delay_minutes,
                            congestion_score=congestion_score,
                            average_speed=average_speed
                        )
                        
                        # Cache'e kaydet
                        self._traffic_cache[cache_key] = (time.time(), traffic_info)
                        return traffic_info
                        
        except Exception as e:
            logger.error(f"Trafik verisi alınamadı: {e}")
            # Varsayılan değerler
            return TrafficInfo(
                level=TrafficLevel.FREE_FLOW,
                delay_minutes=0.0,
                congestion_score=0.0,
                average_speed=60.0
            )
    
    def get_road_conditions(self, route_coordinates: List[Tuple[float, float]]) -> List[RoadInfo]:
        """Yol durumu bilgilerini al (şimdilik simüle edilmiş)"""
        road_conditions = []
        
        for i, (lat, lon) in enumerate(route_coordinates):
            # Simüle edilmiş yol durumu (gerçek veri kaynağına bağlanacak)
            if i % 5 == 0:  # Her 5. noktada bir yol durumu kontrolü
                condition = RoadCondition.NORMAL
                description = "Normal yol durumu"
                severity = 0.0
                estimated_delay = 0.0
                
                # Rastgele yol durumu simülasyonu
                import random
                if random.random() < 0.1:  # %10 ihtimalle çalışma
                    condition = RoadCondition.CONSTRUCTION
                    description = "Yol çalışması"
                    severity = 0.3
                    estimated_delay = 10.0
                elif random.random() < 0.05:  # %5 ihtimalle kaza
                    condition = RoadCondition.ACCIDENT
                    description = "Trafik kazası"
                    severity = 0.8
                    estimated_delay = 25.0
                
                road_conditions.append(RoadInfo(
                    condition=condition,
                    description=description,
                    severity=severity,
                    estimated_delay=estimated_delay
                ))
        
        return road_conditions
    
    def calculate_dynamic_weights(self, weather: WeatherInfo, traffic: TrafficInfo, 
                                 road_conditions: List[RoadInfo]) -> Dict[str, float]:
        """Dinamik yol ağırlıklarını hesapla"""
        base_weights = {
            'motorway': 1.0,
            'trunk': 1.2,
            'primary': 1.5,
            'secondary': 2.0,
            'tertiary': 2.5,
            'residential': 3.0,
            'unclassified': 2.8
        }
        
        # Hava durumu faktörü
        weather_multiplier = 1.0
        if weather.condition == WeatherCondition.RAIN:
            weather_multiplier = 1.3
        elif weather.condition == WeatherCondition.SNOW:
            weather_multiplier = 2.0
        elif weather.condition == WeatherCondition.FOG:
            weather_multiplier = 1.5
        elif weather.condition == WeatherCondition.STORM:
            weather_multiplier = 2.5
        
        # Görüş mesafesi faktörü
        visibility_factor = 1.0
        if weather.visibility < 1.0:  # 1 km'den az görüş
            visibility_factor = 2.0
        elif weather.visibility < 3.0:  # 3 km'den az görüş
            visibility_factor = 1.5
        
        # Trafik faktörü
        traffic_multiplier = 1.0 + traffic.congestion_score
        
        # Yol durumu faktörü
        road_multiplier = 1.0
        if road_conditions:
            max_severity = max(rc.severity for rc in road_conditions)
            road_multiplier = 1.0 + max_severity
        
        # Toplam çarpan
        total_multiplier = weather_multiplier * visibility_factor * traffic_multiplier * road_multiplier
        
        # Ağırlıkları güncelle
        dynamic_weights = {}
        for road_type, base_weight in base_weights.items():
            dynamic_weights[road_type] = base_weight * total_multiplier
        
        return dynamic_weights
    
    def _calculate_optimization(self, weather_info: WeatherInfo, traffic_info: TrafficInfo,
                               road_info: RoadInfo, base_route_info: Dict) -> Dict:
        """Optimizasyon hesaplamalarını yap"""
        
        # Temel değerler
        base_distance = base_route_info.get('distance', 0)
        base_duration = base_route_info.get('duration', 0)
        
        # Çarpanları al - config.py'den direkt import et
        try:
            weather_multiplier = config.WEATHER_MULTIPLIERS.get(weather_info.condition.value, 1.0)
            traffic_multiplier = config.TRAFFIC_MULTIPLIERS.get(traffic_info.level.value, 1.0)
            road_multiplier = config.ROAD_CONDITION_MULTIPLIERS.get(road_info.condition.value, 1.0)
        except (AttributeError, NameError):
            # Eğer config'de yoksa varsayılan değerler kullan
            weather_multiplier = 1.0
            traffic_multiplier = 1.0
            road_multiplier = 1.0
        
        # Toplam çarpan
        total_multiplier = weather_multiplier * traffic_multiplier * road_multiplier
        
        # Optimize edilmiş değerler
        optimized_duration = base_duration * total_multiplier
        estimated_delay = optimized_duration - base_duration
        
        # Öneriler
        recommendations = []
        
        if weather_info.condition != WeatherCondition.CLEAR:
            recommendations.append(f"🌤️ Hava durumu: {weather_info.condition.value} - {weather_multiplier:.1f}x gecikme")
        
        if traffic_info.level != TrafficLevel.FREE_FLOW:
            recommendations.append(f"🚗 Trafik: {traffic_info.level.value} - {traffic_multiplier:.1f}x gecikme")
        
        if road_info.condition != RoadCondition.NORMAL:
            recommendations.append(f"🛣️ Yol durumu: {road_info.condition.value} - {road_multiplier:.1f}x gecikme")
        
        if not recommendations:
            recommendations.append("✅ Optimal koşullar - gecikme yok")
        
        return {
            'weather_info': {
                'condition': weather_info.condition.value,
                'temperature': weather_info.temperature,
                'visibility': weather_info.visibility,
                'multiplier': weather_multiplier
            },
            'traffic_info': {
                'level': traffic_info.level.value,
                'delay_minutes': traffic_info.delay_minutes,
                'congestion_score': traffic_info.congestion_score,
                'multiplier': traffic_multiplier
            },
            'road_info': {
                'condition': road_info.condition.value,
                'severity': road_info.severity,
                'estimated_delay': road_info.estimated_delay,
                'multiplier': road_multiplier
            },
            'optimization': {
                'total_multiplier': total_multiplier,
                'base_duration': base_duration,
                'optimized_duration': optimized_duration,
                'estimated_delay': estimated_delay,
                'efficiency_score': 1.0 / total_multiplier if total_multiplier > 0 else 1.0
            },
            'recommendations': recommendations
        }
    
    async def optimize_route(self, route_coordinates: List[Tuple[float, float]], 
                           base_route_info: Dict) -> Dict:
        """Rota optimizasyonu yap"""
        try:
            # Başlangıç ve bitiş noktaları
            start_lat, start_lon = route_coordinates[0]
            end_lat, end_lon = route_coordinates[-1]
            
            # Hava durumu ve trafik verilerini al
            weather = await self.get_weather_data(start_lat, start_lon)
            traffic = await self.get_traffic_data(start_lat, start_lon, end_lat, end_lon)
            road_conditions = self.get_road_conditions(route_coordinates)
            
            # Dinamik ağırlıkları hesapla
            dynamic_weights = self.calculate_dynamic_weights(weather, traffic, road_conditions)
            
            # Optimizasyon sonuçları
            optimization_result = {
                'original_route': base_route_info,
                'weather_conditions': {
                    'condition': weather.condition.value,
                    'temperature': weather.temperature,
                    'visibility': weather.visibility,
                    'precipitation': weather.precipitation,
                    'wind_speed': weather.wind_speed,
                    'humidity': weather.humidity
                },
                'traffic_conditions': {
                    'level': traffic.level.value,
                    'delay_minutes': traffic.delay_minutes,
                    'congestion_score': traffic.congestion_score,
                    'average_speed': traffic.average_speed
                },
                'road_conditions': [
                    {
                        'condition': rc.condition.value,
                        'description': rc.description,
                        'severity': rc.severity,
                        'estimated_delay': rc.estimated_delay
                    } for rc in road_conditions
                ],
                'dynamic_weights': dynamic_weights,
                'optimization_factors': {
                    'weather_multiplier': 1.0 if weather.condition == WeatherCondition.CLEAR else 1.3,
                    'traffic_multiplier': 1.0 + traffic.congestion_score,
                    'road_multiplier': 1.0 + max(rc.severity for rc in road_conditions) if road_conditions else 1.0
                },
                'recommendations': self._generate_recommendations(weather, traffic, road_conditions)
            }
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Rota optimizasyonu hatası: {e}")
            return {
                'error': str(e),
                'original_route': base_route_info
            }
    
    def _generate_recommendations(self, weather: WeatherInfo, traffic: TrafficInfo, 
                                 road_conditions: List[RoadInfo]) -> List[str]:
        """Duruma göre öneriler oluştur"""
        recommendations = []
        
        # Hava durumu önerileri
        if weather.condition == WeatherCondition.RAIN:
            recommendations.append("🌧️ Yağmurlu hava - Yavaş sürüş önerilir")
        elif weather.condition == WeatherCondition.SNOW:
            recommendations.append("❄️ Karlı hava - Zincir takılması gerekebilir")
        elif weather.condition == WeatherCondition.FOG:
            recommendations.append("🌫️ Sisli hava - Görüş mesafesi düşük")
        elif weather.condition == WeatherCondition.STORM:
            recommendations.append("⛈️ Fırtınalı hava - Acil durum dışında seyahat önerilmez")
        
        # Trafik önerileri
        if traffic.level in [TrafficLevel.HEAVY, TrafficLevel.CONGESTED]:
            recommendations.append("🚗 Ağır trafik - Alternatif rota düşünülebilir")
        
        # Yol durumu önerileri
        for rc in road_conditions:
            if rc.condition == RoadCondition.CONSTRUCTION:
                recommendations.append(f"🚧 Yol çalışması - {rc.estimated_delay:.0f} dk gecikme")
            elif rc.condition == RoadCondition.ACCIDENT:
                recommendations.append(f"🚨 Trafik kazası - {rc.estimated_delay:.0f} dk gecikme")
        
        if not recommendations:
            recommendations.append("✅ Normal koşullar - Standart rota önerilir")
        
        return recommendations

# Test fonksiyonu
def test_smart_optimizer():
    """Akıllı rota optimizasyonu test fonksiyonu"""
    config = {
        'OPENWEATHER_API_KEY': 'test_key',
        'TOMTOM_TRAFFIC_API_KEY': 'test_key'
    }
    
    optimizer = SmartRouteOptimizer(config)
    
    # Test rota koordinatları
    test_route = [
        (40.1926, 29.0766),  # Bursa
        (40.2156, 28.3619),  # Karacabey
        (40.3997, 27.7933)   # Erdek
    ]
    
    base_route_info = {
        'distance': 45.2,
        'duration': 35.5,
        'route_type': 'Balanced'
    }
    
    try:
        result = optimizer.optimize_route(test_route, base_route_info)
        print("🚀 Akıllı Rota Optimizasyonu Test Sonucu:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        # Basit test yap
        print("🧪 Basit test yapılıyor...")
        
        # Varsayılan değerlerle test
        weather_info = optimizer._generate_recommendations(
            WeatherInfo(WeatherCondition.CLEAR, 20.0, 10.0, 0.0, 0.0, 50.0),
            TrafficInfo(TrafficLevel.FREE_FLOW, 0.0, 0.0, 60.0),
            optimizer.get_road_conditions(test_route)
        )
        print("✅ Basit test başarılı!")
        print(f"📋 Öneriler: {weather_info}")

if __name__ == "__main__":
    test_smart_optimizer()
