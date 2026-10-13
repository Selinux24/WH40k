# Rules Engine Schema Definition for Army Lists

## Purpose
This document defines the expected structure (schema) for all unit data ingested into the simulation engine. It ensures consistency when merging data from various sources.

## Core Entity: Unit
Every entry in an army list must conform to this schema.

| Field Name | Data Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| unit_name | String | Yes | The common name of the military unit. | Space Marines |
| points | Integer | Yes | The total cost/point value of the unit. | 180 |
| weapon_ids | Array[String] | No | List of unique IDs for weapons carried by the unit. | ["bolter", "plasma"] |
| abilities | Array[String] | No | List of special rules or inherent abilities. | ["basic", "overlord"] |
| army_list_id | String | Yes | Unique identifier for this specific entry in the list. (Generated during integration) | ARML-001 |

## Data Source Mapping Notes
*   **Source:** `DataSources/dummy_army_list.json`
*   The JSON structure is assumed to directly map to the 'Unit' entity fields above.
*   Integration must ensure that all arrays (`weapon_ids`, `abilities`) are properly handled and validated against known IDs (if a separate lookup table exists).

## Output Format Goal
The final, integrated dataset should be a list of structured objects suitable for direct consumption by the simulation module.