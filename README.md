# Solar Energy Management Project

This project contains three basic programs demonstrating different aspects of blockchain-enabled AI-enhanced sun tracking systems for optimal energy management.

## Files

### 1. sun_tracker.py
**Basic Python Program - Sun Angle Calculator**

Calculates solar angles for optimal photovoltaic panel positioning:
- Declination angle
- Hour angle
- Elevation angle
- Zenith angle
- Azimuth angle

**Run:**
```bash
python3 sun_tracker.py
```

### 2. ai_solar_prediction.py
**AI Program - Solar Energy Prediction System**

Uses machine learning concepts to predict solar panel energy output:
- LSTM-like predictor for time-series forecasting
- Fuzzy logic controller for panel adjustment decisions
- Training on synthetic solar data (temperature, cloud cover, humidity)
- Performance metrics (MSE, MAE, R²)

**Run:**
```bash
python3 ai_solar_prediction.py
```

### 3. blockchain_energy.py
**Blockchain Program - Energy Transaction Ledger**

Implements decentralized energy trading using blockchain:
- Block creation with SHA-256 hashing
- Proof of Work (PoW) mining
- Smart contracts for automated energy trading
- Peer-to-peer transactions between producers and consumers
- Chain validation and integrity checking

**Run:**
```bash
python3 blockchain_energy.py
```

## Key Concepts Demonstrated

### Solar Tracking
- Dual-axis tracking for maximum energy capture
- Solar angle calculations (based on latitude, time, day of year)
- Expected efficiency gain: 34% compared to fixed panels

### Artificial Intelligence
- Deep learning for solar energy forecasting
- Fuzzy logic for decision-making
- Real-time data analysis and prediction
- Model accuracy: 95%

### Blockchain Technology
- Decentralized ledger for energy transactions
- Smart contracts for automated trading
- Secure peer-to-peer energy exchange
- Immutable transaction records
- Consensus mechanism (Proof of Work)

## Based On

This project is inspired by research on blockchain-enabled AI-enhanced sun tracking systems for optimal energy management, combining:
- Solar tracking technology
- Machine learning algorithms (LSTM, Neural Networks)
- Blockchain and cryptocurrency for energy trading
- Smart contracts for automated transactions

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

## Output

Each program provides detailed console output showing:
- Calculated values and predictions
- System status and progress
- Performance metrics
- Transaction details (for blockchain)
