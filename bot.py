#!/usr/bin/python3
import telegram  # Импортируем модуль telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters  # Импортируем необходимые классы и функции из модуля telegram.ext
import os
import subprocess

file_path = None  # declare file_path as a global variable

def handle_file(update, context):
    global file_path  # specify that file_path is a global variable
    # Проверяем, что файл имеет расширение .zab
    file_name = update.message.document.file_name
    file_ext = file_name.split('.')[-1]
    if file_ext != 'zab':
        if file_ext == 'zbk':
            update.message.reply_text('This is a backup from "ExpertUi", send a backup from Smarthome with the extension .zab')
        else:
            update.message.reply_text('This is not a backup from Z-Way Smarthome, the backup must be in .zab format')
        return

    # Скачиваем файл
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file_path = os.path.join('downloads', file_name)
    file.download(file_path)
    update.message.reply_text('File received!', reply_markup=reply_markup)

    # Вызываем второй скрипт, передав ему полный путь к скачанному файлу
    subprocess.call(['python3', 'zabToJSON.py', os.path.abspath(file_path)])
    file_path = file_path.replace('.zab', '.json')

# Получаем токен бота и создаем объект Updater
TOKEN = 'BOT_TOKEN'
bot = telegram.Bot(token=TOKEN)  # Создаем объект бота
updater = Updater(bot=bot, use_context=True)  # Создаем объект Updater с указанием объекта бота и параметром use_context=True

# Определяем список кнопок
buttons = [
    'Convert a backup to Z-Wave.Me HUB',
    'Convert a backup to Raspberry pi or linux system with RaZberry board',
    'Convert a backup to Raspberry pi or linux system with UZB stick',
    'Convert a backup to Home Assistant Z-Way Addon with Razberry board',
    'Convert a backup to Home Assistant Z-Way Addon with UZB stick'
]

# Создаем объект ReplyKeyboardMarkup и передаем в него список кнопок
reply_markup = ReplyKeyboardMarkup([[button] for button in buttons], resize_keyboard=True)


# Определяем функцию-обработчик кнопок
def handle_button(update, context):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    text = update.message.text

    # Определяем суфикс в зависимости от выбранной кнопки
    if text == 'Convert a backup to Z-Wave.Me HUB':
        suffix = '_HUB'
        config_var = 'configs/config'
        port_var = '/dev/ttyS0'
    elif text == 'Convert a backup to Raspberry pi or linux system with RaZberry board':
        suffix = '_RPI_RAZ'
        config_var = 'config'
        port_var = '/dev/ttyAMA0'
    elif text == 'Convert a backup to Raspberry pi or linux system with UZB stick':
        suffix = '_RPI_UZB'
        config_var = 'config'
        port_var = '/dev/ttyACM0'
    elif text == 'Convert a backup to Home Assistant Z-Way Addon with Razberry board':
        suffix = '_HA_RAZ'
        config_var = 'config'
        port_var = '/dev/ttyAMA0'
    elif text == 'Convert a backup to Home Assistant Z-Way Addon with UZB stick':
        suffix = '_HA_UZB'
        config_var = 'config'
        port_var = '/dev/ttyACM0'
    else:
        return
    # Отправляем сообщение с выбранным суффиксом
    context.bot.send_message(chat_id=chat_id,
                             text=f"converting..",
                             reply_markup=ReplyKeyboardRemove())


    file_parts = os.path.splitext(file_path)
    new_file_path = file_parts[0] + suffix + file_parts[1]
    os.rename(file_path, new_file_path)

    print(f'Config key: {config_var}')
    print(f'Port: {port_var}')
    # Вызываем скрипт, передав ему параметры и путь к файлу
    subprocess.call(['python3', 'update_config.py', '--config', config_var, '--port', port_var, new_file_path])
    subprocess.call(['python3', 'jsonToZAB.py', new_file_path])
    zab_path = new_file_path.replace('.json', '.zab')
    print(f'ZAB Path: {zab_path}')
    with open(zab_path, 'rb') as f:
        bot.send_document(chat_id=update.message.chat_id, document=f)
    os.remove(zab_path)

# Регистрируем обработчик кнопок
updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_button))

# Создаем папку для загрузки файлов, если ее нет
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Запускаем бота
updater.start_polling()  # Запускаем бота в режиме опроса сервера
updater.idle()  # Останавливаем бота при получении команды остановки (Ctrl-C)
