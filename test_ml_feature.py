import ml_engine
import json

print("\n--- Testing Medtrack Multimodal ML Engine ---\n")

# Test Case 1: Migraine Symptoms
text_1 = "I have a really bad headache and feel dizzy."
image_1 = "brain_scan.png"
print(f"Input: Text='{text_1}', Image='{image_1}'")
result_1 = ml_engine.predictor.predict(text_1, image_1)
print("Result:")
print(json.dumps(result_1, indent=2))

print("\n------------------------------------------------\n")

# Test Case 2: Infection Symptoms + XRay
text_2 = "I have a high fever and body aches."
image_2 = "chest_xray.png"
print(f"Input: Text='{text_2}', Image='{image_2}'")
result_2 = ml_engine.predictor.predict(text_2, image_2)
print("Result:")
print(json.dumps(result_2, indent=2))

print("\n--- Test Complete ---")
