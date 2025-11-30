"""
ai_prediction.py - AI-Enhanced Solar Energy Prediction Module
Uses machine learning to predict solar panel energy output
"""

import random
import math

class SimpleLSTMPredictor:
    """Simplified LSTM-like predictor for solar energy forecasting"""
    
    def __init__(self):
        random.seed(42)
        self.weights = [random.gauss(0, 1) for _ in range(5)]
        self.historical_data = []
        self.learning_rate = 0.01
    
    def add_data(self, features, target):
        """Add training data"""
        self.historical_data.append((features, target))
    
    def predict(self, features):
        """
        Predict energy output based on features:
        [hour, temperature, cloud_cover, humidity, day_of_year]
        """
        if len(features) != 5:
            raise ValueError("Expected 5 features")
        
        prediction = sum(w * f for w, f in zip(self.weights, features))
        return max(0, prediction)
    
    def train(self, epochs=100, verbose=False):
        """Simple gradient descent training"""
        if not self.historical_data:
            print("No training data available")
            return
        
        for epoch in range(epochs):
            total_loss = 0
            for features, target in self.historical_data:
                prediction = self.predict(features)
                error = target - prediction
                
                for i in range(len(self.weights)):
                    self.weights[i] += self.learning_rate * error * features[i]
                
                total_loss += error ** 2
            
            if verbose and epoch % 20 == 0:
                mse = total_loss / len(self.historical_data)
                print(f"  Epoch {epoch}: MSE = {mse:.4f}")

class FuzzyLogicController:
    """Fuzzy logic controller for panel adjustment decisions"""
    
    def __init__(self):
        self.rules = {
            'low_sun': {'action': 'increase_tilt', 'value': 15},
            'medium_sun': {'action': 'optimal_tilt', 'value': 45},
            'high_sun': {'action': 'decrease_tilt', 'value': 60}
        }
    
    def fuzzify_sun_elevation(self, elevation):
        """Convert crisp elevation to fuzzy categories"""
        if elevation < 30:
            return 'low_sun'
        elif elevation < 60:
            return 'medium_sun'
        else:
            return 'high_sun'
    
    def decide_action(self, elevation, current_output, predicted_output):
        """Fuzzy logic decision making"""
        sun_category = self.fuzzify_sun_elevation(elevation)
        rule = self.rules[sun_category]
        
        # Handle zero or negative predictions
        if predicted_output <= 0:
            return "NO PRODUCTION: Sun below horizon or insufficient light", False
        
        efficiency_ratio = current_output / predicted_output
        
        if efficiency_ratio < 0.7:
            return f"ADJUST: {rule['action']} to {rule['value']}°", False
        else:
            return "MAINTAIN: Current position optimal", True

