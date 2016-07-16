# -*- coding: utf-8 -*-
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
    ConversationHandler)

with open('../conf', 'r') as conf:
    TOKEN = conf.read()

TEXT = u''

# STATES
DO_SOMETHING= 1


def start(bot, update):
    bot.sendMessage(update.message.chat_id, 'started')
    return DO_SOMETHING


def stop(bot, update):
    bot.sendMessage(update.message.chat_id, 'Ended')
    return ConversationHandler.END


def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, text='Canceled')
    return ConversationHandler.END


def do_something(bot, update):
    bot.sendMessage(update.message.chat_id, update.message.text)
    bot.sendMessage(update.message.chat_id, 'do something')
    return DO_SOMETHING


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        allow_reentry=True,

        states={
            DO_SOMETHING: [MessageHandler([Filters.text], do_something),
                           CommandHandler('stop', stop)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()