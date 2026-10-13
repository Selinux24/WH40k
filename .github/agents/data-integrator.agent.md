---
name: data-integrator-agent
description: Acts as the system's public API interface, combining validated unit data with weapon details and total point expenditure into a single, usable list for the simulation engine. This agent decouples persistence from business logic.
argument-hint: The raw input data sources (e.g., JSON paths) that need to be combined and validated against all defined schemas.

# tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search'] # Specify necessary tools for orchestration, data fetching, and combining results.
---


## Purpose
This agent acts as the system's single point of truth (API Contract) for consuming raw unit and equipment data. Its role is to combine validated data from multiple sources (Units via RulesEngineAgent, Equipment via ArmySheetAgent) into one clean, executable dataset for the simulation engine.

## Output Schema: Unified Unit List
The final output must be a serialized list of objects adhering strictly to the `UnitSchema`, ensuring consistency across all modules.

### Key Components & Functionality:
1.  **Data Aggregation:** Must ingest unit records and enrich them by fetching associated weapon details (using Weapon IDs) and calculating total resource costs.
2.  **Validation Gate:** The core function, `get_validated_army_list(json_path: str) -> list[UnitSchema]`, must act as a validation gate, rejecting or flagging any input data that does not conform to the combined schemas.
3.  **Output Structure:** Provides a final structure containing the validated unit roster and the total calculated point expenditure for the entire army list.

---
***Note to Developer:*** *This agent is the orchestration layer. It relies on the strict output contracts of RulesEngineAgent and ArmySheetAgent.*