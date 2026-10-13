# Contrato de API para DataIntegratorAgent (v1.0)

Este archivo define el contrato de datos que debe ser respetado por todos los agentes subsiguientes y es la interfaz pública del sistema.

## 1. Estructura Unificada de Unidad
Debe contener, como mínimo: ID, Nombre, Codex, Puntos Base.

## 2. Mapeo de Armas (Weapon Mapping)
Cada unidad debe tener un array de armas asociadas con su `weapon_id` y los detalles del arma recuperados del RulesEngineAgent.

## 3. Datos Integrados de Listas
Debe proporcionar una lista serializada que contenga la combinación validada de todas las unidades, sus equipos y el total de puntos gastados.

**Función Clave:** `get_validated_army_list(json_path: str) -> list[UnitSchema]`

*Nota:* Este contrato asegura que los algoritmos (SimulationAgent) solo trabajen con datos ya validados y limpios, desacoplando la capa de persistencia de la lógica de negocio.