class AIEnergyPredictor:
    """Main AI predictor class combining LSTM and Fuzzy Logic"""
    
    def __init__(self):
        self.predictor = SimpleLSTMPredictor()
        self.fuzzy_controller = FuzzyLogicController()
        self.trained = False
    
    def generate_training_data(self):
        """Generate synthetic training data for solar prediction"""
        data = []
        random.seed(42)
        
        for day in range(30):
            for hour in range(6, 20):
                temperature = 15 + 10 * math.sin((hour - 6) / 14 * math.pi) + random.gauss(0, 1) * 2
                cloud_cover = max(0, min(1, random.betavariate(2, 5)))
                humidity = 0.4 + 0.3 * random.random()
                
                base_output = 50 * math.sin((hour - 6) / 14 * math.pi)
                weather_factor = (1 - cloud_cover) * (1 - humidity * 0.3)
                energy_output = base_output * weather_factor * (1 + temperature / 100)
                
                features = [hour, temperature, cloud_cover, humidity, day]
                data.append((features, energy_output))
        
        return data
    
    def initialize_and_train(self, verbose=False):
        """Initialize and train the AI model"""
        if verbose:
            print("Generating training data...")
        
        training_data = self.generate_training_data()
        
        if verbose:
            print(f"Training on {len(training_data)} samples...")
        
        for features, target in training_data:
            self.predictor.add_data(features, target)
        
        self.predictor.train(epochs=100, verbose=verbose)
        self.trained = True
        
        if verbose:
            print("Training complete!")
    
    def predict_and_control(self, solar_time, temperature, cloud_cover, 
                           humidity, day_of_year, elevation):
        """
        Predict energy output and provide control decision
        Returns dictionary with prediction and control data
        """
        if not self.trained:
            raise RuntimeError("Model not trained. Call initialize_and_train() first.")
        
        hour = int(solar_time)
        features = [hour, temperature, cloud_cover, humidity, day_of_year]
        predicted_output = self.predictor.predict(features)
        
        # Check if it's nighttime or very low production
        if predicted_output < 0.1 or elevation < 0:
            return {
                'predicted_output': 0.0,
                'current_actual': 0.0,
                'efficiency': 0.0,
                'decision': 'NO PRODUCTION: Nighttime or sun below horizon',
                'is_optimal': False,
                'is_nighttime': True
            }
        
        # Simulate current actual output
        current_actual = predicted_output * (0.85 + random.random() * 0.15)
        
        # Get fuzzy logic decision
        decision, is_optimal = self.fuzzy_controller.decide_action(
            elevation, current_actual, predicted_output
        )
        
        efficiency = (current_actual / predicted_output) * 100
        
        return {
            'predicted_output': predicted_output,
            'current_actual': current_actual,
            'efficiency': efficiency,
            'decision': decision,
            'is_optimal': is_optimal,
            'is_nighttime': False
        }
    
    def display_results(self, prediction_data, inputs):
        """Display AI prediction results"""
        hour = int(inputs['solar_time'])
        minute = int((inputs['solar_time'] % 1) * 60)
        
        print(f"\nCurrent Conditions:")
        print(f"  Time: {hour:02d}:{minute:02d}")
        print(f"  Temperature: {inputs['temperature']:.1f}°C")
        print(f"  Cloud Cover: {inputs['cloud_cover'] * 100:.1f}%")
        print(f"  Humidity: {inputs['humidity'] * 100:.1f}%")
        
        if prediction_data.get('is_nighttime', False):
            print(f"\nPredicted Energy Output: 0.00 kWh")
            print(f"Current Actual Output: 0.00 kWh")
            print(f"System Efficiency: N/A (Nighttime)")
            print(f"\nStatus: 🌙 NIGHTTIME - No solar production")
        else:
            print(f"\nPredicted Energy Output: {prediction_data['predicted_output']:.2f} kWh")
            print(f"Current Actual Output: {prediction_data['current_actual']:.2f} kWh")
            print(f"System Efficiency: {prediction_data['efficiency']:.1f}%")
            
            print(f"\nFuzzy Logic Decision: {prediction_data['decision']}")
            
            if prediction_data['is_optimal']:
                print("Status: ✓ OPTIMAL")
            else:
                print("Status: ⚠ NEEDS ADJUSTMENT")

# Standalone execution mode
if __name__ == "__main__":
    print("=" * 60)
    print("AI Energy Prediction System (Standalone Mode)")
    print("=" * 60)
    
    predictor = AIEnergyPredictor()
    
    print("\nInitializing and training model...")
    predictor.initialize_and_train(verbose=True)
    
    # Get inputs
    print("\n" + "=" * 60)
    solar_time = float(input("Enter solar time (hours, 0-24): "))
    temperature = float(input("Enter temperature (°C): "))
    cloud_cover = float(input("Enter cloud cover (0-100%): ")) / 100.0
    humidity = float(input("Enter humidity (0-100%): ")) / 100.0
    day_of_year = int(input("Enter day of year (1-365): "))
    elevation = float(input("Enter sun elevation angle (degrees): "))
    
    inputs = {
        'solar_time': solar_time,
        'temperature': temperature,
        'cloud_cover': cloud_cover,
        'humidity': humidity
    }
    
    # Predict and display
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    prediction_data = predictor.predict_and_control(
        solar_time, temperature, cloud_cover, humidity, day_of_year, elevation
    )
    
    predictor.display_results(prediction_data, inputs)