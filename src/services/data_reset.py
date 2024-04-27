from pyrogram import Client

from src.db.db import database
from fastapi import HTTPException, status


async def reset_email(email, app_pass, user_ip):
    user = database.get(user_ip)
    if email and app_pass:
        user["email"] = email
        user["app_pass"] = app_pass
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не заданы данные")


async def reset_telegram(phone, api_id, api_hash, code_, user_ip):
    user = database.get(user_ip)
    if phone and api_id and api_hash:
        user["telegram"] = phone
        user["api_id"] = api_id
        user["api_hash"] = api_hash
        send_code = user["code"]
        client = user["client_telegram"]

        try:
            await client.sign_in(phone, send_code.phone_code_hash, code_)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка данных")
        finally:
            await client.disconnect()

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не заданы данные")


async def get_phone_code(phone, api_id, api_hash, user_ip):
    user = database.get(user_ip)
    try:
        client = Client(name=str(api_id), api_id=api_id, api_hash=api_hash, phone_number=phone)
        await client.connect()
        send_code = await client.send_code(phone)
        user["code"] = send_code
        user["client_telegram"] = client
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Данные неверны")
