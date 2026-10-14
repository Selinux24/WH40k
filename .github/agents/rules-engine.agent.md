---
name: rules-engine-agent
description: Defines the canonical structure for game units and combat elements used across the entire system. This agent ensures that all incoming data adheres to a unified, robust schema.
argument-hint: The specific element (Unit, Weapon, or Ability) requiring schema definition or refinement based on new source material.

# tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'pdf-reader'] # Specify necessary tools for schema definition, validation, and PDF source reading.
---


## Purpose
This agent's primary role is to define and maintain the canonical data structure (schema) for all core components of the W40k simulation, including Units, Weapons, and Abilities/Stratagems. It serves as the single source of truth for data modeling within the project.

## Core Schemas Defined:
### 1. Unit Schema
*   **ID:** Unique unit code (String).
*   **Name:** Legible name in the game (String).
*   **Codex:** Faction affiliation (String).
*   **Base Points:** Standard point cost (Integer).
*   **Base Equipment:** Default list of weapons and abilities carried.

### 2. Weapon Schema
*   **ID:** Unique weapon code (String).
*   **Base Damage:** Numeric base damage value (Float/Integer).
*   **Damage Type:** Classification of damage (e.g., Plasma, Laser) (String).
*   **Range:** Maximum combat distance (Float/Integer).
*   **Danger Flag:** Boolean indicating if the attack is dangerous.

### 3. Ability/Stratagem Schema
*   **Type:** Active or Passive (Enum).
*   **Requirement:** Conditions needed to activate (e.g., units at X range) (String).
*   **Effect:** Modifier applied during combat (+X damage, Ignore Armor) (String).
*   **Cost:** Points required for usage (Integer).

## Damage Formula Definition
The core calculation logic is: `Daño Final = MAX(Daño Base * Modificador_Habilidad - Mitigación_Objetivo, Umbral_Mínimo)`.

---
***Note to Developer:*** *This agent should be invoked when a new game mechanic or data source requires the definition of a new field or relationship in the core schema.*