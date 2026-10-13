
import sqlite3
from typing import List, Dict, Any

DATABASE_NAME = "warhammer40k.db"

def get_connection():
    """Establishes and returns a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)

def initialize_database():
    """Creates all necessary tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Units Table: Core entity for characters/creatures
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS units (
            unit_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            faction TEXT,
            model_type TEXT, -- e.g., Infantry, Vehicle, Monster
            wargear_capacity INTEGER DEFAULT 0,
            description TEXT
        );
    """)

    # 2. Weapons Table: Defines weapon types and base stats
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weapons (
            weapon_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            damage_base REAL NOT NULL, -- Base damage value
            range_type TEXT,          -- e.g., Melee, Short, Long
            ammo_requirement INTEGER DEFAULT 0,
            synergy_tags TEXT         -- Comma-separated tags for synergy checks (e.g., 'anti-armor')
        );
    """)

    # 3. Abilities Table: Special powers or skills
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abilities (
            ability_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            effect_type TEXT,       -- e.g., Buff, Debuff, Utility
            prerequisite_unit_id TEXT, -- Null if general ability
            FOREIGN KEY (prerequisite_unit_id) REFERENCES units(unit_id)
        );
    """)

    # 4. Equipment Table: Items carried or equipped (can be a weapon or support gear)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            equipment_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,     -- e.g., Weapon, Armor, Utility
            damage_modifier REAL DEFAULT 0.0, -- Modifier to base damage if it's a weapon
            required_unit_model TEXT  -- Optional constraint for equipment use
        );
    """)

    # 5. Stratagems Table: Tactical options available during combat phases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stratagems (
            stratagem_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            resource_cost INTEGER NOT NULL, -- E.g., Command Points
            effect_details TEXT             -- Detailed effect logic description
        );
    """)

    # Junction Tables for many-to-many relationships (e.g., Unit has multiple Weapons/Abilities)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unit_equipment (
            unit_id TEXT,
            equipment_id TEXT,
            PRIMARY KEY (unit_id, equipment_id),
            FOREIGN KEY (unit_id) REFERENCES units(unit_id),
            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unit_abilities (
            unit_id TEXT,
            ability_id TEXT,
            PRIMARY KEY (unit_id, ability_id),
            FOREIGN KEY (unit_id) REFERENCES units(unit_id),
            FOREIGN KEY (ability_id) REFERENCES abilities(ability_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unit_weapons (
            unit_id TEXT,
            weapon_id TEXT,
            PRIMARY KEY (unit_id, weapon_id),
            FOREIGN KEY (unit_id) REFERENCES units(unit_id),
            FOREIGN KEY (weapon_id) REFERENCES weapons(weapon_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unit_stratagems (
            unit_id TEXT,
            stratagem_id TEXT,
            PRIMARY KEY (unit_id, stratagem_id),
            FOREIGN KEY (unit_id) REFERENCES units(unit_id),
            FOREIGN KEY (stratagem_id) REFERENCES stratagems(stratagem_id)
        );
    """)

    conn.commit()
    conn.close()
    print("Database schema initialized successfully.")

# --- CRUD OPERATIONS SERVICE MODULE ---

def create_unit(unit_data: Dict[str, Any]) -> str:
    """Creates a new Unit record and returns the unit_id."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO units (unit_id, name, faction, model_type, wargear_capacity, description) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            unit_data['unit_id'],
            unit_data['name'],
            unit_data.get('faction', 'Unknown'),
            unit_data.get('model_type', 'Generic'),
            unit_data.get('wargear_capacity', 0),
            unit_data.get('description', '')
        ))
        conn.commit()
        return unit_data['unit_id']
    except sqlite3.IntegrityError:
        return f"Error: Unit with ID {unit_data.get('unit_id')} already exists."
    finally:
        conn.close()

def get_unit(unit_id: str) -> Dict[str, Any] | None:
    """Retrieves a unit by its unique ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM units WHERE unit_id = ?", (unit_id,))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    finally:
        conn.close()

def add_weapon_to_unit(unit_id: str, weapon_id: str) -> bool:
    """Links an existing weapon to a unit."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO unit_weapons (unit_id, weapon_id) VALUES (?, ?)
        """, (unit_id, weapon_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # This handles cases where the relationship already exists or IDs are invalid
        print("Warning: Relationship might already exist or IDs are invalid.")
        return False
    finally:
        conn.close()

def list_all_units() -> List[Dict[str, Any]]:
    """Retrieves a list of all units."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM units")
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    finally:
        conn.close()

if __name__ == "__main__":
    # Example usage demonstrating the full workflow
    initialize_database()

    # 1. Create core entities (Units, Weapons, Stratagems)
    print("\\n--- Populating Core Entities ---")
    
    // Unit Data
    marine_id = create_unit({
        'unit_id': 'SM-001', 
        'name': 'Space Marine Vanguard', 
        'faction': 'Imperium', 
        'model_type': 'Infantry', 
        'wargear_capacity': 3,
        'description': 'Veteran shock trooper.'
    })
    print(f"Created Unit: {marine_id}")

    // Weapon Data
    bolter_id = "WPN-BOLT"
    if not get_unit('SM-001'): # Check if unit creation failed for demonstration purposes
        # Create a dummy weapon first to ensure the example runs
        cursor = get_connection().cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO weapons (weapon_id, name, damage_base, range_type) 
            VALUES (?, ?, ?, ?)
        """, ('WPN-BOLT', 'Bolt Rifle', 3.0, 'Long'))
        get_connection().commit()

    # Link weapon to unit
    add_weapon_to_unit('SM-001', bolter_id)
    print("Linked Bolt Rifle to Space Marine Vanguard.")
    
    # 2. Retrieve and verify data (Read Operation)
    print("\\n--- Reading Data ---")
    marine = get_unit('SM-001')
    if marine:
        print(f"Successfully retrieved Unit: {marine['name']} ({marine['unit_id']})")

    all_units = list_all_units()
    print(f"Total units in database: {len(all_units)}")