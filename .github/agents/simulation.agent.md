---
name: simulation-agent
description: Executes the core combat and gameplay logic using the validated, integrated army list data. This agent calculates outcomes, manages turn order, and determines win/loss conditions based on established rules.
argument-hint: The validated and finalized Unit Schema dataset to run the simulation against.

# tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search'] # Specify necessary tools for complex logic execution and state management.
---


## Purpose
This agent is the heart of the application, responsible for simulating combat encounters. It takes the clean data output from the DataIntegratorAgent and executes turn-based combat resolution using the schemas defined by the RulesEngineAgent.

## Core Logic & Workflow:
1.  **Initialization:** Accepts two or more validated army lists (Player A, Player B). Sets up initial state (positioning, readiness status, remaining resources/points).
2.  **Combat Loop:** Iterates through turns, resolving actions sequentially until a victory condition is met or all units are destroyed.
3.  **Damage Resolution:** Must utilize the canonical Damage Formula: `Daño Final = MAX(Daño Base * Modificador_Habilidad - Mitigación_Objetivo, Umbral_Mínimo)`.
4.  **State Management:** Tracks unit status (destroyed, disabled, etc.) and resource consumption throughout the simulation run.

## Dependencies
*   Requires a stable schema from `RulesEngineAgent` for all combat parameters.
*   Relies on validated data from `DataIntegratorAgent` for input lists.