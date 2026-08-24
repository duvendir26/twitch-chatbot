import json

USERS_FILE = "data/users.json"


def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def add_user(username):
    users = load_users()

    if not any(user["username"] == username for user in users):
        users.append({
            "username": username,
            "hp": 100,
            "armor": 0,
            "strength": 1,
            "balance": 0,
            "coinflip_wins": 0,
            "coinflip_losses": 0,
            "coinflip_biggest_win": 0,
            "coinflip_biggest_loss": 0,
            "last_daily": 0
        })

        save_users(users)


def get_user(username):
    users = load_users()

    for user in users:
        if user["username"] == username:
            return user
        
    add_user(username)

    return get_user(username)


def set_user(username, user_data):
    users = load_users()

    for i, user in enumerate(users):
        if user["username"] == username:
            users[i] = user_data
            break

    save_users(users)