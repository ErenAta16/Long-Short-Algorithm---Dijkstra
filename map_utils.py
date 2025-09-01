#!/usr/bin/env python3
"""
🗺️ HARİTA İŞLEMLERİ 🗺️
Folium harita oluşturma ve görselleştirme fonksiyonları - Tali yolları önceliklendir
"""

import folium
from typing import Dict, List, Tuple, Optional
from fire_stations import categorize_fire_stations

def create_interactive_map(fire_stations: Dict[str, Tuple[float, float]]) -> str:
    """Etkileşimli harita oluştur - Yangın noktası seçimi için"""
    # Marmara Bölgesi merkezi
    center_lat, center_lon = 40.5, 28.5
    
    # Harita oluştur
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=8,
        tiles='OpenStreetMap'
    )
    
    # Harita kontrolleri ekle
    folium.LayerControl().add_to(m)
    
    # İtfaiye istasyonlarını bölgelere göre grupla ve farklı renklerle göster
    region_colors = {
        "Marmara Bölgesi Ana İtfaiyeler": ("red", "fire-extinguisher"),
        "Bursa İlçe İtfaiyeleri": ("darkred", "fire-extinguisher"),
        "Balıkesir İlçe İtfaiyeleri": ("orange", "fire-extinguisher"),
        "Çanakkale İlçe İtfaiyeleri": ("lightred", "fire-extinguisher"),
        "Tekirdağ İlçe İtfaiyeleri": ("cadetblue", "fire-extinguisher"),
        "Kırklareli İlçe İtfaiyeleri": ("blue", "fire-extinguisher"),
        "Yalova İlçe İtfaiyeleri": ("purple", "fire-extinguisher")
    }
    
    # Bölgelere göre grupla
    regions = categorize_fire_stations(fire_stations)
    
    # Her bölgeyi ayrı ayrı ekle
    for region_name, stations in regions.items():
        if stations:
            color, icon = region_colors[region_name]
            for name, coords in stations:
                folium.Marker(
                    coords,
                    popup=f"🚒 {name}<br><small>{region_name}</small>",
                    tooltip=f"🚒 {name}",
                    icon=folium.Icon(color=color, icon=icon)
                ).add_to(m)
    
    # Harita dosyasını kaydet
    map_file = "interactive_fire_map.html"
    m.save(map_file)
    return map_file

