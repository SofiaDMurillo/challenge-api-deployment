from pydantic import BaseModel
from typing import Optional, Literal
import logging
import pandas as pd


# STEP 1 - Define the input parameters 

class PropertyInput(BaseModel):
    area: int
    property_type: Literal["APARTMENT", "HOUSE", "OTHERS"]
    rooms_number: int
    zip_code: int
    land_area: Optional[int] = None
    garden: Optional[bool] = False
    garden_area: Optional[int] = 0
    equipped_kitchen: Optional[bool] = False
    full_address: Optional[str] = None
    swimming_pool: Optional[bool] = False
    furnished: Optional[bool] = False
    open_fire: Optional[bool] = False
    terrace: Optional[bool] = False
    terrace_area: Optional[int] = 0
    facades_number: Optional[int] = None
    building_state: Optional[Literal["NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO REBUILD"]] = "GOOD"

# STEP 2 - Compare to input requirements from model and apply preprocessing rules
    # 2.1 Mandatory fields to be checked if not there error will be raised and model will not be run

def process_mandatory_fields(data: dict):
    mandatory_mapping = {
        'habitableSurface': 'area',
        'bedroomCount': 'rooms_number',
        'postCode': 'zip_code',
        'type': 'property_type'
    }

# Check for missing mandatory fields
    missing_fields = [model_field for model_field, input_field in mandatory_mapping.items()
                      if input_field not in data or data[input_field] is None]

    if missing_fields:
        raise ValueError(f"Missing mandatory fields for prediction: {missing_fields}")

    mapped_values = {
        'habitableSurface': data['area'],
        'bedroomCount': data['rooms_number'],
        'postCode': str(data['zip_code']),
        'type': data['property_type'].upper()
    }

    return mapped_values

# 2.2 will use Garden and Terrace info if available, if not, will default to False/zero and will still use the variables in the model

def process_garden_terrace_fields(data: dict):
    """
    Process optional fields: garden, garden_area, terrace.
    Uses provided values if available, else defaults.
    Returns a dictionary with mapped values.
    """
    processed = {
        'hasGarden': bool(data.get('garden', False)),
        'gardenSurface': int(data.get('garden_area', 0)),
        'hasTerrace': bool(data.get('terrace', False))
    }
    return processed

def process_building_condition(data: dict):
    """
    Process building condition field, 
    Uses value if available, else defaults to 'Good' and runs model 
    Returns a dictionary with the mapped value 
    Returns a message staying what Building Condition was used
    """
    condition_mapping = {
        'NEW': 5,
        'JUST RENOVATED': 4,
        'GOOD': 3,
        'TO RENOVATE': 2,
        'TO REBUILD': 1
    }
    
    building_state = data.get('building_state', 'GOOD')
    mapped_value = condition_mapping.get(building_state.upper(), 3)

    return {'buildingCondition': mapped_value}


def build_model_input(data: dict) -> pd.DataFrame:
    # Map building_state string to int code using your existing function
    building_condition_dict = process_building_condition(data)
    building_condition = building_condition_dict['buildingCondition']

    final_input = {
        'habitableSurface': data['area'],                 # from data.area
        'bedroomCount': data['rooms_number'],             # from data.rooms_number
        'buildingCondition': building_condition,           # mapped int
        'hasGarden': int(bool(data.get('garden', False))),  # bool → int
        'gardenSurface': int(data.get('garden_area', 0)),    # int, default 0
        'hasTerrace': int(bool(data.get('terrace', False))),  # bool → int
        'postCode': str(data['zip_code']),                 # string of zip_code
        'type': data['property_type'].upper(),             # uppercase string
    }

    return pd.DataFrame([final_input])


logging.basicConfig(level=logging.INFO)

def log_prediction_input(final_input: dict):
    """
    Log the final input values used for prediction.
    """
    logging.info(f"Prediction input values: {final_input}")
    # Or if just printing to console:
    print(f"Prediction input values: {final_input}")
