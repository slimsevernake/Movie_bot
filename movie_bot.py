#TODO Хорошая практика - сначала импортируем стандартные пакеты, потом специфические и сторонние

import greeting
import imdb
import logging
import requests
import settings
import math
import textwrap

#TODO Лишние пробелы
from telegram.ext import (Updater, CommandHandler, RegexHandler,
                          ConversationHandler, MessageHandler, Filters)

from telegram import ReplyKeyboardMarkup

#TODO Лишние пробелы
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='movie_bot.log'
                    )

#TODO Лишние пробелы
CHOOSING, SEARCH_ACTOR, SEARCH_MOVIE = range(3)
#TODO Лишние пробелы

def back_to_menu(bot, update, user_data):
    """Возвращает в главное меню.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    #TODO У всех этих принтов и логгирования проблемы с отступами. https://sgillies.net/2017/05/30/python-multi-line-comments-and-triple-quoted-strings.html
    logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
    print(f"""
              User: {update.message.chat.username},
              Chat id: {update.message.chat.id},
              Message: {update.message.text}
            """)
    update.message.reply_text('пока')

    return ConversationHandler.END


def greet_user(bot, update, user_data):
    """Приветсвует пользователя.

    При запуске бота, запускается клавиатура и
    дает информацию о возможностях бота.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    #TODO Если ты в одном месте используешь f-строки, то используй их везде. Или везде .format()
    ave_text = 'Привет {}! {} '.format(update.message.chat.first_name,
                                       greeting.greet_text)
    logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
    print(f"""
              User: {update.message.chat.username},
              Chat id: {update.message.chat.id},
              Message: {update.message.text}
            """)
    update.message.reply_text(ave_text, reply_markup=menu_keyboard())

    return CHOOSING


def get_actor_by_name(bot, update, user_data):
    """Задает вопрос, "Какого актера найти".

    После нажатия кнопки "Поиск актера",
    вступает в диалог с пользователем,
    получает имя и фамилию актера.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    question = 'Какого актера найти?'
    logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
    print(f"""
              User: {update.message.chat.username},
              Chat id: {update.message.chat.id},
              Message: {update.message.text}
            """)
    update.message.reply_text(question)
    return SEARCH_ACTOR


def get_movie_by_name(bot, update, user_data):
    """Задает вопрос, "Какой фильм найти".

    После нажатия кнопки "Поиск фильма",
    вступает в диалог с пользователем,
    получает название фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    question = 'Какой фильм найти?'
    logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
    print(f"""
              User: {update.message.chat.username},
              Chat id: {update.message.chat.id},
              Message: {update.message.text}
            """)
    update.message.reply_text(question)
    return SEARCH_MOVIE


def get_movie_TMDB_id(bot, update, user_data):
    """Получение id фильма на API TMDB.
        Обращаемся к API TMDB.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    query = user_data
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US",
        "query": f"""{query}""", #TODO зачем тут тройные кавычки? 
        "page": 1,
        "include_adult": "false"  #TODO Необходимо унифицировать использование " " и ' ', а то в одних строках одно, в других - другое
    }
    result = requests.get(url, params=params)
    info_movie_TMDB = result.json()
    user_data = info_movie_TMDB["results"][0]["id"]
    get_box_office(bot, update, user_data)


def get_box_office(bot, update, user_data):
    """Выдача сборов фильма.
        Обращаемся к API TMDB.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    movie_id = user_data
    url = f"""https://api.themoviedb.org/3/movie/{movie_id}"""
    params = {
        "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US"
    }
    result = requests.get(url, params=params)
    movie_details = result.json()
    user_data = movie_details["revenue"]
    reply_box_office(bot, update, user_data)


def reply_box_office(bot, update, user_data):
    box_office = user_data
    update.message.reply_text(f"""Сборы по миру: {box_office} $""")
    update.message.reply_text("Что еще ты хочешь найти? Выбирай.")
    return CHOOSING


def get_actor_id(bot, update, user_data):
    """Обращается к базе данных IMDb
    для поиска и выдачи информации о актере.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    try:
        ia = imdb.IMDb()
        user_query = update.message.text
        user_data['actor'] = user_query
        actor = ia.search_person(user_query)
        actor_id = actor[0].personID
        user_data = ia.get_person(actor_id)
        logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                    """)
        print(f"""
              User: {update.message.chat.username},
              Chat id: {update.message.chat.id},
              Message: {update.message.text}
            """)
        reply_actor_photo(bot, update, user_data)
    except IndexError:
        update.message.reply_text('Ничего не найдено, проверьте запрос.')
    return CHOOSING


