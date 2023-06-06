import os
import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto

def save_image_from_bytes(image_bytes, filename):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'wb') as file:
        file.write(image_bytes)

def scrape_telegram_channel(api_id, api_hash, phone_number, channel_username, limit):
    # Create a TelegramClient object and authenticate
    client = TelegramClient('session_name', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))

    # Get the channel entity
    entity = client.get_entity(channel_username)

    # Retrieve the messages from the channel
    messages = client.get_messages(entity, limit=limit)

    data = []
    for message in messages:
        text = message.text
        date = message.date
        image_bytes = None
        image_path = None

        if isinstance(message.media, MessageMediaPhoto):
            photo = message.photo
            if photo is not None:
                image_bytes = client.download_media(photo, bytes)
                if image_bytes is not None:
                    image_path = f'images/{message.id}.jpg'  # Assuming you want to save the images in a folder named "images"
                    save_image_from_bytes(image_bytes, image_path)

        data.append({'Text': text, 'Date': date, 'ImagePath': image_path})

    return data

# Specify your API credentials and other parameters
api_id = '29549426'
api_hash = '44bd5a957eefe65197fe22275a65dc30'
phone_number = '918984937192'
channel_username = 'tikvahethiopia'
limit = 2

# Scrape the Telegram channel
scraped_data = scrape_telegram_channel(api_id, api_hash, phone_number, channel_username, limit)

# Create a DataFrame from the scraped data
df = pd.DataFrame(scraped_data)

# Generate image URLs based on the local file paths
df['ImageURL'] = df['ImagePath'].apply(lambda path: f'file://{os.path.abspath(path)}')

# Specify the path and filename for the CSV file
csv_filename = 'telegram_data.csv'
df.to_csv(csv_filename, index=False)