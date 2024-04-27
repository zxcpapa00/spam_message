import csv
from datetime import datetime
from io import StringIO
from src.db.db import database


async def check_file(file, user_ip):
    contents = await file.read()
    csv_data = contents.decode('cp1251')
    csv_stream = StringIO(csv_data)
    csv_reader = csv.reader(csv_stream, delimiter=";")

    csv_contents = [row for row in csv_reader]
    database[user_ip]["users"] = csv_contents
    return len(csv_contents)


async def convert_time(time):
    date_format = "%Y-%m-%dT%H:%M"
    time = datetime.strptime(time, date_format)
    time_sleep = time - datetime.now()
    return time_sleep.total_seconds()


async def create_message(message):
    text = message
    return text
