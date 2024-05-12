import socket
import logging
import asyncio
from telegram import Bot

#Syslog server config
HOST = '0.0.0.0'
PORT = 514
LOG_FILE = 'syslog_messages.txt'

#Telegram config
TELEGRAM_TOKEN = '7061653572:AAHXPYtGawd3xi3ai1kSk2_AsYiHGpU0gvE'
TELEGRAM_CHAT_ID = '6853099040'

#Send syslog messages to Telegram
async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def main():
  #Start syslog server
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #UDP Socket
  server_socket.bind((HOST, PORT))

  while True:
    message, address = server_socket.recvfrom(8192)
    message_str = message.decode()

    #Rough filter for syslog messages
    if "%" not in message_str:
            continue

    with open(LOG_FILE, 'a') as file:
            file.write("{} - {}\n".format(address, message_str))

    #Obtain severity level from the syslog messages
    severity = int(message.decode().split('-')[1].split(':')[0])

    #Notify to Telegram if severity of 0-4
    if severity <= 4:
        body = "Received Syslog message of level {} from {}: {}".format(severity, address, message.decode())
        await send_telegram_message(body)


if __name__ == "__main__":

    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
    asyncio.run(main())


#Make sure that intermediary devices are configured to the server's IP "logging <>"