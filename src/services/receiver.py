from fastapi import APIRouter, UploadFile, Request

from src.models.data import Data
from src.services.operations import check_file, convert_time
from src.services.sender import send_email, send_telegram, send_sms, send_insta, send_whatsapp

router = APIRouter(prefix="/receive")


@router.post('')
async def get_data(data: Data, request: Request):
    time_sleep = await convert_time(data.datetime)

    if data.channel == "email":
        await send_email(subject=data.subject, text=data.message, user_ip=request.client.host, time_sleep=time_sleep)
    if data.channel == "telegram":
        await send_telegram(text=data.message, user_ip=request.client.host, time_sleep=time_sleep)
    # if data.channel == "instagram":
    #     await send_insta(message=data.message, user_ip=request.client.host, time_sleep=time_sleep)
    # if data.channel == "whatsapp":
    #     await send_whatsapp(message=data.message, user_ip=request.client.host, time_sleep=time_sleep)
    if data.channel == "sms":
        await send_sms(text=data.message, user_ip=request.client.host, time_sleep=time_sleep)


@router.post('/upload')
async def get_len_users(file: UploadFile, request: Request):
    try:
        len_users = await check_file(file, request.client.host)
        return len_users

    except Exception as e:
        print(e)
