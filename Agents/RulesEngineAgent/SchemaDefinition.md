# Schema de Datos Canónico (Propuesto por RulesEngine Agent)

Este esquema se definirá y refinará tras el análisis completo del PDF, pero sirve como punto de partida para estructurar la base de conocimiento.

## 1. Unidad (Unit)
*   **ID:** Código único de la unidad.
*   **Nombre:** Nombre legible en el juego.
*   **Codex:** A qué facción pertenece.
*   **Puntos Base:** Costo de puntos estándar.
*   **Equipo Base:** Lista predeterminada de armamento y habilidades.

## 2. Arma (Weapon)
*   **ID:** Código único del arma.
*   **Daño Base:** Valor numérico base de daño (e.g., 3).
*   **Tipo de Daño:** Cortante, Láser, Plasma, etc.
*   **Alcance:** Distancia máxima de combate.
*   **Peligro:** Si el ataque es peligroso.

## 3. Habilidad/Estratagema (Ability/Stratagem)
*   **Tipo:** Activa o Pasiva.
*   **Requisito:** Condiciones para activar (ej: debe haber unidades a X distancia).
*   **Efecto:** Modificador aplicado al combate (ej: +1 de daño, Ignorar armadura).
*   **Costo:** Puntos necesarios para usarla.

## 4. Fórmula de Daño (Damage Formula)
El cálculo general será una combinación ponderada:
`Daño Final = MAX(Daño Base * Modificador_Habilidad - Mitigación_Objetivo, Umbral_Mínimo)`

*   **Modificadores:** Son acumulativos y se aplican en el momento del combate.
*   **Mitigación/Armadura:** Valores que reducen el daño final.