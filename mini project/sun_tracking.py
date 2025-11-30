"""
sun_tracking.py - Solar Sun Tracking Calculator Module
Calculates solar angles for photovoltaic panel positioning
"""

import math

class SunTracker:
    """Sun tracking calculator for solar panel positioning"""
    
    def __init__(self):
        self.declination = None
        self.hour_angle = None
        self.elevation = None
        self.azimuth = None
        self.zenith = None
    
    def calculate_declination_angle(self, day_of_year):
        """
        Calculate solar declination angle
        δ = -23.45 × cos(360/365 × (n + 10))
        """
        declination = -23.45 * math.cos(math.radians((360/365) * (day_of_year + 10)))
        return declination
    
    def calculate_hour_angle(self, solar_time):
        """
        Calculate hour angle
        h = 15° × (solar_time - 12)
        """
        hour_angle = 15 * (solar_time - 12)
        return hour_angle
    
    def calculate_elevation_angle(self, latitude, declination, hour_angle):
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
    
    def calculate_azimuth_angle(self, latitude, declination, hour_angle, elevation):
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
    
    def calculate_sun_position(self, latitude, day_of_year, solar_time):
        """
        Calculate all solar angles for given parameters
        Returns dictionary with all calculated angles
        """
        self.declination = self.calculate_declination_angle(day_of_year)
        self.hour_angle = self.calculate_hour_angle(solar_time)
        self.elevation = self.calculate_elevation_angle(latitude, self.declination, self.hour_angle)
        self.azimuth = self.calculate_azimuth_angle(latitude, self.declination, self.hour_angle, self.elevation)
        self.zenith = 90 - self.elevation
        
        return {
            'declination': self.declination,
            'hour_angle': self.hour_angle,
            'elevation': self.elevation,
            'azimuth': self.azimuth,
            'zenith': self.zenith
        }
    
    def display_results(self, sun_data):
        """Display sun tracking calculation results"""
        print(f"\nDeclination Angle (δ): {sun_data['declination']:.2f}°")
        print(f"Hour Angle (h): {sun_data['hour_angle']:.2f}°")
        print(f"Elevation Angle (α): {sun_data['elevation']:.2f}°")
        print(f"Zenith Angle (θz): {sun_data['zenith']:.2f}°")
        print(f"Azimuth Angle (γs): {sun_data['azimuth']:.2f}°")
        
        print(f"\n→ Recommended Panel Tilt: {sun_data['elevation']:.2f}° from horizontal")
        print(f"→ Recommended Panel Azimuth: {sun_data['azimuth']:.2f}°")

# Standalone execution mode
if __name__ == "__main__":
    print("=" * 60)
    print("Sun Tracking Calculator (Standalone Mode)")
    print("=" * 60)
    
    tracker = SunTracker()
    
    # Get inputs
    latitude = float(input("\nEnter latitude (degrees): "))
    day_of_year = int(input("Enter day of year (1-365): "))
    solar_time = float(input("Enter solar time (hours, 0-24): "))
    
    # Calculate and display
    sun_data = tracker.calculate_sun_position(latitude, day_of_year, solar_time)
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    tracker.display_results(sun_data)