def create_emergency_route_map(
    fire_stations: Dict[str, Tuple[float, float]],
    fire_location: Tuple[float, float],
    nearest_station: str,
    route_info: Dict
) -> str:
    """Acil durum rota haritası oluştur - Tali yolları önceliklendir"""
    # Harita merkezi (yangın noktası ve en yakın itfaiye arasında)
    fire_lat, fire_lon = fire_location
    station_coords = fire_stations[nearest_station]
    
    center_lat = (fire_lat + station_coords[0]) / 2
    center_lon = (fire_lon + station_coords[1]) / 2
    
    # Harita oluştur
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Yangın noktasını işaretle
    folium.Marker(
        fire_location,
        popup=f"🔥 YANGIN NOKTASI<br><small>Koordinat: {fire_lat:.6f}, {fire_lon:.6f}</small>",
        tooltip="🔥 YANGIN NOKTASI",
        icon=folium.Icon(color='red', icon='fire')
    ).add_to(m)
    
    # En yakın itfaiyeyi işaretle
    folium.Marker(
        station_coords,
        popup=f"🚒 {nearest_station}<br><small>Koordinat: {station_coords[0]:.6f}, {station_coords[1]:.6f}</small>",
        tooltip=f"🚒 {nearest_station}",
        icon=folium.Icon(color='darkred', icon='fire-extinguisher')
    ).add_to(m)
    
    # Rotayı çiz
    route_drawn = False
    
    # OSRM geometrisi varsa onu kullan
    if route_info.get('decoded_geometry') and 'coordinates' in route_info['decoded_geometry']:
        try:
            coords = route_info['decoded_geometry']['coordinates']
            print(f"✅ Decoded OSRM geometrisi bulundu: {len(coords)} nokta")
        except:
            coords = []
    elif route_info.get('geometry') and len(route_info['geometry']) > 0:
        try:
            coords = route_info['geometry']
            print(f"✅ OSRM geometrisi bulundu: {len(coords)} nokta")
            
            # Rota türüne göre renk ve kalınlık belirle
            route_type = route_info.get('route_type', 'N/A')
            terrain_type = route_info.get('terrain_type', 'unknown')
            secondary_ratio = route_info.get('secondary_ratio', 0)
            
            # Tali yol oranına göre renk belirle
            if 'Tali Yol' in route_type or secondary_ratio > 0.5:
                color = 'green'
                weight = 8  # Daha kalın çizgi
                tooltip_text = f"🌾 Tali Yol Rotası: {route_info.get('distance', 0):.1f} km (Tali yol: {secondary_ratio*100:.1f}%)"
            elif 'Ana Yol' in route_type:
                color = 'blue'
                weight = 5
                tooltip_text = f"🛣️ Ana Yol Rotası: {route_info.get('distance', 0):.1f} km (Tali yol: {secondary_ratio*100:.1f}%)"
            else:
                color = 'purple'
                weight = 6
                tooltip_text = f"🛤️ Karma Yol Rotası: {route_info.get('distance', 0):.1f} km (Tali yol: {secondary_ratio*100:.1f}%)"
            
            # Arazi türüne göre ek bilgi
            if terrain_type == "mountain_forest":
                tooltip_text += " 🏔️ Dağ/Orman"
            elif terrain_type == "rural":
                tooltip_text += " 🌾 Kırsal"
            else:
                tooltip_text += " 🏙️ Şehir"
            
            # Koordinatları kontrol et ve düzelt
            valid_coords = []
            for coord in coords:
                if len(coord) == 2 and isinstance(coord[0], (int, float)) and isinstance(coord[1], (int, float)):
                    # Koordinatlar [lat, lon] formatında olmalı
                    if -90 <= coord[0] <= 90 and -180 <= coord[1] <= 180:
                        valid_coords.append(coord)
            
            if valid_coords:
                folium.PolyLine(
                    valid_coords,
                    weight=weight,
                    color=color,
                    opacity=0.8,
                    tooltip=tooltip_text
                ).add_to(m)
                route_drawn = True
                print(f"✅ Gerçek rota geometrisi çizildi ({len(valid_coords)} nokta)")
                print(f"   🎨 Rota türü: {route_type} - Renk: {color} - Kalınlık: {weight}")
                print(f"   🗺️ Arazi türü: {terrain_type} - Tali yol oranı: {secondary_ratio*100:.1f}%")
            else:
                print("⚠️ Geçersiz koordinatlar bulundu, fallback kullanılıyor")
                
        except Exception as e:
            print(f"⚠️ Route geometri hatası: {e}")
            print("⚠️ Fallback rota çizimi kullanılıyor")
    
    # OSRM geometrisi yoksa veya hatalıysa fallback olarak OSRM ile rota çiz
    if not route_drawn:
        print("🔄 OSRM ile fallback rota çizimi yapılıyor...")
        
        # Basit rota çizimi
        coords = f"{station_coords[1]},{station_coords[0]};{fire_lon},{fire_lat}"
        
        # Tali yolları önceliklendiren profiller - Arazi türüne göre
        terrain_type = route_info.get('terrain_type', 'rural')
        
        if terrain_type == "mountain_forest":
            # Dağ/orman için tali yolları önceliklendir
            profiles = [
                ('foot', 'Yaya - Tali Yol', 'green', 8),
                ('cycling', 'Bisiklet - Tali Yol', 'lime', 8),
                ('driving', 'Araç - Karma', 'blue', 5)
            ]
        elif terrain_type == "rural":
            # Kırsal için tali yolları tercih et
            profiles = [
                ('foot', 'Yaya - Tali Yol', 'green', 7),
                ('cycling', 'Bisiklet - Tali Yol', 'lime', 7),
                ('driving', 'Araç - Karma', 'blue', 5)
            ]
        else:
            # Şehir için normal profiller
            profiles = [
                ('driving', 'Araç - Karma', 'blue', 5),
                ('foot', 'Yaya - Tali Yol', 'green', 6),
                ('cycling', 'Bisiklet - Tali Yol', 'lime', 6)
            ]
        
        for profile, profile_name, color, weight in profiles:
            try:
                import requests
                url = f"https://router.project-osrm.org/route/v1/{profile}/{coords}"
                params = {
                    'overview': 'full',
                    'geometries': 'geojson',
                    'steps': 'true'
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('routes'):
                        geo = data['routes'][0]['geometry']['coordinates']
                        # OSRM'den gelen koordinatlar [lon, lat] formatında
                        # Folium için [lat, lon] formatına çevir
                        geo_latlon = [[lat, lon] for lon, lat in geo]
                        
                        folium.PolyLine(
                            geo_latlon,
                            weight=weight,
                            color=color,
                            opacity=0.8,
                            tooltip=f"🛣️ {profile_name}: {route_info.get('distance', 0):.1f} km"
                        ).add_to(m)
                        route_drawn = True
                        print(f"✅ {profile_name} profili ile rota çizildi")
                        print(f"   🎨 Renk: {color}, Kalınlık: {weight}")
                        print(f"   📍 {len(geo_latlon)} nokta ile rota çizildi")
                        break
            except Exception as e:
                print(f"⚠️ {profile_name} hatası: {e}")
                continue
    
    # Hiçbir rota çizilemezse basit çizgi çiz
    if not route_drawn:
        print("⚠️ Hiçbir rota çizilemedi, basit çizgi çiziliyor...")
        folium.PolyLine(
            [station_coords, fire_location],
            weight=3,
            color='red',
            opacity=0.6,
            tooltip="⚠️ Basit rota (OSRM hatası)"
        ).add_to(m)
        print("✅ Basit çizgi rota çizildi")
    
    # Bilgi kutusu ekle
    info_html = f"""
    <div style="position: fixed; top: 20px; right: 20px; width: 350px; background: white; 
         border: 2px solid #ff4444; border-radius: 10px; padding: 20px; z-index: 1000; 
         box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
        <h3 style="color: #ff4444; margin: 0 0 15px 0;">🚨 ACİL DURUM ROTASI</h3>
        <p><strong>🚒 İtfaiye:</strong> {nearest_station}</p>
        <p><strong>🔥 Yangın Noktası:</strong> {fire_lat:.6f}, {fire_lon:.6f}</p>
        <p><strong>📏 Mesafe:</strong> {route_info.get('base_route', {}).get('distance', 0):.1f} km</p>
        <p><strong>🛣️ Rota Türü:</strong> {route_info.get('base_route', {}).get('route_type', 'N/A')}</p>
        <p><strong>🗺️ Arazi Türü:</strong> {route_info.get('terrain_type', 'N/A')}</p>
        <p><strong>🌾 Tali Yol Oranı:</strong> {route_info.get('base_route', {}).get('secondary_ratio', 0)*100:.1f}%</p>
        <p><strong>⏱️ Tahmini Süre:</strong> {route_info.get('base_route', {}).get('duration', 0):.1f} dakika</p>
        <button onclick="this.parentElement.remove()" 
                style="background: #666; color: white; border: none; padding: 8px 16px; 
                       border-radius: 4px; cursor: pointer;">
            Kapat
        </button>
    </div>
    """
    
    # HTML bilgi kutusunu ekle
    folium.Html(
        info_html,
        script=True
    ).add_to(m)
    
    # Harita dosyasını kaydet
    map_file = "emergency_route_map.html"
    m.save(map_file)
    return map_file
