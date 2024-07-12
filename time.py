import os
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from PIL import Image
from telethon.tl.functions.photos import UploadProfilePhotoRequest, UpdateProfilePhotoRequest
from update_photo_with_time import new_photo
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE')
session_file_path = "Telegram.session"

client = TelegramClient(session_file_path, api_id, api_hash)

async def update_profile_picture():
    if os.path.exists(session_file_path):
        print("Session file exists.")
    else:
        print("Session file does not exist.")
        await client.start(phone_number)
    # Replace with the path to your image file
    is_first = True
    while True:
        now = datetime.now()
        seconds_to_next_minute = 60 - now.second
        next_minute_time = now + timedelta(seconds=seconds_to_next_minute)
        current_time = next_minute_time.strftime("%H:%M")
        current_date = now.strftime("%d.%m.%Y")
        image_path = new_photo(current_time)

        # Open and resize the image if needed
        image = Image.open(image_path)
        image = image.resize((512, 512))  # Resize to 512x512 if needed
        image.save(image_path)  # Save the resized image

        file = await client.upload_file(image_path)  # Upload the image file
        await client(UploadProfilePhotoRequest(fallback=True, file=file))  # Update profile picture
        print("Profile picture updated successfully")
        bio = f"⌚️ | {current_time} | 📆 | {current_date}"
        await client(UpdateProfileRequest(about=bio))
        print(f"Updated bio to: {bio}")
        if is_first:
            await asyncio.sleep(60 - datetime.now().second - 5)
            is_first = False
            continue
        await asyncio.sleep(60)

with client:
    client.loop.run_until_complete(update_profile_picture())
