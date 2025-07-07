import sys
from pathlib import Path

# Add the project root folder to sys.path so imports work correctly
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from preprocessing.clean_data import preprocess_input, PropertyInput

def test_preprocess_input():
    # your test code here
    pass

# Create example input data
example_data = PropertyInput(
    habitableSurface=120.5,
    bedroomCount=3,
    buildingCondition=4,
    hasGarden=1,
    gardenSurface=50.0,
    hasTerrace=0,
    epcScore=75,
    hasParking=1,
    postCode=1000,
    type="Apartment",
    province="Brussels",
    subtype="Penthouse",
    region="Brussels-Capital"
)

# Run preprocessing
df = preprocess_input(example_data)
print(df)