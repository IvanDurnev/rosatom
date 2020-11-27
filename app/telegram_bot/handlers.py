from app import db, bot
from app.models import User, MainMenuItems
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.telegram_bot import texts
from app import Config
from telegram import ParseMode
import json
import math
import dialogflow_v2 as dialogflow


def command_start(update, context):
    from app import create_app
    app = create_app(config_class=Config)
    with app.app_context():
        # удаляем сообщение
        chat_id = update.message.from_user.id
        message_id = update.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)

        # функция обработки, если id пользователя в диплинке
        def handle_user_id():
            user_id = deep_link.split('_')[1]
            sender: User = User.query.get(user_id)
            if sender:
                sender.tg_id = update.message.from_user.id
                db.session.commit()
                reply_markup = get_main_menu()

                with open('app/static/images/bot_images/Руки в стороны.jpeg', 'rb') as photo:
                    context.bot.send_photo(chat_id=update.message.from_user.id,
                                   caption=texts.greeting(sender),
                                   photo=photo,
                                   reply_markup=reply_markup,
                                   parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(chat_id=chat_id,
                                 text='Кстати, вот  '
                                      '[короткая инструкция](https://telegra.ph/Instrukciya-po-rabote-v-chat-bote-Rosnano-11-27)',
                                 parse_mode=ParseMode.MARKDOWN)

        # если в составе команды пришел deep_link, то парсим и в отправляем в нужную функцию
        if len(update.message.text.split(' ')) > 1:
            deep_link = update.message.text.split(' ')[1]
            deep_link_dict = {
                'userid': handle_user_id,
            }
            if deep_link.split('_')[0] in deep_link_dict:
                return deep_link_dict[deep_link.split('_')[0]]()

        # если в составе команды deep_link нет, то приветствуем пользователя
        else:
            user = User.query.filter_by(tg_id=update.message.from_user.id).first()
            if not user:
                user = User()
                user.tg_id = chat_id
                user.first_name = update.message.from_user.first_name
                db.session.add(user)
                db.session.commit()
                reg_btn = InlineKeyboardButton(text='Зарегистрироваться',
                                               url=f'{Config.VIDGET_PREFIX}/auth/registration?user_tg_id={update.message.from_user.id}')
                reply_markup = InlineKeyboardMarkup([[reg_btn]])
                return bot.send_message(chat_id=update.message.from_user.id,
                                        text=texts.lets_register(),
                                        reply_markup=reply_markup)
            elif not user.phone or not user.email:
                user.set_subscribed()
                reg_btn = InlineKeyboardButton(text='Зарегистрироваться',
                                               url=f'{Config.VIDGET_PREFIX}/auth/registration?user_tg_id={update.message.from_user.id}')
                reply_markup = InlineKeyboardMarkup([[reg_btn]])
                return bot.send_message(chat_id=update.message.from_user.id,
                                        text=texts.lets_register(),
                                        reply_markup=reply_markup)
            else:
                user.set_subscribed()
                with open('app/static/images/bot_images/Руки в стороны.jpeg', 'rb') as photo:
                    bot.send_photo(chat_id=update.message.from_user.id,
                                   caption=texts.greeting(user),
                                   photo=photo,
                                   reply_markup=get_main_menu(),
                                   parse_mode=ParseMode.MARKDOWN)
                bot.send_message(chat_id=chat_id,
                                 text='Кстати, вот  '
                                      '[короткая инструкция](https://telegra.ph/Instrukciya-igry-Snezhnoe-loto-11-16)',
                                 parse_mode=ParseMode.MARKDOWN)


def command_users_count(update, context):
    from app import create_app
    app = create_app(config_class=Config)
    app.app_context().push()

    all_users = User.query.all()
    tg_users = User.query.filter(User.tg_id.isnot(None)).all()
    unsubscribed_users = User.query.filter(User.tg_id.isnot(None), User.unsubscribed.is_(True)).all()
    user = User.query.filter_by(tg_id=update.message.from_user.id).first()
    bot.send_message(chat_id=user.tg_id,
                     text=f'*Всего в системе* {len(all_users)}\n'
                          f'*Бота подключили* {len(tg_users)}\n'
                          f'*Отписались* {len(unsubscribed_users)}',
                     parse_mode=ParseMode.MARKDOWN)


def text_message(update, context):
    pass


def reply_message(update, context):
    pass


def contact_message(update, context):
    pass

def photo_message(update, context):
    pass


def audio_message(update, context):
    pass


def inline_buttons_handler(update, context):
    from app import create_app
    app = create_app(config_class=Config)
    with app.app_context():
        command = update.callback_query.data.split('_')[1]
        sender = User.query.filter_by(tg_id=update.callback_query.from_user.id).first()

        if command == 'referal':
            texts.refer_link(sender)
        elif command == 'congrat':
            texts.congrat(sender)
        elif command == 'story':
            texts.story(sender)
        elif command == 'photo':
            texts.photo_template(sender)
        elif command == 'poem':
            texts.poem(sender)
        elif command == 'sport':
            texts.sport(sender)

            return 'ok'


def delete_message(update, context):
    chat_id = update.callback_query.from_user.id
    message_id = update.callback_query.message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)


def get_main_menu():
    buttons_list = []
    main_menu_items = MainMenuItems.query.filter(MainMenuItems.enabled.is_(True)).order_by(MainMenuItems.order).all()
    if main_menu_items == None:
        return None
    for item in main_menu_items:
        buttons_list.append([{
            'text': item.text
        }])
    buttons = [*buttons_list]
    ReplyKeyboardMarkup = {
        'keyboard': buttons,
        'resize_keyboard': True,
        'selective': False
    }
    return json.dumps(ReplyKeyboardMarkup)


def create_button_map(buttons, col_count):
    button_map = []
    row_count = math.ceil(len(buttons) / col_count)
    current_button = 0
    for i in range(row_count):
        button_map.append([])
        for j in range(col_count):
            if current_button < len(buttons):
                button_map[len(button_map) - 1].append(buttons[current_button])
                current_button += 1
    return button_map


def get_inline_menu(button_lists):
    buttons = []
    item_count = -1
    for item in button_lists:
        if isinstance(item, list):
            item_count += 1
            buttons.append([])
            for subitem in item:
                inline_button = {
                    'text': f'{subitem["text"]}',
                    'callback_data': f'{subitem["data"]}'
                }
                buttons[item_count].append(inline_button)
        else:
            item_count += 1
            inline_button = {
                'text': f'{item["text"]}',
                'callback_data': f'{item["data"]}'
            }
            buttons.append([inline_button])

    ReplyKeyboardMarkup = {
        'inline_keyboard': buttons
    }
    return json.dumps(ReplyKeyboardMarkup)

