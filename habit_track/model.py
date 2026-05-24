from datetime import date, timedelta


class Habit:
    """creation of habit for the dayly task"""

    def __init__(self,name):
        self.name = name.strip().lower()
        self.created = date.today().isoformat()
        self.checks = []

    def mark_today(self):
        """mark the task done for the current day"""

        today = date.today().isoformat()
        if today in self.checks:
            return False
        self.checks.append(today)
        return True

    def done_today(self):
        """return True if the task was marked"""
        return date.today().isoformat() in self.checks
    
    def streak(self):
        """Calculate the consecutive days till today"""
        if not self.checks:
            return 0
        
        fechas = sorted(
            [date.fromisoformat(c) for c in self.checks],
            reverse=True
        )

        hoy =  date.today()
        ayer = hoy - timedelta(days=1)
        mas_reciente = fechas[0]

        if mas_reciente == hoy:
            esperando = hoy
        elif mas_reciente == ayer:
            esperando = ayer

        else:
            return 0
        
        streak = 0
        for fecha in fechas:
            if fecha == esperando:
                streak = streak + 1
                esperando = esperando - timedelta(days=1)
            else:
                break

        return streak
    
class User:
    """Represetn a user and his activity across the tracker"""
    def __init__(self, user_id, nombre="Anonimo"):
        self.user_id = user_id
        self.nombre = nombre
        self.habits = {}
    
    def add_habit(self, name):
        """create a new habit"""
        clean_name = name.lower().strip()

        if not clean_name:
            raise ValueError("The habit name cant be empty")
        if clean_name in self.habits:
            raise ValueError("The habit '" + clean_name + "' already exists")
        
        habit = Habit(clean_name)
        self.habits[clean_name] = habit
        return habit
    
    def delete_habit(self, name):
        """Returns True if deleted, False if did not exist. Does not throw an exception"""
        clean_name = name.lower().strip()
        if clean_name not in self.habits:
            return False
        del self.habits[clean_name]
        return True
    
    def check(self, name):
        """Mark one habit as completed today. Return text message"""
        clean_name = name.lower().strip()

        if clean_name not in self.habits:
            raise KeyError("You don't have the habit '" + clean_name + "'")
        habit = self.habits[clean_name]


        if habit.mark_today():
            return (
                "Marked '" + clean_name + "'."
                " Current streak: " + str(habit.streak()) + " days"
            )
        return "You already marked '" + clean_name + "' today."



        
