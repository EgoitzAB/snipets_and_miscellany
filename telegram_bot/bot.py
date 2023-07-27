#!/usr/bin/python3

import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

TOKEN = "5835605911:AAFqdHfOmyWfbS0zXXVuMIDPWmQzz-GQ7qQ"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="¡Soy un bot, me cago en tu puta madre!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=update.message.reply_text("Déjate de emoticonos que soy un bot, no tengo sentimientos."))


async def docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=update.message.reply_text("No soy tu secretario ni me interesan tus cosas, soy un bot tarugo."))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    dice_handler = MessageHandler(filters.Dice.ALL & (~filters.COMMAND), dice)
    docs_handler = MessageHandler(filters.Document.ALL & (~filters.COMMAND), docs)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)


    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(dice_handler)
    application.add_handler(docs_handler)

    application.run_polling()
