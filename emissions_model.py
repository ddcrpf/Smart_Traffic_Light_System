# Dummy model for emission prediction
def predict_emission(vehicle_type):
    # Replace with actual ML model logic
    emissions = {
        'car': 2.3,   # Example CO2 emissions in g/km
        'truck': 5.7,
        'motorcycle': 1.2,
        'bus': 6.5,
        'emergency': 0.0
    }
    return emissions.get(vehicle_type, 0)
