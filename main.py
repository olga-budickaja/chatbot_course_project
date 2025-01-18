import telebot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import os
from dotenv import load_dotenv
import json

load_dotenv()

token = os.getenv("TOKEN_TELEBOT")
admin = int(os.getenv("ADMIN"))
bot = telebot.TeleBot(token)


try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"films": [], "musics": []}


def save_data():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_films = KeyboardButton('Фільми 🎥')
btn_musics = KeyboardButton('Музика 🎵')
btn_histories = KeyboardButton('Анекдоти 😂')
btn_plays = KeyboardButton('Ігри 🎮')

MENU_KEYBOARD.add(btn_films, btn_musics, btn_histories, btn_plays)

ADMIN_KEYBOARD_FILM = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_add_film = KeyboardButton('Створити новий фільм')
btn_delete_film = KeyboardButton('Видалити фільм')
btn_view_film = KeyboardButton('Переглянути фільм')

ADMIN_KEYBOARD_FILM.add(btn_add_film, btn_delete_film, btn_view_film)

users = {}


@bot.message_handler(commands=['start'])
def start(message:Message):
    user_name = message.from_user.first_name

    if message.chat.id == admin:
        sent_message = bot.send_message(message.chat.id, "Вітаю в адмін панелі", reply_markup=MENU_KEYBOARD)
        bot.register_next_step_handler(sent_message, admin_panel)
    else:
        sent_message = bot.send_message(message.chat.id, f"🎬 Вітаю, {user_name}! Я розважальний бот 🤖. Розповім тобі про цікаві фільми 🎥, найулюбленіші хіти 🎵, найсмішніші анекдоти 😂 та навіть запропоную пограти 🎮!",
        reply_markup=MENU_KEYBOARD)
        sent_message = bot.send_message(message.chat.id, "Оберіть категорію: ")
        bot.register_next_step_handler(sent_message, user_panel)



# ADMIN PANEL
def admin_panel(message:Message):
    sent_message = bot.send_message(message.chat.id, "Оберіть категорію: ", reply_markup=ReplyKeyboardRemove())
    if message.text == 'Фільми 🎥':
        choose_category_admin(message, ADMIN_KEYBOARD_FILM, admin_panel_film)
    elif message.text == 'Музика 🎵':
        pass
    elif message.text == 'Анекдоти 😂':
        pass
    elif message.text == 'Ігри 🎮':
        pass


def choose_category_admin(message:Message, markup, fnk):
    """
    This function returns choose category from admin-menu,
    where message - message:Message,
    markup - name of ReplyKeyboardMarkup,
    fnc - next step`s function
    """
    sent_message = bot.send_message(message.chat.id, "Оберіть дію: ", reply_markup=markup)
    bot.register_next_step_handler(sent_message, fnk)


# films
def admin_panel_film(message:Message):
    if message.text == 'Створити новий фільм':
        sent_message = bot.send_message(message.chat.id, "Введіть назву фільма: ", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(sent_message, get_new_film_title)
    elif message.text == 'Видалити фільм':
        if len(data["films"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, film in  enumerate(data["films"]):
                keyboard.add(KeyboardButton(f'{idx + 1}. {film["title"]}'))

            sent_message = bot.send_message(message.chat.id, "Оберіть фільм для видалення: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, remove_film)
        else:
            sent_message = bot.send_message(message.chat.id, "В базі даних ще немає фільмів. Створіть перший: ", reply_markup=ReplyKeyboardRemove())
            sent_message = bot.send_message(message.chat.id, "Введіть назву фільма: ")
            bot.register_next_step_handler(sent_message, get_new_film_title)
    elif message.text == 'Переглянути фільм':
        if len(data["films"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, film in  enumerate(data["films"]):
                keyboard.add(KeyboardButton(f'{idx + 1}. {film["title"]}'))

            sent_message = bot.send_message(message.chat.id, "Оберіть фільм для перегляду: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, get_info_film)
        else:
            sent_message = bot.send_message(message.chat.id, "В базі даних ще немає фільмів. Створіть перший: ", reply_markup=ReplyKeyboardRemove())
            sent_message = bot.send_message(message.chat.id, "Введіть назву фільма: ")
            bot.register_next_step_handler(sent_message, get_new_film_title)


# create film
def get_new_film_title(message:Message):
    title = message.text
    new_film = {
        'title': title,
        'link': '',
        'desc': []
    }
    data['films'].append(new_film)
    save_data()
    sent_message = bot.send_message(message.chat.id, "Введіть посилання на фільм: ")

    bot.register_next_step_handler(sent_message, get_new_film_link)



def get_new_film_link(message:Message):
    data['films'][-1]['link'] = message.text
    save_data()
    sent_message = bot.send_message(message.chat.id, "Введіть короткий опис: ")
    bot.register_next_step_handler(sent_message, get_new_film_desc)



def get_new_film_desc(message: Message):
    if message.text in ["/end", "Закінчити створення"]:
        sent_message = bot.send_message(message.chat.id, "Фільм створено успішно.")
        start(message)
    else:
        data['films'][-1]['desc'].append(message.text)
        save_data()
        handle_end_creation(message, 'Фільм', 'Введіть короткий опис', get_new_film_desc)



# USER PANEL
def user_panel(message:Message):
    if message.text == 'Фільми 🎥':
        if len(data["films"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, film in  enumerate(data["films"]):
                keyboard.add(KeyboardButton(f'{idx + 1}. {film["title"]}'))

            sent_message = bot.send_message(message.chat.id, "Оберіть фільм для перегляду: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, get_info_film)
        elif message.text == 'Музика 🎵':
            pass
        elif message.text == 'Анекдоти 😂':
            pass
        elif message.text == 'Ігри 🎮':
            pass


# get film
def get_info_film(message: Message):
    id_film = int(message.text.split(".")[0]) - 1
    film = data["films"][id_film]

    bot.send_message(message.chat.id, film['title'], reply_markup=ReplyKeyboardRemove())

    for i in film['desc']:
        bot.send_message(message.chat.id, i)

    bot.send_message(message.chat.id, film['link'])
    start(message)


# remove film
def remove_film(message: Message):
    id_film = int(message.text.split(".")[0]) - 1
    del  data["films"][id_film]

    bot.send_message(message.chat.id, "Фільм успішно видалено.")
    start(message)


# GENERALY FUNCTIONS
def handle_end_creation(message: Message, name, action, func):
    """
    This function ended actions,
    where name - a category name,
    action - an action text,
    func - next step`s function
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_end_film = KeyboardButton('Закінчити створення')
    keyboard.add(btn_end_film)

    if message.text == "Закінчити створення" or message.text == "/end":
        sent_message = bot.send_message(message.chat.id, f"{name} успішно створено!",  reply_markup=ReplyKeyboardRemove())
        start(message)
    else:
        sent_message = bot.send_message(message.chat.id, f"{action} aбo - /end, щоб закінчити: ", reply_markup=keyboard)
        bot.register_next_step_handler(sent_message, func)


bot.infinity_polling()
