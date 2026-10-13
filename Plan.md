# Plan de Proyecto: Analizador Avanzado de Reglas Warhammer 40k

## Objetivo General

Crear un sistema integral capaz de analizar las reglas completas de Warhammer 40k, procesando múltiples fuentes de documentación (reglamento general, libros de ejército, revisiones de puntos, Q&A) para generar una lista detallada y calculada de posibles configuraciones de armamento para cualquier lista de ejército. El resultado debe incluir un análisis exhaustivo del daño potencial que la lista puede infligir contra unidades de otros codex, considerando habilidades, estratagemas y equipamiento.

## Estrategia de Contexto Grande

Dado el gran volumen y la naturaleza evolutiva de los documentos (actualizaciones periódicas), se implementará una estrategia modular:

1. **Modelo de Datos Centralizado:** Definir un esquema de datos robusto e inmutable que sirva como fuente única de verdad para todas las unidades, armas y reglas.
2. **Ingesta por Componentes:** Desarrollar módulos de ingesta específicos (JSON para listas, PDF/TXT parsers para reglamentos) en lugar de depender de una sola lectura masiva.
3. **Base de Conocimiento Vectorial (Recomendado):** Utilizar un sistema de base de datos vectorial o graph database para indexar el texto completo y las reglas, permitiendo búsquedas semánticas que no agotan el contexto lineal del modelo.

## Fases de Desarrollo y Agentes Requeridos

Se requiere la creación de los siguientes agentes especializados, cada uno responsable de una fase clave:

### 1. Agente de Análisis de Reglamentos Generales (RulesEngine Agent)

**Objetivo:** Leer y procesar el documento PDF del reglamento general (`docs/Rules`).
**Tareas Clave:**

* Inferir el modelo de datos canónico para unidades, armas, habilidades y estratagemas.
* Desarrollar la lógica algorítmica fundamental para el cálculo de daño (Daño Base * Modificadores de Habilidad + Bonificaciones de Equipo).
* Establecer las reglas de negocio que rigen la interacción entre diferentes mecánicas del juego.

### 2. Agente de Procesamiento de Listas de Ejército (ArmySheet Agent)

**Objetivo:** Consumir los datos JSON del repositorio `wh40k-11e` y mapearlos al modelo canónico.
**Tareas Clave:**

* Mapear estructuras JSON a las clases de dominio definidas en la Fase 1.
* Validar la integridad de los datos importados contra el reglamento general.
* Crear un *parser* eficiente para manejar grandes volúmenes de listas de forma escalable.

### 3. Agente Integrador y Modelador de Datos (DataIntegrator Agent)

**Objetivo:** Crear una capa de abstracción que permita la lectura, actualización y combinación segura de datos de múltiples fuentes (PDFs, JSONs).
**Tareas Clave:**

* Implementar el ORM/DAL para acceder a los datos estructurados.
* Gestionar versiones de esquemas ante actualizaciones del juego.
* Proveer una API unificada para que otros agentes accedan a la información sin conocer su origen (JSON vs PDF).

### 4. Agente de Generación de Lógica y Cálculo (SimulationAgent)

**Objetivo:** Ejecutar los algoritmos complejos de simulación y generación de listas.
**Tareas Clave:**

* Generar las clases de ejecución que reciben una lista validada y calculan:
  * Todas las combinaciones posibles de armamento y habilidades para la unidad.
  * El daño potencial total contra un objetivo específico (otro codex), considerando sinergias y penalizaciones.
  * La lógica para generar listas completas cumpliendo con restricciones de puntos y reglas.

### 5. Agente de Interfaz Web (WebUI Agent)

**Objetivo:** Crear una aplicación web interactiva para la visualización y comparación de resultados.
**Tareas Clave:**

* Desarrollar el *frontend* utilizando un framework moderno (React/Vue).
* Implementar la funcionalidad de carga de listas desde NewRecruit y su visualización comparativa (comparación de daño entre listados).
* Conectar el *backend* a la API del `DataIntegrator Agent`.

### 6. Agente de Ingesta Continua (UpdateAgent)

**Objetivo:** Automatizar la actualización de la base de datos cuando cambien las fuentes externas.
**Tareas Clave:**

* Monitorear los directorios `docs/Rules` y el repositorio JSON.
* Ejecutar *pipelines* automatizados: [New Data] -> [DataIntegrator Agent] -> [Validation/Test].

## Estructura de Carpetas (Propuesta)

```text
C:\Users\Usuario\source\repos\Selinux24\WH40k
├── Docs/
│   └── Rules/ (PDF del reglamento general, actualizado periódicamente)
├── Code/ (Contendrá toda la codificación necesaria del proyecto)
│   ├── src/
│   │   ├── core/          # Algoritmos de daño y lógica central
│   │   ├── data/          # Modelos de datos e integradores (DataIntegrator Agent output)
│   │   ├── services/      # Servicios de procesamiento (SimulationAgent output)
│   │   └── web/           # Componentes de la interfaz web (WebUI Agent output)
│   └── tests/             # Pruebas unitarias y de integración
└── .github/agents/        # Contendrá los skills, instrucciones y scripts para cada agente.
    ├── ArmySheetAgent/
    │   ├── instructions.md
    │   └── skills.json
    ├── DataIntegratorAgent/
    │   ├── instructions.md
    │   └── skills.json
    ├── RulesEngineAgent/
    │   ├── instructions.md
    │   └── skills.json
    ├── SimulationAgent/
    │   ├── instructions.md
    │   └── skills.json
    ├── WebUIAgent/
    │   ├── instructions.md
    │   └── skills.json
    └── UpdateAgent/
        ├── instructions.md
        └── skills.json
```
