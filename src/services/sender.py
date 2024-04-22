import asyncio
from email.message import EmailMessage

from src.config import settings
import smtplib
from src.db.db import database

from pyrogram import Client

from src.services.operations import create_message


async def send_email(subject, text, time_sleep, user_ip):
    users = database[user_ip]
    await asyncio.sleep(time_sleep)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        for info in users:
            email = EmailMessage()
            email["From"] = settings.SMTP_USER
            email["To"] = info[1]
            email["Subject"] = subject

            message = await create_message(info[0], text)
            email.set_content(message)
            try:
                server.send_message(email)
                await asyncio.sleep(1)
            except Exception as ex:
                print(f"Ошибка отправки email на {info[1]}")


async def send_telegram(text, time_sleep, user_ip):
    users = database[user_ip]
    await asyncio.sleep(time_sleep)

    async with Client(name="botchat", api_id=settings.API_ID, api_hash=settings.API_HASH) as client:
        for info in users:
            try:
                message = await create_message(info[0], text)
                await client.send_message(chat_id=info[1], text=message)
                await asyncio.sleep(1)
            except Exception as ex:
                print(f"Ошибка отправки на телеграм {info[1]}")


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
    users = database[user_ip]
    await asyncio.sleep(time_sleep)

    for info in users:
        params = {
            'project': 'sendersmser',
            'recipients': f'{info[1]}',
            'message': f'Привет {info[0]} '
                       f'\n{text}',
            'apikey': '133deb0cbe5368f892b4a80c8cdd3306'
        }

        response = requests.post(url, data=params)

        if response.status_code == 200:
            print("SMS успешно отправлено!")
        else:
            print("Ошибка при отправке SMS:", response.text)