def get_movie_id(bot, update, user_data):
    """Обращается к базе данных IMDb
    для получения id фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    try:
        ia = imdb.IMDb() #TODO ia не очень название для переменной
        user_query = update.message.text
        user_data['movie'] = user_query
        movie = ia.search_movie(user_query)
        movie_id = movie[0].movieID
        user_data = ia.get_movie(movie_id)
        logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
        print(f"""
                User: {update.message.chat.username},
                Chat id: {update.message.chat.id},
                Message: {update.message.text}
            """)
        get_movie_poster(bot, update, user_data)
        reply_description(bot, update, user_data)
    except IndexError:
        update.message.reply_text('Ничего не найдено, проверьте запрос.')
    return CHOOSING


def get_movie_poster(bot, update, user_data):
    """Выдача постера к фильму.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    url = info_movie['cover url']
    bot.send_photo(chat_id=update.message.chat.id, photo=url)


def reply_description(bot, update, user_data):
    """Выдает краткое описание фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    parts = info_movie['plot'][0].split('::') #TODOTODO parts - не очень название для переменной, я не понимаю, что внутри
    short_description = parts[0]
    update.message.reply_text(short_description)
    reply_directors(bot, update, user_data)


def reply_directors(bot, update, user_data):
    """Выдача режиссеров фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    directors_info = info_movie['director'][0:]
    name_director = []
    for directors in directors_info:
        name_director.append(directors['name'])
    producers = ', '.join(name_director)
    update.message.reply_text(f"Режиссеры: {producers}")
    reply_main_roles(bot, update, user_data)


def reply_main_roles(bot, update, user_data):
    """Выдача актеров в главных ролях фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    name_actors = []
    for actor in info_movie['cast'][:6]:
        name_actors.append(f"""{actor['name']} в роли {actor.currentRole}""")
    main_actors = '\n'.join(name_actors)
    update.message.reply_text(f"""В главных ролях: {main_actors}""")
    reply_release_date(bot, update, user_data)


def reply_release_date(bot, update, user_data):
    """Выдача даты выпуска.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    release = info_movie['original air date']
    update.message.reply_text(f"Дата выхода: {release}")
    get_movie_TMDB_id(bot, update, user_data)


def reply_actor_photo(bot, update, user_data):
    """Выдача биографии актера.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_actor = user_data
    url = info_actor['headshot']
    bot.send_photo(chat_id=update.message.chat.id, photo=url)
    reply_actor_birth_date(bot, update, user_data)


def reply_actor_birth_date(bot, update, user_data):
    info_actor = user_data
    update.message.reply_text(f"""Дата рождения: {info_actor['birth date']}""")
    reply_actor_actor_features(bot, update, user_data)


def reply_actor_actor_features(bot, update, user_data):
    info_actor = user_data
    features = '.'.join(info_actor['trade mark'])
    update.message.reply_text(f"""О том, кого обычно играет: {features}""")
    update.message.reply_text("Что еще ты хочешь найти? Выбирай.")
    return CHOOSING


def menu_keyboard():
    film_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера'],
                                         ['Отмена'] #TODO что с квадратными скобками
                                         ], resize_keyboard=True
                                        )
    return film_keyboard


def talk_to_me(bot, update, user_data):
        response_user = f""" Привет {update.message.chat.first_name},
                            {greeting.greet_text}"""
        logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
        print(f"""
                User: {update.message.chat.username},
                Chat id: {update.message.chat.id},
                Message: {update.message.text}
            """)
        update.message.reply_text(response_user, reply_markup=menu_keyboard())


def main():
    #TODO Не очень информативно
    """
    
    Запускает бот и работает с диалогом.

    """
    moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')
    print('Бот запускается') #TODO А когда запустится?

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', greet_user,
                                     pass_user_data=True),
                      RegexHandler('^(Поиск актера)$', get_actor_by_name,
                                   pass_user_data=True),
                      RegexHandler('^(Поиск фильма)$', get_movie_by_name,
                                   pass_user_data=True)],

        states={
            CHOOSING: [RegexHandler('^(Поиск актера)$', get_actor_by_name,
                                    pass_user_data=True),
                       RegexHandler('^(Поиск фильма)$', get_movie_by_name,
                                    pass_user_data=True)],

            SEARCH_ACTOR: [RegexHandler('^(Отмена)$', back_to_menu,
                                        pass_user_data=True),
                           MessageHandler(Filters.text, get_actor_id,
                                          pass_user_data=True)],

            SEARCH_MOVIE: [RegexHandler('^(Отмена)$', back_to_menu,
                                        pass_user_data=True),
                           MessageHandler(Filters.text, get_movie_id,
                                          pass_user_data=True)],
        },

        fallbacks=[RegexHandler('^(Отмена)$', back_to_menu,
                                pass_user_data=True)]

    )

    dp = moviebot.dispatcher
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, talk_to_me,
                                  pass_user_data=True))
    moviebot.start_polling()
    moviebot.idle()


if __name__ == "__main__":
    main()
