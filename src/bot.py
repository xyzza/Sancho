# -*- coding: utf-8 -*-
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
    ConversationHandler)

with open('../conf', 'r') as conf:
    TOKEN = conf.read()


# STATES
WAIT_FOR_TASK, WRITING_TASK = 1, 2


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=u'Принимаю описание задачи')
    return WRITING_TASK


def cancel(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Canceled')
    return ConversationHandler.END


def _help(bot, update):
    bot.sendMessage(update.message.chat_id, text=u'Справка')
    return WAIT_FOR_TASK


def error(bot, update, error):
    pass


def foo(bot, update):
    return WAIT_FOR_TASK

# def gender(bot, update):
#     user = update.message.from_user
#     logger.info("Gender of %s: %s" % (user.first_name, update.message.text))
#     bot.sendMessage(update.message.chat_id,
#                     text='I see! Please send me a photo of yourself, '
#                          'so I know what you look like, or send /skip if you don\'t want to.')
#
#     return PHOTO


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('help', _help)],

        states={
            WRITING_TASK: [RegexHandler('^(Boy|Girl|Other)$', foo)],

            WAIT_FOR_TASK: [MessageHandler([Filters.text], start),
                    CommandHandler('cancel', cancel)],

            # LOCATION: [MessageHandler([Filters.location], location),
            #            CommandHandler('skip', skip_location)],
            #
            # BIO: [MessageHandler([Filters.text], bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()