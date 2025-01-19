import telebot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import os
from dotenv import load_dotenv
import json
import random

load_dotenv()

token = os.getenv("TOKEN_TELEBOT")
admin = int(os.getenv("ADMIN"))
bot = telebot.TeleBot(token)

users = {}

try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"films": [], "musics": [], "joks": []}


def save_data():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_films = KeyboardButton('Фільми 🎥')
btn_musics = KeyboardButton('Музика 🎵')
btn_histories = KeyboardButton('Приколи 😂')
btn_plays = KeyboardButton('Ігри 🎮')

MENU_KEYBOARD.add(btn_films, btn_musics, btn_histories, btn_plays)

ADMIN_KEYBOARD_FILM = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_add_film = KeyboardButton('Додати фільм')
btn_delete_film = KeyboardButton('Видалити фільм')
btn_view_film = KeyboardButton('Переглянути фільм')

ADMIN_KEYBOARD_FILM.add(btn_add_film, btn_delete_film, btn_view_film)

ADMIN_KEYBOARD_MUSIC = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_add_music = KeyboardButton('Додати музику')
btn_delete_music = KeyboardButton('Видалити музику')
btn_view_music = KeyboardButton('Переглянути музику')

ADMIN_KEYBOARD_MUSIC.add(btn_add_music, btn_delete_music, btn_view_music)

ADMIN_KEYBOARD_JOKE = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_add_joke = KeyboardButton('Додати прикол')
btn_delete_joke = KeyboardButton('Видалити прикол')
btn_view_joke = KeyboardButton('Переглянути приколи')

ADMIN_KEYBOARD_JOKE.add(btn_add_joke, btn_delete_joke, btn_view_joke)

ADMIN_KEYBOARD_PLAY = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_play_1 = KeyboardButton('Камінь-ножиці-папір 🪨✂️🧻')
btn_play_2 = KeyboardButton('Вгадай число 🤓')

ADMIN_KEYBOARD_PLAY.add(btn_play_1, btn_play_2)


