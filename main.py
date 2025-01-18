import telebot
import os
from dotenv import load_dotenv

load_dotenv()

token = os.geten("TOKEN_TELEBOT")

bot = telebot.TeleBot(token)
