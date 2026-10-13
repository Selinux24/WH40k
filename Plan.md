# Plan for Warhammer 40k Combat Analysis System

## Overview
This project aims to create a sophisticated system capable of ingesting and analyzing the complex ruleset of Warhammer 40k from various sources (regulations, army books, FAQs) to perform detailed combat analysis. The goal is to generate comprehensive reports listing all possible weapon configurations for an army list and estimating the resulting damage output against units from other codexes.

## Architectural Strategy: Context Management
Given the large volume of documentation (PDFs, TXT rules), a layered approach is necessary to avoid context exhaustion. Key strategies will include:
1.  **Modular Knowledge Base:** Treating each major rulebook or document category as a distinct module within the system's knowledge graph/database structure.
2.  **Abstraction Layers:** Using an initial analysis phase (Phase 1) to generate abstract data models and calculation algorithms, rather than trying to process all raw text simultaneously.
3.  **API/Service Pattern:** Implementing services for specific functions (e.g., `DamageCalculatorService`, `ListGeneratorService`) that consume structured data inputs rather than raw textual rules.

## Development Phases & Agents
The project will be developed using specialized agents, each responsible for one phase of the system build-out.

### Phase 1: Data Model Inference & Core Algorithms (Knowledge Acquisition)
*   **Goal:** Read general rules from PDFs and infer the canonical data model (e.g., Unit Schema, Weapon Schema, Ability/Stratagem Schema).
*   **Expected Output:** A formal definition of the database schema and pseudocode for core damage calculation logic.
*   **Agent Focus:** `RuleModelInferenceAgent`

### Phase 2: Data Model & Persistence Implementation (Structure)
*   **Goal:** Implement the inferred data model using a robust, structured storage solution (e.g., SQLite/PostgreSQL). Create initial ORM/schema definitions.
*   **Expected Output:** Database schema definitions and basic CRUD operations for core entities.
*   **Agent Focus:** `DataModelAgent`

### Phase 3: Testing and Validation (Safety Net)
*   **Goal:** Generate comprehensive, representative test data sets based on existing rules or known valid army lists. Implement unit tests for the damage calculation algorithms.
*   **Expected Output:** Test dataset files (JSON/YAML) and a suite of passing unit tests.
*   **Agent Focus:** `TestGeneratorAgent`

### Phase 4: Data Integration Pipeline (Ingestion & Updates)
*   **Goal:** Create ingestion tools to handle structured data updates from external sources (e.g., NewRecruit JSON, updated PDF rules). This must be resilient to changes in source formats.
*   **Expected Output:** Dedicated parsers/ingesters for different input types.
*   **Agent Focus:** `DataIngestionAgent`

### Phase 5: Core Logic Execution & API (Functionality)
*   **Goal:** Implement the core business logic classes: List Generation and Damage Calculation Engines. These services will use the structured data from Phase 2/4.
*   **Expected Output:** The primary service layer code (`ListGeneratorService`, `DamageCalculatorService`).
*   **Agent Focus:** `CoreLogicEngineAgent`

### Phase 6: Web Interface & User Experience (Presentation)
*   **Goal:** Develop a web application to provide the user interface. This tool will consume the services from Phase 5 and allow interactive list building and comparison viewing.
*   **Expected Output:** Frontend code (e.g., React/Vue setup) and API endpoints for the core logic.
*   **Agent Focus:** `WebInterfaceAgent`

## Project Structure & Next Steps
The codebase will be organized under the [Code/](c:\Users\Usuario\source\repos\Selinux24\WH40k\Code/) directory, with specialized agent skills and instructions stored in a dedicated `agents/` folder.

**Next immediate steps:**
1.  Create the necessary directories: `agents/`, `docs/rules/`. (Directories already exist or are planned).
2.  Define initial skills within these agents that guide their work according to this plan.
3.  Begin Phase 1 by analyzing a representative PDF rule document to solidify the data model inference process.