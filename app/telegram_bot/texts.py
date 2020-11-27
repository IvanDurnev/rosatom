from app import bot
from app.models import Tag
from telegram import KeyboardButton, ReplyKeyboardMarkup
from config import Config


def organizers(sender):
    text = '''
Организатор:
[Амурская областная филармония](http://amurphil.ru)

Партнёр:
[Резиденция Дедушки Мороза в Благовещенске](https://www.instagram.com/domdedamoroza/?igshid=cklfrsza6feb)
    '''
    bot.send_message(chat_id=sender.tg_id,
                     text=text,
                     parse_mode='Markdown',
                     disable_web_page_preview=True)


def success_registration(user):
    return f'*Поздравляем, {user.first_name}!*\n Регистрация прошла успешно.'


def lets_register():
    text = '''
Привет! Сначала надо зарегистрироваться. Нажимай кнопку ниже.
    '''
    return text


def photo_template(user):
    text = '''
Чтобы получить фото в рамке - нужно прислать сюда любую свою личную фотографию или фотографию, где ты с коллективом или семьёй, и обязательно подписать её хэштэгом #фотозона

А вот, на всякий случай, видеоинструкция: https://telegra.ph/Kak-poluchit-foto-v-ramke-07-23
'''
    response = bot.send_message(chat_id=user.tg_id,
                                text=text,
                                parse_mode='Markdown')
    save_message(response, 'income', user.tg_id)


def stickers(user):
    text = '''
Вот ваши праздничные стикеры.
https://t.me/addstickers/dvergede
    '''
    response = bot.send_message(chat_id=user.tg_id,
                                text=text,
                                parse_mode='Markdown')
    save_message(response, 'income', user.tg_id)


def congrat(user):
    text = '''
❗️ Оставляй здесь свои поздравления и приветы любимым коллегам с #Поздравление и некоторые из них услышите в эфире 🙌🏻
    '''
    response = bot.send_message(chat_id=user.tg_id,
                                text=text,
                                parse_mode='Markdown')
    save_message(response, 'income', user.tg_id)


def program(user):
    text = '''
Данный блок создан, чтобы сотрудники всегда могли быть в курсе событий и знать когда их будут ждать новые активации и игры. 

Например:
Понедельник: 
 ⁃ 18.00-19.00 - Играем в виз по сериалам;
 ⁃ 19.00-19.30 - Учимся пить вино + виртуальная прогулка по Лувру.

Среда: 
 ⁃ 13.00-18.00 - Скинь самую смешную фотографию за 2020 год;
 ⁃ 18,00-19.00 - Новогоднее лото.

Пятница:
 ⁃ 18.00-18.30 - Мастер-класс по изготовлению коктейлей; 
 ⁃ 18.30-18.40 - С коктейлями смотрим приветственную речь главы компании;
 ⁃ 18.40-19.30 - Играем в клевер;
 ⁃ 19.30-20.00 - Награждение лучших сотрудников года;
 ⁃ 20.30-22.00 - Старт онлайн-активностей + диджей-сет в основной трансляции.

Внимание!
Также в отдельных виртуальных комнатах будут работать:
 ⁃ Детские мастер-классы;
 ⁃ Чемпионат по мафии;
 ⁃ Угадай мелодию;
 ⁃ Zoom-крокодил.
'''
    response = bot.send_animation(chat_id=user.tg_id,
                                  caption=text,
                                  animation='https://media.giphy.com/media/26u4cqiYI30juCOGY/giphy.gif',
                                  parse_mode='Markdown')
    # save_message(response, 'income', user.tg_id)



def tg_user_mention(user):
    return f'[{user.first_name} {user.last_name}](tg://user?id={user.tg_id})'


def greeting(user):
    text = f'''
Здравствуйте, {user.first_name}!
Это бот для постановки и выполнения задач Роснано 
'''
    return text


def main_menu():
    return '''
Внизу экрана иконка в виде квадратика, в котором 4 лепестка.
Нажимай на неё и ты увидишь кнопки главного меню.
Если такой кнопки нет - пришлите боту команду /start <- или нажмите на эту
Инструкция с картинкой здесь: https://telegra.ph/ikonka-09-15
    '''


def refer_link(user):
    text = '''
*КОНКУРС "ПОДКЛЮЧИ КОЛЛЕГУ"*

Итак, смотри внимательно, всего 2 условия конкурса:👇

✅ Тебе нужно участвовать абсолютно во всех активностях и в конкурсах в чат-боте;

✅Тебе необходимо подключить как можно больше коллег.

Как это сделать:
1. Под этим сообщением твоя индивидуальная ССЫЛКА.
2. Скопируй её.
3. Именно ЭТУ ссылку тебе необходимо направить коллегам,  которые еще не подключены.

Ссылку направляй любым удобным способом (электронная почта, WhatsApp, Telegram и д.р.).
‼️Главное, тебе необходимо проверить, чтобы коллеги по твоей ссылке  прошли регистрацию и подключились.

При выполнении всех этих пунктов - твой ценный балл будет зачтен в твою копилку!
Помни, чем больше подключений, тем выше твоя активность.
'''
    response = bot.send_message(chat_id=user.tg_id,
                                text=text,
                                parse_mode='Markdown')
    save_message(response, 'income', user.tg_id)
    link = f'https://t.me/{Config.BOT_NAME}?start=refer_{user.id}'
    response = bot.send_message(chat_id=user.tg_id,
                                text=link)
    save_message(response, 'income', user.tg_id)


def invited_user_came(user):
    return f'''
По твоему приглашению зарегистрирован пользователь {user.first_name}
'''


def already_registered():
    return '''
Привет, вы уже регистрировались
'''


def help(user):
    reply_markup = None
    if not user.phone:
        text = f'{user.first_name}, твой запрос на техподдержку принят.\n' \
               f'Нажмите на кнопку ниже, чтобы поделиться с администратором номером телефона.\n' \
               f'С вами свяжутся при ближайшей возможности.'
        phone_button = KeyboardButton(text='☎️ НАЖМИТЕ СЮДА, ЧТОБЫ ПОДЕЛИТЬСЯ НОМЕРОМ ТЕЛЕФОНА', request_contact=True)
        reply_markup = ReplyKeyboardMarkup(keyboard=[[phone_button]], one_time_keyboard=True, selective=True)
    else:
        text = f'{user.first_name}, твой запрос на техподдержку принят.\n' \
               f'С тобой свяжутся при ближайшей возможности.'
    ai_tag = Tag.query.filter(Tag.name.ilike('AI')).first()
    # if ai_tag in user.tags:
    #     user.tags.remove(ai_tag)
    #     db.session.commit()
    for moderator in user.get_group().moderators:
        response = bot.send_message(chat_id=moderator.tg_id,
                                    text=f'🆘{tg_user_mention(user)} просит помощи\n'
                                         f'id: {user.id}\n'
                                         f'ФИ: {user.first_name} {user.last_name}',
                                    parse_mode='Markdown')
        save_message(tg_message=response, direction='income', user_tg_id=moderator.tg_id)
    response = bot.send_message(chat_id=user.tg_id, text=text, reply_markup=reply_markup)
    save_message(tg_message=response, direction='income', user_tg_id=user.tg_id)
    response = bot.send_message(chat_id=user.tg_id,
                     text='Кстати, вот  '
                          '[короткая инструкция](https://telegra.ph/Instrukciya-igry-Snezhnoe-loto-11-16)',
                     parse_mode='Markdown')
    save_message(tg_message=response, direction='income', user_tg_id=user.tg_id)



