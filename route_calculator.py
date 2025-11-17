#!/usr/bin/env python3
"""
🚒 ACİL DURUM ROTA HESAPLAYICI 🚒
Akıllı rota optimizasyonu ile entegre edilmiş
"""

import requests
import json
import math
from typing import Dict, Tuple, List, Optional
from fire_stations import load_fire_stations
from fire_station_finder import FireStationFinder
from smart_route_optimizer import SmartRouteOptimizer
import config
import polyline  # OSRM encoded polyline decode için

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """İki nokta arasındaki mesafeyi hesapla (km)"""
    R = 6371  # Dünya'nın yarıçapı (km)
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

async def find_nearest_fire_station(fire_location: Tuple[float, float], 
                                   fire_stations: Dict[str, Tuple[float, float]] = None,
                                   tomtom_api = None) -> Tuple[str, Tuple[float, float], float]:
    """En yakın itfaiye istasyonunu bul - Otomatik veya manuel"""
    
    # Otomatik itfaiye bulma sistemi varsa kullan
    if tomtom_api:
        try:
            print("🔍 Otomatik itfaiye arama sistemi kullanılıyor...")
            finder = FireStationFinder(tomtom_api)
            nearest_station_info = await finder.get_nearest_fire_station(fire_location)
            
            if nearest_station_info:
                station_name = nearest_station_info['name']
                station_coords = nearest_station_info['coords']
                distance = nearest_station_info['distance']
                
                print(f"✅ Otomatik bulunan itfaiye: {station_name}")
                print(f"   📍 Konum: {station_coords}")
                print(f"   📏 Mesafe: {distance:.1f} km")
                print(f"   🏠 Adres: {nearest_station_info.get('address', 'N/A')}")
                
                return station_name, station_coords, distance
            else:
                print("⚠️ Otomatik arama başarısız, manuel arama kullanılıyor...")
                
        except Exception as e:
            print(f"⚠️ Otomatik itfaiye arama hatası: {e}")
            print("🔄 Manuel arama kullanılıyor...")
    
    # Manuel arama (fallback)
    if fire_stations is None:
        fire_stations = load_fire_stations()
    
    fire_lat, fire_lon = fire_location
    nearest_station = None
    nearest_coords = None
    min_distance = float('inf')
    
    for name, coords in fire_stations.items():
        distance = haversine_distance(fire_location[0], fire_location[1], coords[0], coords[1])
        if distance < min_distance:
            min_distance = distance
            nearest_station = name
            nearest_coords = coords
    
    if nearest_station is None:
        raise ValueError("Hiç itfaiye istasyonu bulunamadı!")
    
    print(f"✅ Manuel bulunan itfaiye: {nearest_station}")
    print(f"   📍 Konum: {nearest_coords}")
    print(f"   📏 Mesafe: {min_distance:.1f} km")
    
    return nearest_station, nearest_coords, min_distance

def determine_terrain_type(lat: float, lon: float) -> str:
    """Arazi türünü belirle (basit heuristik)"""
    # İzmir ve Manisa bölgesi için arazi tespiti
    # İzmir: ~38.0-39.1 lat, ~26.3-28.2 lon
    # Manisa: ~38.5-38.6 lat, ~27.4-28.2 lon
    
    if 38.0 <= lat <= 39.1 and 26.3 <= lon <= 28.5:
        # İzmir-Manisa bölgesi
        if lon < 27.0:  # Batı İzmir (Çeşme, Urla) - Kıyı
            return "urban"
        elif lat < 38.3:  # Güney İzmir (Menderes, Torbalı) - Kırsal
            return "rural"
        elif lat > 38.7 or lon > 28.0:  # Manisa ve kuzey İzmir - Dağlık/Ormanlık
            return "mountain_forest"
        else:  # Merkez bölgeler
            return "urban"
    else:
        # Diğer bölgeler için genel sınıflandırma
        return "rural"

def get_osrm_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float, 
                   terrain_type: str = "rural") -> Optional[Dict]:
    """OSRM'den rota al"""
    try:
        # Terrain tipine göre profil seç
        if terrain_type in ["mountain", "forest"]:
            profile = "foot"  # Dağ/orman için yaya profili
        elif terrain_type == "rural":
            profile = "cycling"  # Kırsal için bisiklet profili
        else:
            profile = "driving"  # Şehir için araç profili
        
        url = f"http://router.project-osrm.org/route/v1/{profile}/{start_lon},{start_lat};{end_lon},{end_lat}"
        params = {
            'overview': 'full',
            'steps': 'true',
            'annotations': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ OSRM hatası: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"⚠️ OSRM bağlantı hatası: {e}")
        return None

