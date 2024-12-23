from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
import database.database as mdb

db = mdb.Database()

async def helpe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Команды: \n"
             "1. /room_list ~ список комнат\n"
             "2. /get_room [номер комнаты] ~ заселение в комнату\n"
             "3. /add_cash [количество] ~ пополнение счета\n"
             "3. /leave_room ~ покинуть комнату\n"
             "4. /list_service ~ список услуг\n"
             "5. /get_service [название услуги] ~ приобрести услгу\n"
             "6. /list_product ~ список товаров\n"
             "7. /get_product [название товара] ~ приобрести товар\n"
    )


async def admin_helpe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Команды администратора: \n"
             "1. /add_room [номер комнаты] [цена] ~ добавить комнату\n"
             "2. /add_service [название услуги] [цена] ~ Добавить услугу\n"
             "3. /add_product [название товара] [цена] [количество] ~ Добавить товар\n"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if db.add_user(update.effective_user.id):
        output_info = "Добро пожаловать в гостиницу 'Юность'!\nВведите /help для просмотра доступных команд."
    else:
        output_info = 'Рад снова вас видеть! Чем могу помочь?\nВведите /help для просмотра доступных команд.'

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{output_info}"
    )


async def get_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_code = context.args[0]
    if db.get_admin(update.effective_user.id, admin_code):
        output_info = "Вы получили права администратора."
    else:
        output_info = "Неверный код администратора."
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{output_info}"
    )


async def get_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        room_number = int(context.args[0])
        rv = db.get_room(update.effective_user.id, room_number)
        if rv == 1:
            output_info = f"Вы заселены в комнату {room_number}."
        elif rv == 2:
            output_info = "У вас недостаточно средств"
        elif rv == 0:
            output_info = "Комната занята"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{output_info}"
        )
    except (ValueError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Неверный номер комнаты"
        )


async def leave_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if db.leave_room(update.effective_user.id):
        output_info = "Вы успешно покинули комнату."
    else:
        output_info = "Вы не заселены в комнату."
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{output_info}"
    )


async def add_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        room_number = int(context.args[0])
        price = float(context.args[1])
        if db.add_room(room_number, price, update.effective_user.id):
            output_info = f"Комната {room_number} добавлена с ценой {price}."
        else:
            output_info = "Не удалось добавить комнату. Возможно, комната с таким номером уже существует."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{output_info}"
        )
    except (IndexError, ValueError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Использование: /add_room [номер комнаты] [цена]"
        )


async def room_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rooms = db.list_rooms()
    room_list_text = rooms
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=room_list_text
    )


async def add_cash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        if amount > 0:
            db.add_cash(update.effective_user.id, amount)
            output_info = f"Ваш счет пополнен на {amount} руб."
        else:
            output_info = "Сумма пополнения должна быть положительной."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{output_info}"
        )
    except (IndexError, ValueError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Использование: /add_funds [сумма]"
        )


async def add_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        service_name = context.args[0]
        service_price = float(context.args[1])
        if db.add_service(update.effective_user.id, service_name, service_price):
            output_info = f"Услуга '{service_name}' добавлена с ценой {service_price}."
        else:
            output_info = "Не удалось добавить услугу. Возможно, услуга с таким названием уже существует."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{output_info}"
        )
    except (IndexError, ValueError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Использование: /add_service [название услуги] [цена]"
        )


async def service_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    services = db.list_services()
    service_list_text = services
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=service_list_text
    )


async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        service_name = context.args[0]
        rv = db.get_service(update.effective_user.id, service_name)
        if rv == 1:
            output_info = f"Услуга '{service_name}' оказана."
        elif rv == 2:
            output_info = "У вас недостаточно средств."
        elif rv == 0:
            output_info = "Услуга не найдена."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{output_info}"
        )
    except (IndexError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Использование: /get_service [название услуги]"
        )


async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        product_name = context.args[0]
        product_price = float(context.args[1])
        product_quantity = int(context.args[2])
        if db.add_product(update.effective_user.id, product_name, product_price, product_quantity):
            output_info = f"Продукт '{product_name}' добавлен с ценой {product_price} и количеством {product_quantity}."
        else:
            output_info = "Не удалось добавить продукт. Возможно, продукт с таким названием уже существует."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{output_info}"
        )
    except (IndexError, ValueError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Использование: /add_product [название товара] [цена] [количество]"
        )


async def product_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = db.list_products()
    product_list_text = products
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=product_list_text
    )


async def get_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        product_name = context.args[0]
        product_quantity = int(context.args[1])
        rv = db.get_product(update.effective_user.id, product_name, product_quantity)
        if rv == 1:
            output_info = f"Продукт '{product_name}' приобретен."
        elif rv == 2:
            output_info = "У вас недостаточно средств."
        elif rv == 0:
            output_info = "Продукт не найден."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{output_info}"
        )
    except (IndexError):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Использование: /get_product [название товара]"
        )