# Plan de Proyecto: Analizador Avanzado de Reglas Warhammer 40k

## Objetivo General

Crear un sistema integral capaz de analizar las reglas completas de Warhammer 40k, procesando múltiples fuentes de documentación (reglamento general, libros de ejército, revisiones de puntos, Q&A) para generar una lista detallada y calculada de posibles configuraciones de armamento para cualquier lista de ejército. El resultado debe incluir un análisis exhaustivo del daño potencial que la lista puede infligir contra unidades de otros codex, considerando habilidades, estratagemas y equipamiento.

## Estrategia de Contexto Grande

Dado el gran volumen y la naturaleza evolutiva de los documentos (actualizaciones periódicas), se implementará una estrategia modular:

1. **Modelo de Datos Centralizado:** Definir un esquema de datos robusto e inmutable que sirva como fuente única de verdad para todas las unidades, armas y reglas. Deberá inferirse a partir de las reglas generales de Warhammer 40K, que están escritas en PDF dentro de la carpeta Docs/Rules
2. **Ingesta por Componentes:** Desarrollar módulos de ingesta específicos (JSON para listas, PDF/TXT parsers para reglamentos) en lugar de depender de una sola lectura masiva.
3. **Base de Conocimiento Vectorial (Recomendado):** Utilizar un sistema de base de datos vectorial o graph database para indexar el texto completo y las reglas, permitiendo búsquedas semánticas que no agotan el contexto lineal del modelo.

## Tareas de Desarrollo y Agentes Requeridos

Se requiere la utilización de los siguientes agentes especializados, cada uno responsable de una fase clave:

### 1. Ingesta de reglas: RulesEngine Agent

**Objetivo:** Leer y procesar el documento PDF del reglamento general (`docs/Rules`).
**Tareas Clave:**

* Inferir el modelo de datos canónico para unidades, armas, habilidades y estratagemas.
* Desarrollar la lógica algorítmica fundamental para el cálculo de daño (Daño Base * Modificadores de Habilidad + Bonificaciones de Equipo).
* Establecer las reglas de negocio que rigen la interacción entre diferentes mecánicas del juego.

### 2. Ingesta de listas de ejército: ArmySheet Agent

**Objetivo:** Consumir los datos JSON de las listas de ejército en el direction Docs/Codex y mapearlos al modelo canónico.
**Tareas Clave:**

* Mapear estructuras JSON a las clases de dominio definidas en la Fase 1.
* Validar la integridad de los datos importados contra el reglamento general.
* Crear un *parser* eficiente para manejar grandes volúmenes de listas de forma escalable.

### 3. Librería de Integración de datos: DataIntegrator Agent

**Objetivo:** Crear una capa de abstracción que permita la lectura, actualización y combinación segura de datos de múltiples fuentes (PDFs, JSONs).
**Tareas Clave:**

* Implementar el ORM/DAL para acceder a los datos estructurados.
* Gestionar versiones de esquemas ante actualizaciones del juego.
* Proveer una API unificada para que otros agentes accedan a la información sin conocer su origen (JSON vs PDF).

### 4. Librería de de Lógica y Cálculo: SimulationAgent

**Objetivo:** Ejecutar los algoritmos complejos de simulación y generación de listas.
**Tareas Clave:**

* Generar las clases de ejecución que reciben una lista validada y calculan:
  * Todas las combinaciones posibles de armamento y habilidades para la unidad.
  * El daño potencial total contra un objetivo específico (otro codex), considerando sinergias y penalizaciones.
  * La lógica para generar listas completas cumpliendo con restricciones de puntos y reglas.

### 5. Implementación de la Web: WebUI Agent

**Objetivo:** Crear una aplicación web interactiva para la visualización y comparación de resultados.
**Tareas Clave:**

* Desarrollar el *frontend* utilizando un framework moderno (React/Vue).
* Implementar la funcionalidad de carga de listas desde base de datos y su visualización comparativa (comparación de daño entre listados).
* Conectar el *backend* a la API de la librería de integración de datos.

### 6. Proceso de Ingesta Continua: UpdateAgent

**Objetivo:** Automatizar la actualización de la base de datos cuando cambien las fuentes externas.
**Tareas Clave:**

* Monitorear los directorios `docs/Rules` y `docs/Codex`.
* Ejecución manual: [New Data] -> [DataIntegrator Agent] -> [Validation/Test].

## Entregables

* La programación de la ingesta de datos, la integración con la base de datos, y el motor de cálculo de las simulaciones, debe realizarse en PYTHON
* La base de datos deberá ser ChromaDB.
* La web debera estar contenida en una carpeta única, de forma que pueda copiarse a cualquier parte y lanzarse desde cualquier explorador.
* La implementación de la web deberá utilizar REACT.

## Estructura de Carpetas (Propuesta)

```text
C:\Users\Usuario\source\repos\Selinux24\WH40k
├── Docs/
│   ├── Rules/ (PDF del reglamento general, actualizado periódicamente)
│   └── Codex/ (Listas de ejército en formato JSON)
├── Code/ (Contendrá toda la codificación necesaria del proyecto)
│   ├── src/
│   │   ├── core/          # Algoritmos de daño y lógica central
│   │   ├── data/          # Modelos de datos e integradores (DataIntegrator Agent output)
│   │   ├── services/      # Servicios de procesamiento (SimulationAgent output)
│   │   └── web/           # Componentes de la interfaz web (WebUI Agent output)
│   └── tests/             # Pruebas unitarias y de integración
└── .github/agents/        # Contendrá los agentes
    └── skills/            # Contendrá los skills
```

## Metodología de Trabajo

Realiza las tareas de forma autónoma. Si hay alguna duda toma tú las decisiones y déjalo anotado en el documento NOTES.md

Trabaja en bucle: Planifica, construye, revisa, corrige y repite. No me entregues el primer resultado.
Usa un árbitro que emplee técnicas adversariales para auditar y criticar el trabajo hecho, que no haya participado en su construcción, y que busque fallos a propósito como si quisiera tumbarlo. Sigue mejorando hasta que lo dé por bueno.

El árbitro no dará el trabajo por bueno hasta que se cumplan estos puntos:

* Existe una base de datos con información cargada a partir de las reglas y el contenido de `docs/Codex`
* Existe una web que permite cargar dos listas de ejército desde la base de datos y realizar una comparación
* La comparación realiza un cruce de cada arma y cada unidad de una lista, contra las unidades de la otra lista
* Cada comparación permite seleccionar al usuario dinámicamente, habilidades especiales y estratagemas disponibles para la situación
