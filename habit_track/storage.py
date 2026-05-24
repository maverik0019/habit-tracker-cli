import json
from pathlib import Path
from model import User, Habit

DATA_FILE = Path(__file__).parent.parent / "data" / "users.json"

def load_users():
    """read the JSON file and rebuild the object User and Habit"""

    if not DATA_FILE.exists():
        return {}
    
    try:
        with open(DATA_FILE, "r" , encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Warning:The data file is corrupt. Starting from scratch")
        return {}
    
    users = {}

    for user_id, info in data.items():
        user = User(
            user_id=user_id,
            nombre=info.get("nombre", "Anonimo")
        )

        for name_habit, habit_data in info.get("habits", {}).items():
            habit = Habit(name_habit)

            habit.created = habit_data["created"]
            habit.checks = habit_data["checked"]
            user.habits[name_habit] = habit
        users[user_id] = user
    return users

def save_users(users):
    """Convierte los objetos a diccionario plano y los escribe en JSON.
    `indent=2` makes the JSON readable. `ensure_ascii=False` allows accented characters."""

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {}

    for user_id, user in users.items():
        data[user_id] = {
            "nombre": user.nombre,
            "habits": {
                name: {
                    "created" : habit.created,
                    "checked" : habit.checks, 
                }
                for name, habit in user.habits.items()
            },
        }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)