@bot.message_handler(commands=['start'])
def start(message:Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if message.chat.id == admin:
        sent_message = bot.send_message(message.chat.id, "Вітаю в адмін панелі", reply_markup=MENU_KEYBOARD)
        bot.register_next_step_handler(sent_message, admin_panel)
    else:
        if user_id not in users:
            users[user_id] = True
            bot.send_message(message.chat.id, f"🎬 Вітаю, {user_name}! Я розважальний бот 🤖. "
                                "Розповім тобі про цікаві фільми 🎥, найулюбленіші хіти 🎵, "
                                "найсмішніші приколи 😂 та навіть запропоную пограти 🎮!",
                        reply_markup=MENU_KEYBOARD)
        sent_message = bot.send_message(message.chat.id, "Оберіть категорію: ", reply_markup=MENU_KEYBOARD)
        bot.register_next_step_handler(sent_message, user_panel)



# ADMIN PANEL
def admin_panel(message:Message):
    sent_message = bot.send_message(message.chat.id, "Оберіть категорію: ", reply_markup=ReplyKeyboardRemove())
    if message.text == 'Фільми 🎥':
        choose_category_admin(message, ADMIN_KEYBOARD_FILM, admin_panel_film)
    elif message.text == 'Музика 🎵':
        choose_category_admin(message, ADMIN_KEYBOARD_MUSIC, admin_panel_music)
    elif message.text == 'Приколи 😂':
        choose_category_admin(message, ADMIN_KEYBOARD_JOKE, admin_panel_joke)
    elif message.text == 'Ігри 🎮':
        choose_category_admin(message, ADMIN_KEYBOARD_PLAY, play_panel)


def choose_category_admin(message:Message, markup, fnk):
    """
    This function returns choose category from admin-menu,
    where message - message:Message,
    markup - name of ReplyKeyboardMarkup,
    fnc - next step`s function
    """
    sent_message = bot.send_message(message.chat.id, "Оберіть дію: ", reply_markup=markup)
    bot.register_next_step_handler(sent_message, fnk)


# FILMS
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
    if message.text in ["/end", "Закінчити"]:
        sent_message = bot.send_message(message.chat.id, "Фільм створено успішно.")
        start(message)
    else:
        data['films'][-1]['desc'].append(message.text)
        save_data()
        handle_end_creation(message, 'Фільм створено успішно.', 'Введіть короткий опис', get_new_film_desc)


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


# MUSICS
def admin_panel_music(message:Message):
    if message.text == 'Додати музику':
        sent_message = bot.send_message(message.chat.id, "Введіть назву треку: ", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(sent_message, get_new_music_title)
    elif message.text == 'Видалити музику':
        if len(data["musics"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, music in  enumerate(data["musics"]):
                keyboard.add(KeyboardButton(f'{idx + 1}. {music["title"]}'))

            sent_message = bot.send_message(message.chat.id, "Оберіть музику для видалення: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, remove_music)
        else:
            sent_message = bot.send_message(message.chat.id, "В базі даних ще немає музики. Створіть першу: ", reply_markup=ReplyKeyboardRemove())
            sent_message = bot.send_message(message.chat.id, "Введіть назву музики: ")
            bot.register_next_step_handler(sent_message, get_new_music_title)
    elif message.text == 'Переглянути музику':
        if len(data["musics"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, music in  enumerate(data["musics"]):
                keyboard.add(KeyboardButton(f'{idx + 1}. {music["title"]}'))

            sent_message = bot.send_message(message.chat.id, "Оберіть музику для перегляду: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, get_info_music)
        else:
            sent_message = bot.send_message(message.chat.id, "В базі даних ще немає музики. Створіть першу: ", reply_markup=ReplyKeyboardRemove())
            sent_message = bot.send_message(message.chat.id, "Введіть назву музики: ")
            bot.register_next_step_handler(sent_message, get_new_music_title)


# create music
def get_new_music_title(message:Message):
    title = message.text
    new_music = {
        'title': title,
        'link': '',
    }
    data['musics'].append(new_music)
    save_data()
    sent_message = bot.send_message(message.chat.id, "Введіть посилання на музику: ")

    bot.register_next_step_handler(sent_message, get_new_music_link)


def get_new_music_link(message:Message):
    data['musics'][-1]['link'] = message.text
    save_data()
    bot.send_message(message.chat.id, "Музику створено успішно.")
    start(message)


# get music
def get_info_music(message: Message):
    id_music = int(message.text.split(".")[0]) - 1
    music = data["musics"][id_music]

    bot.send_message(message.chat.id, music['title'], reply_markup=ReplyKeyboardRemove())

    bot.send_message(message.chat.id, music['link'])
    start(message)


# remove music
def remove_music(message: Message):
    id_film = int(message.text.split(".")[0]) - 1
    del  data["musics"][id_film]

    bot.send_message(message.chat.id, "Музику успішно видалено.")
    start(message)


# JOKS
def admin_panel_joke(message:Message):
    if message.text == 'Додати прикол':
        sent_message = bot.send_message(message.chat.id, "Введіть вміст приколу: ", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(sent_message, get_new_joke_title)
    elif message.text == 'Видалити прикол':
        if len(data["joks"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, joke in  enumerate(data["joks"]):
                title = f"{idx + 1}. {joke["title"]}"
                image_url = joke["link"]

                keyboard.add(KeyboardButton(f'{idx + 1}. {joke["title"]}'))

                bot.send_photo(message.chat.id, image_url, caption=title)

            sent_message = bot.send_message(message.chat.id, "Оберіть прикол для видалення: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, remove_joke)
        else:
            sent_message = bot.send_message(message.chat.id, "В базі даних ще немає приколів. Створіть перший: ", reply_markup=ReplyKeyboardRemove())
            sent_message = bot.send_message(message.chat.id, "Введіть нотатку для приколу: ")
            bot.register_next_step_handler(sent_message, get_new_joke_title)
    elif message.text == 'Переглянути приколи':
        if len(data["joks"]):
            for idx, joke in enumerate(data["joks"]):
                title = joke["title"]
                media_url = joke["link"]

                bot.send_video(message.chat.id, media_url, caption=title)

            start(message)
        else:
            sent_message = bot.send_message(message.chat.id, "В базі даних ще немає приколів. Створіть перший: ", reply_markup=ReplyKeyboardRemove())
            sent_message = bot.send_message(message.chat.id, "Введіть вміст приколу: ")
            bot.register_next_step_handler(sent_message, get_new_joke_title)


# create joke
def get_new_joke_title(message:Message):
    title = message.text
    new_joke = {
        'title': title,
        'link': '',
    }
    data['joks'].append(new_joke)
    save_data()
    sent_message = bot.send_message(message.chat.id, "Введіть посилання на прикол: ")

    bot.register_next_step_handler(sent_message, get_new_joke_link)


def get_new_joke_link(message:Message):
    data['joks'][-1]['link'] = message.text
    save_data()
    sent_message = bot.send_message(message.chat.id, "Прикол створено успішно.")
    start(message)


# remove joke
def remove_joke(message: Message):
    id_film = int(message.text.split(".")[0]) - 1
    del  data["joks"][id_film]

    bot.send_message(message.chat.id, "Прикол успішно видалено.")
    start(message)


# USER PANEL
def user_panel(message:Message):
    if message.text == 'Фільми 🎥':
        if len(data["films"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, film in  enumerate(data["films"]):
                keyboard.add(KeyboardButton(f'{idx + 1}. {film["title"]}'))

            sent_message = bot.send_message(message.chat.id, "Оберіть фільм для перегляду: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, get_info_film)
        else:
            bot.send_message(message.chat.id, "Фільмів, нажаль, немає. 🤷🏽‍♀️")
            start(message)
    elif message.text == 'Музика 🎵':
        if len(data["musics"]):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for idx, music in  enumerate(data["musics"]):
                keyboard.add(KeyboardButton(f'{idx + 1}. {music["title"]}'))

            sent_message = bot.send_message(message.chat.id, "Оберіть музику для перегляду: ", reply_markup=keyboard)
            bot.register_next_step_handler(sent_message, get_info_music)
        else:
            bot.send_message(message.chat.id, "Музики, нажаль, немає. 🤷🏽‍♀️")
            start(message)
    elif message.text == 'Приколи 😂':
        if len(data["joks"]):
            for idx, joke in enumerate(data["joks"]):
                title = joke["title"]
                media_url = joke["link"]

                bot.send_video(message.chat.id, media_url, caption=title)

            start(message)
    elif message.text == 'Ігри 🎮':
        choose_category_admin(message, ADMIN_KEYBOARD_PLAY, play_panel)


# PLAYS
def play_panel(message:Message):
    if message.text == 'Камінь-ножиці-папір 🪨✂️🧻':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Камінь 🪨", "Ножиці ✂️", "Папір 🧻", "Закінчити")
        sent_message = bot.send_message(message.chat.id, "Оберіть свій хід: ", reply_markup=keyboard)
        bot.register_next_step_handler(sent_message, get_play_step)
    elif message.text == 'Вгадай число 🤓':
        random_number = random.randint(0, 100)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Дізнатись число 😈", "Закінчити")

        sent_message = bot.send_message(
            message.chat.id, "Вгадайте число від 0 до 100 включно: ", reply_markup=keyboard
        )

        bot.register_next_step_handler(sent_message, lambda msg: check_guess(msg, random_number))

def check_guess(message: Message, random_number):
    answer = message.text.strip()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Дізнатись число 😈", "Закінчити")

    if answer == "Закінчити":
        bot.send_message(message.chat.id, "Гру завершено.")
        start(message)
        return

    if answer == "Дізнатись число 😈":
        bot.send_message(message.chat.id, f"Загадане число: {random_number} 🤓")
        bot.send_message(message.chat.id, "Гру завершено.")
        start(message)
        return

    if not answer.isdigit():
        bot.send_message(message.chat.id, "Упс, 🙄 Будь ласка, введіть число від 0 до 100!", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda msg: check_guess(msg, random_number))
        return

    answer = int(answer)

    if not (0 <= answer <= 100):
        bot.send_message(message.chat.id, "Упс, 🙄 Будь ласка, введіть число від 0 до 100!", reply_markup=keyboard)
        bot.register_next_step_handler(message, lambda msg: check_guess(msg, random_number))
        return

    if answer == random_number:
        bot.send_message(message.chat.id, "Вітаю! Ви перемогли. 🏆")
        start(message)
    elif answer > random_number:
        bot.send_message(message.chat.id, "Не вгадали. 🤓 Підказка: Загадане число менше", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Не вгадали. 🤓 Підказка: Загадане число більше", reply_markup=keyboard)

    bot.register_next_step_handler(message, lambda msg: check_guess(msg, random_number))



def get_play_step(message: Message):
    user_answer = message.text
    bot_answers = ["Камінь 🪨", "Ножиці ✂️", "Папір 🧻"]
    keyboard = ["Камінь 🪨", "Ножиці ✂️", "Папір 🧻", "Закінчити"]

    # Випадковий вибір бота без зайвого тексту
    bot_choice = random.choice(bot_answers)

    bot.send_message(message.chat.id, f"Моя Відповідь: {bot_choice}")

    # Перевіряємо результат гри
    if user_answer == bot_choice:
        bot.send_message(message.chat.id, "Нічия 🤝")
        handle_and_creation_plays(message, "Оберіть свій хід: ", keyboard)

    elif user_answer == "Камінь 🪨":
        match bot_choice:
            case "Ножиці ✂️":
                bot.send_message(message.chat.id, "Вітаю! Ви перемогли. 🏆")
            case "Папір 🧻":
                bot.send_message(message.chat.id, "Ви програли. 🥺 Спробуємо ще?")

        handle_and_creation_plays(message, "Оберіть свій хід: ", keyboard)

    elif user_answer == "Ножиці ✂️":
        match bot_choice:
            case "Папір 🧻":
                bot.send_message(message.chat.id, "Вітаю! Ви перемогли. 🏆")
            case "Камінь 🪨":
                bot.send_message(message.chat.id, "Ви програли. 🥺 Спробуємо ще?")

        handle_and_creation_plays(message, "Оберіть свій хід: ", keyboard)

    elif user_answer == "Папір 🧻":
        match bot_choice:
            case "Камінь 🪨":
                bot.send_message(message.chat.id, "Вітаю! Ви перемогли. 🏆")
            case "Ножиці ✂️":
                bot.send_message(message.chat.id, "Ви програли. 🥺 Спробуємо ще?")

        handle_and_creation_plays(message, "Оберіть свій хід: ", keyboard)

    else:
        bot.send_message(message.chat.id, "Будь ласка, виберіть Камінь 🪨, Ножиці ✂️ або Папір 🧻.")
        handle_and_creation_plays(message, "Оберіть свій хід: ", keyboard)


# GENERALY FUNCTIONS
def handle_end_creation(message: Message, text_message, action, func):
    """
    This function ended actions,
    where name - a category name,
    action - an action text,
    func - next step`s function
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_end_film = KeyboardButton('Закінчити')
    keyboard.add(btn_end_film)

    if message.text == "Закінчити" or message.text == "/end":
        sent_message = bot.send_message(message.chat.id, f"{text_message} успішно створено!",  reply_markup=ReplyKeyboardRemove())
        start(message)
    else:
        sent_message = bot.send_message(message.chat.id, f"{action} aбo - /end, щоб закінчити: ", reply_markup=keyboard)
        bot.register_next_step_handler(sent_message, func)


def handle_and_creation_plays(message:Message, text_message, keyboardPlay):
    """
    This function ended plays,
    where text_message - text message for play start again,
    keyboardPlay - keyboard for play
    """
    if message.text == "Закінчити":
        bot.send_message(message.chat.id, "Гру завершено.")
        start(message)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for btn in keyboardPlay:
            keyboard.add(btn, )

        sent_message = bot.send_message(message.chat.id, text_message, reply_markup=keyboard)
        bot.register_next_step_handler(sent_message, get_play_step)


bot.infinity_polling()
