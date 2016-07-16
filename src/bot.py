# -*- coding: utf-8 -*-
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
    ConversationHandler)
import storage as STORAGE

with open('../conf', 'r') as conf:
    TOKEN = conf.read()


# STATES
WRITE_ISSUE = 1


def start(bot, update):
    bot.sendMessage(update.message.chat_id, 'started')
    STORAGE.set_user_issues(update.message.chat_id)
    return WRITE_ISSUE


def stop(bot, update):
    bot.sendMessage(update.message.chat_id, 'stopped')
    return ConversationHandler.END


def help_info(bot, update):
    bot.sendMessage(update.message.chat_id, 'You can use commands:\n'
                                            '/start - to start writing issue\n'
                                            '/stop - to stop & save issue\n'
                                            '/cancel - to cancel issue\n'
                                            '/help - to see this info')
    return WRITE_ISSUE


def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, text='canceled')
    return ConversationHandler.END


def do_something(bot, update):
    issue = STORAGE.get_user_issue(update.message.chat_id)
    if not issue.summary:
        issue.summary = update.message.text[:150]
    issue.text += update.message.text + '\n'
    STORAGE.set_user_issues(issue)
    bot.sendMessage(update.message.chat_id, issue.text)
    bot.sendMessage(update.message.chat_id,
                    'creating ISSUE: "{}"...'.format(issue.summary))

    return WRITE_ISSUE


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        allow_reentry=True,

        states={
            WRITE_ISSUE: [MessageHandler([Filters.text], do_something),
                          CommandHandler('stop', stop),
                          CommandHandler('help', help_info)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()