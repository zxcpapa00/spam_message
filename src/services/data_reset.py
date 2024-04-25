from src.db.db import database


async def reset_email(email, app_pass, user_ip):
    user = database.get(user_ip)
    user["email"] = email
    user["app_pass"] = app_pass


async def reset_telegram():
    pass