def extract_road_types_from_steps(steps: List[Dict]) -> List[str]:
    """OSRM adımlarından yol tiplerini çıkar"""
    road_types = []
    
    for step in steps:
        if 'maneuver' in step and 'instruction' in step['maneuver']:
            instruction = step['maneuver']['instruction']
            
            # Yol tipini belirle
            if 'motorway' in instruction.lower():
                road_types.append('motorway')
            elif 'trunk' in instruction.lower():
                road_types.append('trunk')
            elif 'primary' in instruction.lower():
                road_types.append('primary')
            elif 'secondary' in instruction.lower():
                road_types.append('secondary')
            elif 'tertiary' in instruction.lower():
                road_types.append('tertiary')
            elif 'residential' in instruction.lower():
                road_types.append('residential')
            else:
                road_types.append('unclassified')
    
    return road_types

def classify_route_by_road_types(road_types: List[str]) -> str:
    """Yol tiplerine göre rotayı sınıflandır"""
    if not road_types:
        return "Bilinmeyen"
    
    # Yol tipi sayılarını hesapla
    type_counts = {}
    for road_type in road_types:
        type_counts[road_type] = type_counts.get(road_type, 0) + 1
    
    total_roads = len(road_types)
    
    # Ana yol ağırlıklı mı?
    main_road_count = type_counts.get('motorway', 0) + type_counts.get('trunk', 0) + type_counts.get('primary', 0)
    main_road_ratio = main_road_count / total_roads
    
    # Tali yol ağırlıklı mı?
    secondary_road_count = type_counts.get('secondary', 0) + type_counts.get('tertiary', 0) + type_counts.get('residential', 0)
    secondary_road_ratio = secondary_road_count / total_roads
    
    if main_road_ratio > 0.6:
        return "Ana Yol Ağırlıklı"
    elif secondary_road_ratio > 0.6:
        return "Tali Yol Ağırlıklı"
    else:
        return "Karma Yol"

