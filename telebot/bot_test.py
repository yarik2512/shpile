import telebot

TOKEN = "1796337176:AAHXAE_gRgrhdAWlZmc_hb6KFqVb0JBjxvk"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Hello!")


bot.polling()
