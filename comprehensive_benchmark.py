#!/usr/bin/env python3
"""
🎯 KAPSAMLI BENCHMARK TEST SİSTEMİ 🎯
Koordinat doğrulama, algoritma performansı, sistem sağlığı testleri
"""

import json
import time
from typing import Dict, List, Tuple
from network_builder import build_izmir_manisa_network
from advanced_pathfinding import (
    RoadNetwork, DijkstraPathfinder, AStarPathfinder, 
    BidirectionalDijkstra
)
from fire_stations import load_fire_stations
import random

class ComprehensiveBenchmark:
    """Kapsamlı benchmark test sistemi"""
    
    def __init__(self):
        self.results = {
            'coordinate_validation': {},
            'algorithm_performance': {},
            'system_health': {},
            'network_analysis': {},
            'summary': {}
        }
    
    def run_all_tests(self) -> Dict:
        """Tüm testleri çalıştır"""
        print("🎯 KAPSAMLI BENCHMARK TEST SİSTEMİ BAŞLATILIYOR...")
        print("=" * 80)
        
        # 1. Koordinat Doğrulama
        print("\n1️⃣  KOORDİNAT DOĞRULAMA TESTLERİ")
        print("-" * 80)
        coord_results = self.test_coordinate_validation()
        
        # 2. Network Analizi
        print("\n2️⃣  NETWORK ANALİZİ")
        print("-" * 80)
        network_results = self.test_network_structure()
        
        # 3. Algoritma Performansı
        print("\n3️⃣  ALGORİTMA PERFORMANS TESTLERİ")
        print("-" * 80)
        algo_results = self.test_algorithm_performance()
        
        # 4. Sistem Sağlığı
        print("\n4️⃣  SİSTEM SAĞLIĞI TESTLERİ")
        print("-" * 80)
        health_results = self.test_system_health()
        
        # Özet
        summary = self.generate_summary(coord_results, network_results, algo_results, health_results)
        
        self.results = {
            'coordinate_validation': coord_results,
            'network_analysis': network_results,
            'algorithm_performance': algo_results,
            'system_health': health_results,
            'summary': summary
        }
        
        return self.results
    
    def test_coordinate_validation(self) -> Dict:
        """Koordinat doğrulama testleri"""
        print("🔍 İtfaiye istasyonu koordinatları doğrulanıyor...")
        
        fire_stations = load_fire_stations()
        results = {
            'total_stations': len(fire_stations),
            'valid_coordinates': 0,
            'invalid_coordinates': 0,
            'out_of_bounds': 0,
            'duplicates': 0,
            'issues': []
        }
        
        # İzmir-Manisa bölge sınırları (genişletilmiş)
        IZMIR_BBOX = {
            'min_lat': 37.7, 'max_lat': 39.2,  # Bergama için genişletildi
            'min_lon': 26.2, 'max_lon': 28.3   # Kiraz için genişletildi
        }
        
        MANISA_BBOX = {
            'min_lat': 38.2, 'max_lat': 39.3,  # Genişletildi
            'min_lon': 27.2, 'max_lon': 28.8   # Sarıgöl için genişletildi
        }
        
        seen_coords = set()
        
        for name, (lat, lon) in fire_stations.items():
            # 1. Koordinat aralığı kontrolü
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                results['invalid_coordinates'] += 1
                results['issues'].append({
                    'station': name,
                    'issue': 'Geçersiz koordinat aralığı',
                    'coords': (lat, lon)
                })
                print(f"   ❌ {name}: Geçersiz koordinat ({lat}, {lon})")
                continue
            
            # 2. Bölge kontrolü
            in_izmir = (IZMIR_BBOX['min_lat'] <= lat <= IZMIR_BBOX['max_lat'] and
                       IZMIR_BBOX['min_lon'] <= lon <= IZMIR_BBOX['max_lon'])
            in_manisa = (MANISA_BBOX['min_lat'] <= lat <= MANISA_BBOX['max_lat'] and
                        MANISA_BBOX['min_lon'] <= lon <= MANISA_BBOX['max_lon'])
            
            if not (in_izmir or in_manisa):
                results['out_of_bounds'] += 1
                results['issues'].append({
                    'station': name,
                    'issue': 'Bölge dışında',
                    'coords': (lat, lon)
                })
                print(f"   ⚠️  {name}: Bölge dışında ({lat}, {lon})")
                continue
            
            # 3. Duplicate kontrolü (100m tolerans)
            coord_key = (round(lat, 3), round(lon, 3))
            if coord_key in seen_coords:
                results['duplicates'] += 1
                results['issues'].append({
                    'station': name,
                    'issue': 'Duplicate koordinat',
                    'coords': (lat, lon)
                })
                print(f"   ⚠️  {name}: Duplicate koordinat")
            else:
                seen_coords.add(coord_key)
                results['valid_coordinates'] += 1
        
        # Sonuçlar
        print(f"\n📊 Koordinat Doğrulama Sonuçları:")
        print(f"   Toplam İstasyon: {results['total_stations']}")
        print(f"   ✅ Geçerli: {results['valid_coordinates']}")
        print(f"   ❌ Geçersiz: {results['invalid_coordinates']}")
        print(f"   ⚠️  Bölge Dışı: {results['out_of_bounds']}")
        print(f"   🔄 Duplicate: {results['duplicates']}")
        
        success_rate = (results['valid_coordinates'] / results['total_stations']) * 100
        print(f"   📈 Başarı Oranı: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("   🎉 MÜKEMMEL! Tüm koordinatlar geçerli!")
        elif success_rate >= 90:
            print("   ✅ İYİ! Çoğu koordinat geçerli.")
        else:
            print("   ⚠️  DİKKAT! Bazı koordinatlar düzeltilmeli!")
        
        return results
    
    def test_network_structure(self) -> Dict:
        """Network yapısı analizi"""
        print("🏗️  Network yapısı analiz ediliyor...")
        
        network = build_izmir_manisa_network()
        
        results = {
            'node_count': network.node_count(),
            'edge_count': network.edge_count(),
            'fire_station_count': len(network.fire_stations),
            'average_degree': 0,
            'isolated_nodes': 0,
            'connectivity': 'unknown'
        }
        
        # Ortalama derece hesapla
        total_degree = sum(len(edges) for edges in network.edges.values())
        if network.node_count() > 0:
            results['average_degree'] = total_degree / network.node_count()
        
        # İzole node kontrolü
        isolated = 0
        for node_id in network.nodes:
            if node_id not in network.edges or len(network.edges[node_id]) == 0:
                isolated += 1
        results['isolated_nodes'] = isolated
        
        # Bağlantılılık kontrolü
        if isolated == 0 and results['average_degree'] >= 2:
            results['connectivity'] = 'excellent'
        elif isolated == 0:
            results['connectivity'] = 'good'
        else:
            results['connectivity'] = 'poor'
        
        print(f"\n📊 Network Analizi:")
        print(f"   Node Sayısı: {results['node_count']}")
        print(f"   Edge Sayısı: {results['edge_count']}")
        print(f"   İtfaiye Sayısı: {results['fire_station_count']}")
        print(f"   Ortalama Derece: {results['average_degree']:.2f}")
        print(f"   İzole Node: {results['isolated_nodes']}")
        print(f"   Bağlantılılık: {results['connectivity']}")
        
        return results
    
    def test_algorithm_performance(self) -> Dict:
        """Algoritma performans testleri"""
        print("⚡ Algoritma performans testleri yapılıyor...")
        
        network = build_izmir_manisa_network()
        fire_stations = network.fire_stations
        
        if len(fire_stations) < 2:
            print("   ⚠️  Yeterli istasyon yok!")
            return {}
        
        # Test rotaları
        test_count = min(30, len(fire_stations) * (len(fire_stations) - 1) // 2)
        test_pairs = random.sample(
            [(fire_stations[i], fire_stations[j]) 
             for i in range(len(fire_stations)) 
             for j in range(i+1, len(fire_stations))],
            min(test_count, len(fire_stations) * (len(fire_stations) - 1) // 2)
        )
        
        results = {
            'dijkstra': {'times': [], 'nodes': [], 'distances': []},
            'astar': {'times': [], 'nodes': [], 'distances': []},
            'bidirectional': {'times': [], 'nodes': [], 'distances': []},
            'correctness': {'passed': 0, 'failed': 0}
        }
        
        print(f"   🔍 {len(test_pairs)} rota test ediliyor...")
        
        for start_id, end_id in test_pairs:
            # Dijkstra
            dijkstra = DijkstraPathfinder(network)
            start_time = time.time()
            result_d = dijkstra.find_shortest_path(start_id, end_id)
            dijkstra_time = time.time() - start_time
            
            if result_d:
                results['dijkstra']['times'].append(dijkstra_time * 1000)  # ms
                results['dijkstra']['nodes'].append(result_d['stats']['nodes_explored'])
                results['dijkstra']['distances'].append(result_d['distance'])
            
            # A*
            astar = AStarPathfinder(network)
            start_time = time.time()
            result_a = astar.find_shortest_path(start_id, end_id)
            astar_time = time.time() - start_time
            
            if result_a:
                results['astar']['times'].append(astar_time * 1000)  # ms
                results['astar']['nodes'].append(result_a['stats']['nodes_explored'])
                results['astar']['distances'].append(result_a['distance'])
            
            # Bidirectional
            bidirectional = BidirectionalDijkstra(network)
            start_time = time.time()
            result_b = bidirectional.find_shortest_path(start_id, end_id)
            bidirectional_time = time.time() - start_time
            
            if result_b:
                results['bidirectional']['times'].append(bidirectional_time * 1000)  # ms
                results['bidirectional']['nodes'].append(result_b['stats']['nodes_explored'])
                results['bidirectional']['distances'].append(result_b['distance'])
            
            # Doğruluk kontrolü
            if result_d and result_a and result_b:
                dist_d = result_d['distance']
                dist_a = result_a['distance']
                dist_b = result_b['distance']
                
                if abs(dist_d - dist_a) < 0.01 and abs(dist_d - dist_b) < 0.01:
                    results['correctness']['passed'] += 1
                else:
                    results['correctness']['failed'] += 1
        
        # İstatistikler
        stats = {}
        for algo in ['dijkstra', 'astar', 'bidirectional']:
            if results[algo]['times']:
                stats[algo] = {
                    'avg_time_ms': sum(results[algo]['times']) / len(results[algo]['times']),
                    'min_time_ms': min(results[algo]['times']),
                    'max_time_ms': max(results[algo]['times']),
                    'avg_nodes': sum(results[algo]['nodes']) / len(results[algo]['nodes']),
                    'avg_distance': sum(results[algo]['distances']) / len(results[algo]['distances'])
                }
        
        print(f"\n📊 Performans İstatistikleri:")
        print(f"{'Algoritma':<15} {'Ort. Süre (ms)':<15} {'Ort. Node':<12} {'Ort. Mesafe (km)'}")
        print("-" * 70)
        
        for algo, algo_stats in stats.items():
            print(f"{algo:<15} {algo_stats['avg_time_ms']:<15.4f} "
                  f"{algo_stats['avg_nodes']:<12.1f} {algo_stats['avg_distance']:.2f}")
        
        # Doğruluk
        total_correctness = results['correctness']['passed'] + results['correctness']['failed']
        if total_correctness > 0:
            correctness_rate = (results['correctness']['passed'] / total_correctness) * 100
            print(f"\n✅ Doğruluk: {results['correctness']['passed']}/{total_correctness} "
                  f"({correctness_rate:.1f}%)")
        
        return {'raw_data': results, 'statistics': stats}
    
    def test_system_health(self) -> Dict:
        """Sistem sağlığı testleri"""
        print("🏥 Sistem sağlığı kontrol ediliyor...")
        
        results = {
            'modules_loaded': True,
            'network_buildable': False,
            'algorithms_working': False,
            'data_accessible': False,
            'issues': []
        }
        
        # 1. Modül yükleme
        try:
            from fire_stations import load_fire_stations
            from network_builder import build_izmir_manisa_network
            from advanced_pathfinding import DijkstraPathfinder
            results['modules_loaded'] = True
            print("   ✅ Modüller yüklendi")
        except Exception as e:
            results['modules_loaded'] = False
            results['issues'].append(f"Modül yükleme hatası: {e}")
            print(f"   ❌ Modül yükleme hatası: {e}")
        
        # 2. Veri erişimi
        try:
            fire_stations = load_fire_stations()
            if len(fire_stations) > 0:
                results['data_accessible'] = True
                print(f"   ✅ Veri erişilebilir ({len(fire_stations)} istasyon)")
            else:
                results['issues'].append("Veri boş")
                print("   ⚠️  Veri boş")
        except Exception as e:
            results['issues'].append(f"Veri erişim hatası: {e}")
            print(f"   ❌ Veri erişim hatası: {e}")
        
        # 3. Network oluşturma
        try:
            network = build_izmir_manisa_network()
            if network.node_count() > 0:
                results['network_buildable'] = True
                print(f"   ✅ Network oluşturuldu ({network.node_count()} node)")
            else:
                results['issues'].append("Network boş")
                print("   ⚠️  Network boş")
        except Exception as e:
            results['issues'].append(f"Network oluşturma hatası: {e}")
            print(f"   ❌ Network oluşturma hatası: {e}")
        
        # 4. Algoritma çalışması
        try:
            network = build_izmir_manisa_network()
            if len(network.fire_stations) >= 2:
                dijkstra = DijkstraPathfinder(network)
                start_id = network.fire_stations[0]
                end_id = network.fire_stations[1]
                result = dijkstra.find_shortest_path(start_id, end_id)
                
                if result:
                    results['algorithms_working'] = True
                    print(f"   ✅ Algoritmalar çalışıyor (test rota: {result['distance']:.2f} km)")
                else:
                    results['issues'].append("Algoritma sonuç döndürmüyor")
                    print("   ⚠️  Algoritma sonuç döndürmüyor")
            else:
                results['issues'].append("Yeterli istasyon yok")
                print("   ⚠️  Yeterli istasyon yok")
        except Exception as e:
            results['issues'].append(f"Algoritma hatası: {e}")
            print(f"   ❌ Algoritma hatası: {e}")
        
        # Genel sağlık skoru
        health_score = sum([
            results['modules_loaded'],
            results['data_accessible'],
            results['network_buildable'],
            results['algorithms_working']
        ]) * 25
        
        results['health_score'] = health_score
        
        print(f"\n📊 Sistem Sağlığı Skoru: {health_score}%")
        
        if health_score == 100:
            print("   🎉 MÜKEMMEL! Sistem tamamen sağlıklı!")
        elif health_score >= 75:
            print("   ✅ İYİ! Sistem genel olarak sağlıklı.")
        elif health_score >= 50:
            print("   ⚠️  ORTA! Bazı sorunlar var.")
        else:
            print("   ❌ KRİTİK! Sistemde ciddi sorunlar var!")
        
        return results
    
    def generate_summary(self, coord_results, network_results, algo_results, health_results) -> Dict:
        """Genel özet oluştur"""
        summary = {
            'overall_status': 'UNKNOWN',
            'total_score': 0,
            'recommendations': []
        }
        
        # Skor hesapla
        scores = []
        
        # Koordinat skoru
        if coord_results.get('total_stations', 0) > 0:
            coord_score = (coord_results.get('valid_coordinates', 0) / 
                          coord_results.get('total_stations', 1)) * 100
            scores.append(coord_score)
        
        # Network skoru
        if network_results.get('connectivity') == 'excellent':
            network_score = 100
        elif network_results.get('connectivity') == 'good':
            network_score = 75
        else:
            network_score = 50
        scores.append(network_score)
        
        # Algoritma skoru
        if algo_results.get('statistics'):
            algo_score = 100  # Algoritmalar çalışıyor
        else:
            algo_score = 0
        scores.append(algo_score)
        
        # Sağlık skoru
        health_score = health_results.get('health_score', 0)
        scores.append(health_score)
        
        # Ortalama skor
        if scores:
            summary['total_score'] = sum(scores) / len(scores)
        
        # Genel durum
        if summary['total_score'] >= 90:
            summary['overall_status'] = 'EXCELLENT'
        elif summary['total_score'] >= 75:
            summary['overall_status'] = 'GOOD'
        elif summary['total_score'] >= 50:
            summary['overall_status'] = 'FAIR'
        else:
            summary['overall_status'] = 'POOR'
        
        # Öneriler
        if coord_results.get('invalid_coordinates', 0) > 0:
            summary['recommendations'].append(
                f"⚠️  {coord_results['invalid_coordinates']} geçersiz koordinat düzeltilmeli"
            )
        
        if coord_results.get('out_of_bounds', 0) > 0:
            summary['recommendations'].append(
                f"⚠️  {coord_results['out_of_bounds']} istasyon bölge dışında"
            )
        
        if network_results.get('isolated_nodes', 0) > 0:
            summary['recommendations'].append(
                f"⚠️  {network_results['isolated_nodes']} izole node var"
            )
        
        if health_score < 100:
            summary['recommendations'].append("🔧 Sistem sağlığı iyileştirilmeli")
        
        if not summary['recommendations']:
            summary['recommendations'].append("✅ Sistem mükemmel durumda!")
        
        return summary
    
    def save_report(self, filename: str = "comprehensive_benchmark_report.json"):
        """Raporu kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Rapor kaydedildi: {filename}")
    
    def print_final_summary(self):
        """Final özeti yazdır"""
        summary = self.results.get('summary', {})
        
        print("\n" + "=" * 80)
        print("📋 BENCHMARK ÖZET RAPORU")
        print("=" * 80)
        
        print(f"\n🎯 Genel Durum: {summary.get('overall_status', 'UNKNOWN')}")
        print(f"📊 Toplam Skor: {summary.get('total_score', 0):.1f}%")
        
        print(f"\n💡 Öneriler:")
        for rec in summary.get('recommendations', []):
            print(f"   {rec}")
        
        print("\n" + "=" * 80)


def main():
    """Ana fonksiyon"""
    benchmark = ComprehensiveBenchmark()
    
    # Tüm testleri çalıştır
    results = benchmark.run_all_tests()
    
    # Final özet
    benchmark.print_final_summary()
    
    # Raporu kaydet
    benchmark.save_report()
    
    print("\n✅ BENCHMARK TESTLERİ TAMAMLANDI!")


if __name__ == "__main__":
    main()

