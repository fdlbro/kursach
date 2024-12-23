import logging

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler

import botmethods.localmethods as localmethods

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Rework this command to explain how bot works"
    )


def main():
    application = ApplicationBuilder().token('6881868535:AAGp24WZsY310VPUivWa9ePt2J2bE8UYUAY').build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), localmethods.start)
    help_handler = CommandHandler('help', localmethods.helpe)
    admin_help_handler = CommandHandler('admin_help', localmethods.admin_helpe)
    unknown_handler = MessageHandler(filters.COMMAND, localmethods.start)
    get_admin_handler = CommandHandler('get_admin', localmethods.get_admin)
    get_room_handler = CommandHandler('get_room', localmethods.get_room)
    leave_room_handler = CommandHandler('leave_room', localmethods.leave_room)
    add_room_handler = CommandHandler('add_room', localmethods.add_room)
    room_list_handler = CommandHandler('room_list', localmethods.room_list)
    add_cash_handler = CommandHandler('add_cash', localmethods.add_cash)
    list_service_handler = CommandHandler('list_service', localmethods.service_list)
    get_service_handler = CommandHandler('get_service', localmethods.get_service)
    list_product_handler = CommandHandler('list_product', localmethods.product_list)
    get_product_handler = CommandHandler('get_product', localmethods.get_product)
    add_service_handler = CommandHandler('add_service', localmethods.add_service)
    add_product_handler = CommandHandler('add_product', localmethods.add_product)
    

    application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(admin_help_handler)
    application.add_handler(get_admin_handler)
    application.add_handler(get_room_handler)
    application.add_handler(leave_room_handler)
    application.add_handler(add_room_handler)
    application.add_handler(room_list_handler)
    application.add_handler(add_cash_handler)
    application.add_handler(list_service_handler)
    application.add_handler(get_service_handler)
    application.add_handler(list_product_handler)
    application.add_handler(get_product_handler)
    application.add_handler(add_service_handler)
    application.add_handler(add_product_handler)

    application.add_handler(unknown_handler)


    application.run_polling()


if __name__ == '__main__':
    main()
