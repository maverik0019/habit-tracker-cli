from storage import load_users, save_users
from model import User

LOCAL_USER = "local"

def show_menu():

    print("")

    print("======================================")
    print("        HABIT TRACKER")
    print("======================================")

    print("1. Add habit")
    print("2. Mark today's habit")
    print("3. View today's habits")
    print("4. View streaks")
    print("5. List all habits")
    print("6. Delete habit")
    print("0. Exit")

def get_user(users):
    """Return the local user. If it is the first time, ask for the name."""

    if LOCAL_USER not in users:
        name = input("Hello, what is your name? ").strip()
        if not name:
            name = "Anonymous"

        users[LOCAL_USER] = User(LOCAL_USER, name)
    return users[LOCAL_USER]

def command_add(user):
    name = input("Habit name: ").strip()
    if not name:
        print("Warning: the name cannot be empty")
        return
    try:
        user.add_habit(name)
        print("Done. Habit '" + name.lower() + "' added")
    except ValueError as error:
        print("Warning: " + str(error))

def command_check(user):
    if not user.habits:
        print("Warning: you do not have any habits yet. Add one first.")
        return
    name = input("Which habit did you complete? ").strip()

    if not name:
        print("Warning: empty name")
        return
    try:
        message = user.check(name)
        print(message)
    except KeyError as error:

        print("Warning: " + str(error))

def command_today(user):
    if not user.habits:
        print("You do not have any habits registered yet.")
        return
    print("")
    print("Today's habits (" + user.nombre + "): ")

    for name, habit in user.habits.items():
        status = "[X]" if habit.done_today() else "[ ]"
        print(" " + status + " " + name)

def command_streaks(user):
    if not user.habits:
        print("You do not have any habits registered yet.")
        return
    print("")
    print("Current streaks:")
    for name, habit in user.habits.items():
        print(" " + name + ": " + str(habit.streak()) + " days")

def command_list(user):
    if not user.habits:
        print("You do not have any habits registered yet.")
        return

    print("")
    print("All your habits:")

    for name, habit in user.habits.items():
        total = len(habit.checks)
        print(
            " - " + name +
            " (created: " + habit.created + ", " +
            "total checks: " + str(total) + ")"
        )
def command_delete(user):
    if not user.habits:
        print("You do not have any habits to delete.")
        return
    name = input("Which habit do you want to delete? ").strip()
    if not name:
        print("Warning: empty name")
        return
    if user.delete_habit(name):
        print("Done. Habit '" + name.lower() + "' deleted")
    else:
        print("Warning: that habit was not found")

def main():

    users = load_users()
    user = get_user(users)

    while True:
        show_menu()
        option = input("Option: ").strip()
        if option == "1":
            command_add(user)
        elif option == "2":
            command_check(user)
        elif option == "3":
            command_today(user)
        elif option == "4":
            command_streaks(user)
        elif option == "5":
            command_list(user)
        elif option == "6":
            command_delete(user)
        elif option == "0":
            save_users(users)
            print("See you tomorrow.")
            break
        else:
            print("Warning: invalid option")
        save_users(users)

if __name__ == "__main__":

    main()