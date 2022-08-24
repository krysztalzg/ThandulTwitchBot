from bot.chat_bot import bot

try:
    bot.run()
except:
    bot.close_db()
