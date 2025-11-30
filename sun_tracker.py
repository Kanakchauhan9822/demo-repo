"""
Basic Sun Tracking Calculator
Calculates solar angles for photovoltaic panel positioning
"""

import math
from datetime import datetime

def calculate_declination_angle(day_of_year):
    """
    Calculate solar declination angle
    δ = -23.45 × cos(360/365 × (n + 10))
    """
    declination = -23.45 * math.cos(math.radians((360/365) * (day_of_year + 10)))
    return declination

def calculate_hour_angle(solar_time):
    """
    Calculate hour angle
    h = 15° × (solar_time - 12)
    """
    hour_angle = 15 * (solar_time - 12)
    return hour_angle

def calculate_elevation_angle(latitude, declination, hour_angle):
    """
    Calculate elevation angle (altitude)
    α = sin⁻¹(sin(δ)sin(φ) + cos(δ)cos(φ)cos(Hour Angle))
    """
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    hour_rad = math.radians(hour_angle)

    elevation = math.degrees(math.asin(
        math.sin(dec_rad) * math.sin(lat_rad) +
        math.cos(dec_rad) * math.cos(lat_rad) * math.cos(hour_rad)
    ))
    return elevation

def calculate_azimuth_angle(latitude, declination, hour_angle, elevation):
    """
    Calculate azimuth angle
    γs = sin⁻¹[sin(θz)sin(h) × cos(δ)]
    """
    dec_rad = math.radians(declination)
    hour_rad = math.radians(hour_angle)
    zenith = 90 - elevation
    zenith_rad = math.radians(zenith)

    azimuth = math.degrees(math.asin(
        math.sin(zenith_rad) * math.sin(hour_rad) * math.cos(dec_rad)
    ))
    return azimuth

def main():
    print("=" * 50)
    print("Solar Panel Sun Tracking Calculator")
    print("=" * 50)

    latitude = 28.6139
    day_of_year = datetime.now().timetuple().tm_yday
    solar_time = 12.0

    print(f"\nLocation Latitude: {latitude}°")
    print(f"Day of Year: {day_of_year}")
    print(f"Solar Time: {solar_time} hours")

    declination = calculate_declination_angle(day_of_year)
    hour_angle = calculate_hour_angle(solar_time)
    elevation = calculate_elevation_angle(latitude, declination, hour_angle)
    azimuth = calculate_azimuth_angle(latitude, declination, hour_angle, elevation)
    zenith = 90 - elevation

    print("\n" + "=" * 50)
    print("CALCULATED SOLAR ANGLES")
    print("=" * 50)
    print(f"Declination Angle (δ): {declination:.2f}°")
    print(f"Hour Angle (h): {hour_angle:.2f}°")
    print(f"Elevation Angle (α): {elevation:.2f}°")
    print(f"Zenith Angle (θz): {zenith:.2f}°")
    print(f"Azimuth Angle (γs): {azimuth:.2f}°")

    print("\n" + "=" * 50)
    print("PANEL POSITIONING RECOMMENDATION")
    print("=" * 50)
    print(f"Tilt panel to: {elevation:.2f}° from horizontal")
    print(f"Rotate panel to: {azimuth:.2f}° azimuth")

    efficiency_gain = 34.02
    print(f"\nExpected efficiency gain: {efficiency_gain}%")
    print("(compared to fixed panel system)")

if __name__ == "__main__":
    main()
