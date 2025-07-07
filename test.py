from preprocessing.cleaning_data import (
    process_mandatory_fields,
    process_garden_terrace_fields,
    process_building_condition,
    build_model_input
)
from predict.prediction import predict_price

# Example input data matching your PropertyInput model
input_data = {
    "area": 120,
    "property_type": "HOUSE",
    "rooms_number": 3,
    "zip_code": 1000,
    "garden": True,
    "garden_area": 50,
    "terrace": False,
    "building_state": "GOOD"
}

# STEP 1: Process mandatory fields
mandatory_fields = process_mandatory_fields(input_data)

# STEP 2: Process optional garden and terrace fields
garden_terrace_fields = process_garden_terrace_fields(input_data)

# STEP 3: Process building condition
building_condition_field = process_building_condition(input_data)

# STEP 4: Merge all preprocessed fields together
preprocessed_data = {
    **mandatory_fields,
    **garden_terrace_fields,
    **building_condition_field
}

# STEP 5: Build final model input (filter expected model fields)
final_input = build_model_input(preprocessed_data)

# STEP 6: Run prediction
predicted_price = predict_price(final_input)

# STEP 7: Display result
print(f"Predicted price: {predicted_price}")