#!/usr/bin/env python3
"""
🏗️ YOL AĞI OLUŞTURUCU 🏗️
OpenStreetMap ve gerçek itfaiye verilerinden yol ağı oluşturur

Özellikler:
1. Overpass API ile gerçek yol verilerini çeker
2. İtfaiye istasyonlarını nodelar olarak ekler
3. Yol tiplerini (motorway, primary, secondary vb.) tanımlar
4. Dinamik ağırlıklandırma (hava durumu, trafik) uygular
5. Graph veri yapısını oluşturur
"""

import json
import requests
import time
from typing import Dict, List, Tuple, Optional
from advanced_pathfinding import RoadNetwork, RoadType
from fire_stations import load_fire_stations
import math

class NetworkBuilder:
    """Yol ağı oluşturucu - Gerçek verilerle"""
    
    def __init__(self):
        self.network = RoadNetwork()
        self.node_map = {}  # (lat, lon) -> node_id mapping
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        
    def build_from_fire_stations(self, fire_stations: Optional[Dict[str, Tuple[float, float]]] = None) -> RoadNetwork:
        """
        İtfaiye istasyonlarından network oluştur
        
        Strateji:
        1. Her itfaiye istasyonunu bir node olarak ekle
        2. En yakın komşularla bağlantı kur
        3. Mesafe ve yol tipine göre ağırlıklandır
        """
        if fire_stations is None:
            fire_stations = load_fire_stations()
        
        print(f"🏗️  Network oluşturuluyor: {len(fire_stations)} itfaiye istasyonu")
        
        # İtfaiye istasyonlarını nodelar olarak ekle
        station_ids = {}
        for name, (lat, lon) in fire_stations.items():
            node_id = self.network.add_node(lat, lon, name, is_fire_station=True)
            station_ids[name] = node_id
            self.node_map[(lat, lon)] = node_id
        
        print(f"✅ {len(station_ids)} itfaiye istasyonu eklendi")
        
        # Her istasyonu en yakın N komşusuna bağla
        print("🔗 Bağlantılar oluşturuluyor...")
        n_neighbors = min(5, len(fire_stations) - 1)  # Her node en fazla 5 komşuya bağlı
        
        edge_count = 0
        for name1, (lat1, lon1) in fire_stations.items():
            node1_id = station_ids[name1]
            
            # En yakın komşuları bul
            neighbors = self._find_k_nearest_neighbors(
                (lat1, lon1), fire_stations, n_neighbors, exclude=[name1]
            )
            
            for neighbor_name, distance in neighbors:
                node2_id = station_ids[neighbor_name]
                
                # Yol tipini mesafeye göre belirle (heuristic)
                road_type = self._estimate_road_type(distance)
                
                try:
                    self.network.add_edge(node1_id, node2_id, road_type, bidirectional=True)
                    edge_count += 1
                except ValueError:
                    continue
        
        print(f"✅ {edge_count} bağlantı oluşturuldu")
        print(f"📊 Network hazır: {self.network.node_count()} node, {self.network.edge_count()} edge")
        
        return self.network
    
    def build_from_osm_data(self, bbox: Tuple[float, float, float, float], 
                           fire_stations: Optional[Dict[str, Tuple[float, float]]] = None) -> RoadNetwork:
        """
        OpenStreetMap'ten gerçek yol verilerini çekerek network oluştur
        
        Args:
            bbox: (min_lat, min_lon, max_lat, max_lon) - Bounding box
            fire_stations: İtfaiye istasyonları dictionary
        
        Returns:
            RoadNetwork with real OSM data
        """
        if fire_stations is None:
            fire_stations = load_fire_stations()
        
        print(f"🗺️  OpenStreetMap'ten veri çekiliyor...")
        print(f"   Bbox: {bbox}")
        
        # Overpass QL sorgusu - Yolları çek
        overpass_query = f"""
        [out:json][timeout:60];
        (
          way["highway"]["highway"!~"footway|path|cycleway"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out body;
        >;
        out skel qt;
        """
        
        try:
            response = requests.post(
                self.overpass_url,
                data={'data': overpass_query},
                timeout=120
            )
            
            if response.status_code != 200:
                print(f"❌ Overpass API hatası: {response.status_code}")
                print("🔄 Fallback: İtfaiye istasyonlarından network oluşturuluyor...")
                return self.build_from_fire_stations(fire_stations)
            
            osm_data = response.json()
            print(f"✅ OSM verisi alındı: {len(osm_data.get('elements', []))} element")
            
            # OSM verilerini işle
            return self._process_osm_data(osm_data, fire_stations)
            
        except Exception as e:
            print(f"❌ OSM veri çekme hatası: {e}")
            print("🔄 Fallback: İtfaiye istasyonlarından network oluşturuluyor...")
            return self.build_from_fire_stations(fire_stations)
    
    def _process_osm_data(self, osm_data: Dict, fire_stations: Dict[str, Tuple[float, float]]) -> RoadNetwork:
        """OSM verilerini işleyerek network oluştur"""
        elements = osm_data.get('elements', [])
        
        # Önce nodeları map'e al
        osm_nodes = {}
        for elem in elements:
            if elem['type'] == 'node':
                osm_nodes[elem['id']] = (elem['lat'], elem['lon'])
        
        print(f"📍 {len(osm_nodes)} OSM node bulundu")
        
        # İtfaiye istasyonlarını ekle
        station_ids = {}
        for name, (lat, lon) in fire_stations.items():
            node_id = self.network.add_node(lat, lon, name, is_fire_station=True)
            station_ids[name] = node_id
            self.node_map[(lat, lon)] = node_id
        
        print(f"✅ {len(station_ids)} itfaiye istasyonu eklendi")
        
        # Wayları işle (yollar)
        way_count = 0
        edge_count = 0
        
        for elem in elements:
            if elem['type'] == 'way' and 'nodes' in elem:
                tags = elem.get('tags', {})
                highway_type = tags.get('highway', '')
                
                # Yol tipini belirle
                road_type = self._osm_to_road_type(highway_type)
                if road_type is None:
                    continue
                
                way_count += 1
                way_nodes = elem['nodes']
                
                # Way'deki ardışık nodeları edge olarak ekle
                for i in range(len(way_nodes) - 1):
                    node1_osm_id = way_nodes[i]
                    node2_osm_id = way_nodes[i + 1]
                    
                    if node1_osm_id not in osm_nodes or node2_osm_id not in osm_nodes:
                        continue
                    
                    lat1, lon1 = osm_nodes[node1_osm_id]
                    lat2, lon2 = osm_nodes[node2_osm_id]
                    
                    # Networkümüze node ekle (eğer yoksa)
                    if (lat1, lon1) not in self.node_map:
                        node1_id = self.network.add_node(lat1, lon1)
                        self.node_map[(lat1, lon1)] = node1_id
                    else:
                        node1_id = self.node_map[(lat1, lon1)]
                    
                    if (lat2, lon2) not in self.node_map:
                        node2_id = self.network.add_node(lat2, lon2)
                        self.node_map[(lat2, lon2)] = node2_id
                    else:
                        node2_id = self.node_map[(lat2, lon2)]
                    
                    # Edge ekle
                    try:
                        oneway = tags.get('oneway', 'no') == 'yes'
                        self.network.add_edge(node1_id, node2_id, road_type, bidirectional=not oneway)
                        edge_count += 1
                    except ValueError:
                        continue
        
        print(f"✅ {way_count} yol işlendi, {edge_count} edge oluşturuldu")
        print(f"📊 Network hazır: {self.network.node_count()} node, {self.network.edge_count()} edge")
        
        return self.network
    
    def _find_k_nearest_neighbors(self, point: Tuple[float, float], 
                                  all_points: Dict[str, Tuple[float, float]], 
                                  k: int, exclude: List[str] = None) -> List[Tuple[str, float]]:
        """K en yakın komşuyu bul"""
        if exclude is None:
            exclude = []
        
        distances = []
        lat1, lon1 = point
        
        for name, (lat2, lon2) in all_points.items():
            if name in exclude:
                continue
            
            dist = self._haversine_distance(lat1, lon1, lat2, lon2)
            distances.append((name, dist))
        
        # Mesafeye göre sırala ve ilk k'yı al
        distances.sort(key=lambda x: x[1])
        return distances[:k]
    
    def _estimate_road_type(self, distance_km: float) -> RoadType:
        """
        Mesafeye göre yol tipini tahmin et (heuristic)
        
        Mantık:
        - Kısa mesafe (<5 km): Muhtemelen şehir içi -> Secondary/Tertiary
        - Orta mesafe (5-20 km): Primary
        - Uzun mesafe (>20 km): Motorway/Trunk
        """
        if distance_km < 5:
            return RoadType.SECONDARY  # Tali yol - şehir içi
        elif distance_km < 20:
            return RoadType.PRIMARY
        else:
            return RoadType.TRUNK
    
    def _osm_to_road_type(self, highway_tag: str) -> Optional[RoadType]:
        """OSM highway tag'ini RoadType'a çevir"""
        mapping = {
            'motorway': RoadType.MOTORWAY,
            'motorway_link': RoadType.MOTORWAY,
            'trunk': RoadType.TRUNK,
            'trunk_link': RoadType.TRUNK,
            'primary': RoadType.PRIMARY,
            'primary_link': RoadType.PRIMARY,
            'secondary': RoadType.SECONDARY,
            'secondary_link': RoadType.SECONDARY,
            'tertiary': RoadType.TERTIARY,
            'tertiary_link': RoadType.TERTIARY,
            'residential': RoadType.RESIDENTIAL,
            'unclassified': RoadType.UNCLASSIFIED,
            'service': RoadType.RESIDENTIAL,
            'living_street': RoadType.RESIDENTIAL
        }
        
        return mapping.get(highway_tag.lower())
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine ile mesafe hesapla"""
        R = 6371  # km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def add_intermediate_nodes(self, density: int = 10) -> None:
        """
        Network'e ara nodelar ekle (daha gerçekçi network)
        
        Args:
            density: Her edge için kaç ara node ekleneceği
        """
        print(f"🔧 Ara nodelar ekleniyor (density={density})...")
        
        # Mevcut edge'leri kopyala
        original_edges = []
        for from_id, edges in list(self.network.edges.items()):
            for edge in edges:
                original_edges.append((from_id, edge))
        
        new_nodes_count = 0
        
        for from_id, edge in original_edges:
            to_id = edge.to_node
            
            from_node = self.network.nodes[from_id]
            to_node = self.network.nodes[to_id]
            
            # Edge'i sil
            self.network.edges[from_id] = [e for e in self.network.edges[from_id] if e.to_node != to_id]
            
            # Ara nodelar oluştur
            prev_id = from_id
            for i in range(1, density):
                # İnterpolasyon ile ara koordinatlar
                ratio = i / density
                inter_lat = from_node.lat + (to_node.lat - from_node.lat) * ratio
                inter_lon = from_node.lon + (to_node.lon - from_node.lon) * ratio
                
                # Ara node ekle
                inter_id = self.network.add_node(inter_lat, inter_lon)
                self.node_map[(inter_lat, inter_lon)] = inter_id
                
                # Edge'leri bağla
                self.network.add_edge(prev_id, inter_id, edge.road_type, bidirectional=True)
                
                prev_id = inter_id
                new_nodes_count += 1
            
            # Son edge'i ekle
            self.network.add_edge(prev_id, to_id, edge.road_type, bidirectional=True)
        
        print(f"✅ {new_nodes_count} ara node eklendi")
        print(f"📊 Yeni network: {self.network.node_count()} node, {self.network.edge_count()} edge")


def build_izmir_manisa_network(use_osm: bool = False) -> RoadNetwork:
    """
    İzmir-Manisa bölgesi için network oluştur
    
    Args:
        use_osm: True ise OpenStreetMap'ten gerçek veri çeker (yavaş ama gerçekçi)
                 False ise itfaiye istasyonlarından basit network oluşturur (hızlı)
    """
    builder = NetworkBuilder()
    
    if use_osm:
        # İzmir-Manisa bounding box
        # min_lat, min_lon, max_lat, max_lon
        bbox = (38.0, 26.3, 39.1, 28.5)
        
        print("🗺️  OSM modunda network oluşturuluyor (bu uzun sürebilir)...")
        network = builder.build_from_osm_data(bbox)
    else:
        print("⚡ Hızlı modda network oluşturuluyor...")
        network = builder.build_from_fire_stations()
    
    return network


# Test fonksiyonu
if __name__ == "__main__":
    print("🏗️  Network Builder Test Ediliyor...\n")
    
    # Hızlı mod ile test
    print("=" * 60)
    print("TEST 1: Hızlı Mod (İtfaiye İstasyonlarından)")
    print("=" * 60)
    network = build_izmir_manisa_network(use_osm=False)
    
    print(f"\n📊 Network İstatistikleri:")
    print(f"   Node sayısı: {network.node_count()}")
    print(f"   Edge sayısı: {network.edge_count()}")
    print(f"   İtfaiye sayısı: {len(network.fire_stations)}")
    
    # İlk birkaç itfaiye arasında test
    if len(network.fire_stations) >= 2:
        start_id = network.fire_stations[0]
        end_id = network.fire_stations[1]
        
        start_name = network.nodes[start_id].name
        end_name = network.nodes[end_id].name
        
        print(f"\n🧪 Test Rotası: {start_name} -> {end_name}")
        
        from advanced_pathfinding import DijkstraPathfinder, AStarPathfinder
        
        dijkstra = DijkstraPathfinder(network)
        result = dijkstra.find_shortest_path(start_id, end_id)
        
        if result:
            print(f"   📏 Mesafe: {result['distance']:.2f} km")
            print(f"   ⏱️  Süre: {result['estimated_time']:.1f} dakika")
            print(f"   🔍 İncelenen node: {result['stats']['nodes_explored']}")
            print(f"   ⚡ Hesaplama süresi: {result['stats']['execution_time']:.4f} saniye")
        else:
            print("   ❌ Rota bulunamadı")
    
    print("\n✅ Test tamamlandı!")

