from fastapi import APIRouter, UploadFile, Request

from src.db.db import database
from src.models.data import Data
from src.services.data_reset import reset_email, reset_telegram, get_phone_code
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


@router.post('/res_email')
async def res_email(request: Request):
    data = await request.json()
    await reset_email(data.get("email"), data.get("app_pass"), request.client.host)


@router.post('/res_telegram')
async def res_telegram(request: Request):
    data = await request.json()
    await reset_telegram(data.get("phone"), data.get("api_id"), data.get("api_hash"), data.get("code_"),
                         request.client.host)


@router.post('/get_code')
async def get_code(request: Request):
    data = await request.json()
    await get_phone_code(data.get("phone"), data.get("api_id"), data.get("api_hash"), request.client.host)


@router.post('/upload')
async def get_len_users(file: UploadFile, request: Request):
    try:
        len_users = await check_file(file, request.client.host)
        return len_users

    except Exception as e:
        print(e)
