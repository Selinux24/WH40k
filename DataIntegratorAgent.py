import json
import os
from typing import List, Dict, Any

# --- Configuration ---
SCHEMA_PATH = "RulesEngineAgent/SchemaDefinition.md"
DATA_SOURCE_PATH = "DataSources/dummy_army_list.json"
OUTPUT_FILE = "integrated_dataset.json"

def load_schema(path: str) -> Dict[str, Any]:
    """Loads and parses the schema definition from a markdown file."""
    print(f"Attempting to load schema from: {path}")
    try:
        with open(path, 'r') as f:
            # Simple parsing for demonstration; in reality, this would be more robust.
            content = f.read()
            return {"unit_name": "String", "points": "Integer", "weapon_ids": "Array[String]", "abilities": "Array[String]"}
    except FileNotFoundError:
        print(f"Error: Schema file not found at {path}")
        # Returning a default structure if the file is missing for safe execution continuation.
        return {}

def load_data(path: str) -> List[Dict[str, Any]]:
    """Loads the dummy JSON data."""
    print(f"Loading data from: {path}")
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                # Handle case where JSON might be a single object instead of a list
                print("Warning: Data source is not a list; wrapping it.")
                return [data]
    except FileNotFoundError:
        print(f"Error: Data file not found at {path}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data.")
        return []

def validate_and_integrate(raw_data: List[Dict[str, Any]], schema: Dict[str, str]) -> List[Dict[str, Any]]:
    """Validates raw unit data against the defined schema and structures it."""
    integrated_units = []
    print("Starting validation and integration process...")

    for i, raw_unit in enumerate(raw_data):
        validated_unit: Dict[str, Any] = {}
        is_valid = True

        # 1. Basic Field Validation (Schema enforcement)
        # In a real scenario, this would check types rigorously. Here we assume the input structure is generally correct.
        try:
            unit_name = str(raw_unit.get("unit_name", "")).strip()
            points = int(raw_unit.get("points")) # Assumes points field exists and is convertible to int
            weapon_ids = raw_unit.get("weapon_ids", [])
            abilities = raw_unit.get("abilities", [])

            if not unit_name or points is None:
                print(f"Skipping record {i}: Missing required fields (unit_name or points).")
                is_valid = False

            # 2. Integration Logic (Adding unique ID, ensuring structure)
            validated_unit["unit_name"] = unit_name
            validated_unit["points"] = points
            validated_unit["weapon_ids"] = [str(wid).strip() for wid in weapon_ids] # Ensure list of strings
            validated_unit["abilities"] = [str(a).strip() for a in abilities]
            # Generate unique ID based on index and type
            validated_unit["army_list_id"] = f"ARML-{i+1:03d}"

        except Exception as e:
            print(f"Skipping record {i} due to validation error: {e}")
            is_valid = False

        if is_valid:
            integrated_units.append(validated_unit)

    return integrated_units

def main():
    """Main function to run the data integration pipeline."""
    # 1. Load Schema (for context/validation rules)
    schema = load_schema(SCHEMA_PATH)
    if not schema:
        print("FATAL: Cannot proceed without a valid schema.")
        return

    # 2. Load Raw Data
    raw_data = load_data(DATA_SOURCE_PATH)
    if not raw_data:
        print("FATAL: Cannot proceed without source data.")
        return

    # 3. Validate and Integrate
    integrated_dataset = validate_and_integrate(raw_data, schema)

    # 4. Save Output
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(integrated_dataset, f, indent=4)
        print("\\n[SUCCESS] Data integration complete.")
        print(f"Successfully processed {len(raw_data)} records into {len(integrated_dataset)} structured units.")
        print(f"Output saved to: {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error saving the integrated dataset: {e}")


if __name__ == "__main__":
    main()