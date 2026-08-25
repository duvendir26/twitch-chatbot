# Users can send keks to eachother
# Make sure the user is in the user list
# Only $kek command adds new users

from utils.users import load_users, set_user


async def cmd_send(username, reply, args=None):
    print(f"@{username} requested send command with args: {args}")

    if not args or len(args) < 2:
        await reply(f"@{username} Usage: $send <recipient> <amount>")
        return

    recipient = args[0].lstrip('@')
    try:
        amount = int(args[1])
    except ValueError:
        await reply(f"@{username} Invalid amount. Please enter a valid number.")
        return

    if amount <= 0:
        await reply(f"@{username} Amount must be greater than zero.")
        return

    users = load_users()
    user = next((u for u in users if u['username'].lower() == username.lower()), None)
    if not user:
        await reply(f"@{username} You are not registered. Use $kek to register KEKP")
        return
    
    recipient_user = next((u for u in users if u['username'].lower() == recipient.lower()), None)
    if not recipient_user:
        await reply(f"@{username} User is not registered (use $kek) wideKEKA")
        return

    if user['balance'] < amount:
        await reply(f"@{username} You do not have enough keks to send.")
        return

    user['balance'] -= amount
    recipient_user['balance'] += amount
    
    set_user(user['username'], user)
    set_user(recipient_user['username'], recipient_user)

    await reply(f"@{username} sent {amount} 🍪 to @{recipient}.")