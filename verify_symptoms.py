from ml_engine import predictor

def test_prediction(symptoms, expected_disease):
    print(f"Testing Symptoms: '{symptoms}'")
    result = predictor.predict(symptoms, "none.jpg")
    print(f"Prediction: {result['prediction']} (Confidence: {result['confidence']})")
    
    if expected_disease in result['prediction']:
        print("[PASS]")
    else:
        print(f"[FAIL] (Expected {expected_disease})")
    print("-" * 20)

print("--- Verifying Disease Knowledge Base ---")
test_prediction("I have lost my sense of smell and feel tired", "COVID-19")
test_prediction("My joints are swelling and painful", "Arthritis")
test_prediction("Severe headache and pain behind eyes", "Dengue")
test_prediction("Heartburn and chest pain after eating", "GERD")
