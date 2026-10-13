from flask import Flask, request, jsonify
from src.services.combat_engine import calculate_combat_damage

app = Flask(__name__)

@app.route('/api/calculate-combat', methods=['POST'])
def calculate_combat():
    """
    API endpoint to receive two army lists and return a combat report.
    Expects JSON body: {"army1": "list...", "army2": "list..."}
    """
    data = request.get_json()

    if not data or 'army1' not in data or 'army2' not in data:
        return jsonify({"error": "Missing army lists. Requires JSON body with 'army1' and 'army2'."}), 400

    army_list1 = data['army1']
    army_list2 = data['army2']

    try:
        # Call the core business logic function
        report = calculate_combat_damage(army_list1, army_list2)
        return jsonify({"status": "success", "report": report})
    except Exception as e:
        print(f"Error during combat calculation: {e}")
        return jsonify({"error": f"An internal error occurred while calculating combat damage: {str(e)}"}), 500

if __name__ == '__main__':
    # Note: In a real deployment, use gunicorn/waitress instead of app.run()
    app.run(debug=True, port=5000)