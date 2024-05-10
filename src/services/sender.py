import asyncio
from email.message import EmailMessage

from fastapi import HTTPException, status

from src.config import settings
import smtplib
from src.db.db import database

from pyrogram import Client

from src.services.operations import create_message


async def send_email(subject, text, time_sleep, user_ip):
    user = database.get(user_ip)
    if user:
        users = user.get("users")
        await asyncio.sleep(time_sleep)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:

            if user.get("email") and user.get("app_pass"):
                try:
                    server.login(user.get("email"), user.get("app_pass"))
                except Exception as e:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Не правильно заданы email или пароль приложения")
            else:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
            async for info in users:
                email = EmailMessage()
                email["From"] = settings.SMTP_USER if not (user.get("email") and user.get("app_pass")) else user.get(
                    "email")
                if info:
                    email["To"] = info[0]
                    email["Subject"] = subject

                    message = await create_message(text)
                    email.set_content(message)
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не правильно заданы данные")
                try:
                    server.send_message(email)
                    await asyncio.sleep(1)
                except Exception as ex:
                    pass


async def send_telegram(text, time_sleep, user_ip):
    user = database.get(user_ip)
    if user:
        users = user.get("users")
        await asyncio.sleep(time_sleep)
        api_id = user.get("api_id")
        api_hash = user.get("api_hash")
        phone = user.get("telegram")
        if api_id and api_hash and phone:
            async with Client(name=str(api_id), api_id=api_id, api_hash=api_hash, phone_number=phone) as client:
                async for info in users:
                    try:
                        message = await create_message(text)
                        await client.send_message(chat_id=info[0], text=message)
                        await asyncio.sleep(1)
                    except Exception as ex:
                        pass
        else:
            async with Client(name="botchat", api_id=settings.API_ID, api_hash=settings.API_HASH) as client:
                async for info in users:
                    try:
                        message = await create_message(text)
                        await client.send_message(chat_id=info[0], text=message)
                        await asyncio.sleep(1)
                    except Exception as ex:
                        pass


async def send_insta(message, time_sleep, user_ip):
    pass
    # proxy_host = "38.152.247.115"
    # proxy_port = "9534"
    # proxy = Proxy()
    # proxy.proxy_type = ProxyType.MANUAL
    # proxy.http_proxy = f"{proxy_host}:{proxy_port}"
    # proxy.ssl_proxy = f"{proxy_host}:{proxy_port}"
    #
    # # Настройка параметров запуска Chrome
    # chrome_options = Options()
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--proxy-server=http://{}:{}'.format(proxy_host, proxy_port))
    # driver = webdriver.Chrome(options=chrome_options)
    # driver.get("https://www.instagram.com")
    # time.sleep(50)


async def send_whatsapp(message, time_sleep, user_ip):
    pass


async def send_sms(text, time_sleep, user_ip):
    import requests
    url = 'https://sms.notisend.ru/api/message/send'
    user = database.get(user_ip)
    if user:
        users = user.get("users")
        await asyncio.sleep(time_sleep)

        for info in users:
            params = {
                'project': 'sendersmser',
                'recipients': info[0],
                'message': text,
                'apikey': '133deb0cbe5368f892b4a80c8cdd3306'
            }

            response = requests.post(url, data=params)

            if response.status_code == 200:
                print("SMS успешно отправлено!")
            else:
                print("Ошибка при отправке SMS:", response.text)