async def analyze_emergency_route(fire_location: Tuple[float, float], fire_stations: Dict[str, Tuple[float, float]] = None, tomtom_api = None) -> Dict:
    """Acil durum rotasını analiz et - Akıllı optimizasyon ile"""
    try:
        print(f"🔥 Yangın noktası analiz ediliyor: {fire_location[0]}, {fire_location[1]}")
        
        # Arazi türünü belirle
        terrain_type = determine_terrain_type(fire_location[0], fire_location[1])
        print(f"🗺️ Arazi türü: {terrain_type}")
        
        if terrain_type in ["mountain", "forest"]:
            print("🌾 Kırsal yangın tespit edildi - Tali yollar tercih ediliyor!")
        elif terrain_type == "rural":
            print("🌾 Kırsal yangın tespit edildi - Tali yollar tercih ediliyor!")
        else:
            print("🏙️ Şehir yangını tespit edildi - Ana yollar tercih ediliyor!")
        
        # İtfaiye istasyonlarını yükle (parametre yoksa varsayılan)
        if fire_stations is None:
            fire_stations = load_fire_stations()
        
        # En yakın itfaiye istasyonunu bul
        nearest_station, nearest_coords, distance = await find_nearest_fire_station(fire_location, fire_stations, tomtom_api)
        print(f"🚒 En yakın itfaiye: {nearest_station}")
        print(f"📍 Mesafe: {distance:.1f} km")
        
        # OSRM rota al
        print("🔍 OSRM ile rota aranıyor...")
        print(f"   📍 Başlangıç: {nearest_coords[0]:.6f}, {nearest_coords[1]:.6f}")
        print(f"   📍 Hedef: {fire_location[0]:.6f}, {fire_location[1]:.6f}")
        
        # Farklı profilleri dene
        profiles = ["foot", "cycling", "driving"]
        best_route = None
        
        for profile in profiles:
            print(f"  📍 {profile.title()} - {profile.title()} profili deneniyor...")
            
            # OSRM endpoint'ini güncelle
            url = f"http://router.project-osrm.org/route/v1/{profile}/{nearest_coords[1]},{nearest_coords[0]};{fire_location[1]},{fire_location[0]}"
            params = {'overview': 'full', 'steps': 'true', 'annotations': 'true'}
            
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    route_data = response.json()
                    
                    # Debug: API yanıtını kontrol et
                    print(f"    🔍 API yanıtı: {type(route_data)}")
                    if isinstance(route_data, dict):
                        print(f"    📊 Ana anahtarlar: {list(route_data.keys())}")
                        if 'routes' in route_data:
                            print(f"    🛣️ Routes sayısı: {len(route_data['routes'])}")
                    
                    if 'routes' in route_data and route_data['routes']:
                        route = route_data['routes'][0]
                        
                        # Route yapısını kontrol et
                        print(f"    📋 Route anahtarları: {list(route.keys())}")
                        
                        # Geometri kontrolü
                        if 'geometry' in route:
                            geometry = route['geometry']
                            print(f"    🗺️ Geometry tipi: {type(geometry)}")
                            
                            if isinstance(geometry, str):
                                # OSRM encoded polyline string'i decode et
                                try:
                                    decoded_coords = polyline.decode(geometry)
                                    print(f"    ✅ Encoded polyline decode edildi: {len(decoded_coords)} nokta")
                                    
                                    # Koordinatları [lat, lon] formatına çevir
                                    coordinates = [[lat, lon] for lat, lon in decoded_coords]
                                    
                                    # Route'a geometry bilgisini ekle
                                    route['decoded_geometry'] = {'coordinates': coordinates}
                                    
                                    if not best_route or route.get('distance', 0) < best_route.get('distance', float('inf')):
                                        best_route = route
                                        best_profile = profile
                                        
                                except Exception as decode_error:
                                    print(f"    ❌ Polyline decode hatası: {decode_error}")
                                    
                            elif isinstance(geometry, dict) and 'coordinates' in geometry:
                                coords = geometry['coordinates']
                                print(f"    ✅ Geometri bulundu: {len(coords)} nokta")
                                
                                if not best_route or route.get('distance', 0) < best_route.get('distance', float('inf')):
                                    best_route = route
                                    best_profile = profile
                            else:
                                print(f"    ❌ Geometri koordinatları bulunamadı")
                        else:
                            print(f"    ❌ Geometri bulunamadı")
                    else:
                        print(f"    ❌ Rota bulunamadı")
                        
            except Exception as e:
                print(f"    ❌ {profile} profili hatası: {e}")
                import traceback
                print(f"    📋 Hata detayı: {traceback.format_exc()}")
                continue
        
        if not best_route:
            print("❌ Hiçbir profilde rota bulunamadı!")
            return {
                'error': 'OSRM rota bulunamadı',
                'fire_location': fire_location,
                'nearest_station': nearest_station,
                'distance': distance
            }
        
        print(f"✅ En iyi rota: {best_profile} profili")
        
        # Yol tiplerini çıkar
        road_types = []
        if 'legs' in best_route and best_route['legs']:
            for leg in best_route['legs']:
                if 'steps' in leg:
                    road_types.extend(extract_road_types_from_steps(leg['steps']))
        
        # Rotayı sınıflandır
        route_classification = classify_route_by_road_types(road_types)
        
        # Tali yol oranını hesapla
        secondary_ratio = 0.0
        if road_types:
            secondary_count = sum(1 for rt in road_types if rt in ['secondary', 'tertiary', 'residential'])
            secondary_ratio = secondary_count / len(road_types)
        
        # Temel rota bilgileri
        base_route_info = {
            'distance': best_route['distance'] / 1000,  # m'den km'ye
            'duration': best_route['duration'] / 60,    # saniyeden dakikaya
            'route_type': route_classification,
            'profile_used': best_profile,
            'road_types': road_types,
            'secondary_ratio': secondary_ratio
        }
        
        # 🚀 AKILLI ROTA OPTİMİZASYONU
        print("🧠 Akıllı rota optimizasyonu yapılıyor...")
        
        # Optimizer'ı başlat
        config_dict = {
            'OPENWEATHER_API_KEY': config.OPENWEATHER_API_KEY,
            'TOMTOM_TRAFFIC_API_KEY': config.TOMTOM_TRAFFIC_API_KEY,
            'WEATHER_MULTIPLIERS': config.WEATHER_MULTIPLIERS,
            'TRAFFIC_MULTIPLIERS': config.TRAFFIC_MULTIPLIERS,
            'ROAD_CONDITION_MULTIPLIERS': config.ROAD_CONDITION_MULTIPLIERS
        }
        
        optimizer = SmartRouteOptimizer(config_dict)
        
        # Rota koordinatlarını hazırla
        route_coordinates = []
        if 'decoded_geometry' in best_route and 'coordinates' in best_route['decoded_geometry']:
            for coord in best_route['decoded_geometry']['coordinates']:
                route_coordinates.append((coord[0], coord[1]))  # lat, lon
        elif 'geometry' in best_route and 'coordinates' in best_route['geometry']:
            for coord in best_route['geometry']['coordinates']:
                route_coordinates.append((coord[1], coord[0]))  # lon, lat -> lat, lon
        
        # Optimizasyon yap
        optimization_result = await optimizer.optimize_route(route_coordinates, base_route_info)
        
        # Sonuçları birleştir
        final_result = {
            'fire_location': fire_location,
            'nearest_station': nearest_station,
            'nearest_station_coords': nearest_coords,
            'base_route': base_route_info,
            'smart_optimization': optimization_result,
            'terrain_type': terrain_type,
            'recommendations': optimization_result.get('recommendations', [])
        }
        
        print("✅ Akıllı rota analizi tamamlandı!")
        return final_result
        
    except Exception as e:
        print(f"❌ Rota analizi hatası: {e}")
        return {
            'error': str(e),
            'fire_location': fire_location
        }
