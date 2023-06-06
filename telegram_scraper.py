from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerChannel
import pandas as pd

api_id = '29549426'
api_hash = '44bd5a957eefe65197fe22275a65dc30'
session_name = 'first try of the scraper'

client = TelegramClient(session_name, api_id, api_hash)
client.start()

channel_username = 'tikvahethiopia'
channel_entity = client.get_entity(channel_username)
messages = client(GetHistoryRequest(
    peer=channel_entity,
    limit=100,  # Specify the number of messages to retrieve
    offset_date=None,
    offset_id=0,
    max_id=0,
    min_id=0,
    add_offset=0,
    hash=0
))

data= []

for message in messages.messages:
    text = message.message
    date = message.date
    data.append({'Text':text, 'Date':date})

df=pd.DataFrame(data)
csv_filename='tikvah_data.csv'
df.to_csv(csv_filename,index=True)
client.disconnect()
