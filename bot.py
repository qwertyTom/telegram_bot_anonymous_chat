import telebot
from telebot import types
from database import Database

TOKEN = ''
db = Database('db.db')
bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Cari lawan bicara')
    markup.add(item1)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🗣 Сказать свой профиль')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌ Berhenti mencari')
    markup.add(item1)
    return markup

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Saya Pria 👨')
    item2 = types.KeyboardButton('Saya Wanita 👩‍🦱')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Hai, {0.first_name}! Selamat datang di obrolan anonim! Tunjukkan jenis kelamin Anda! '.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Cari lawan bicara')
    markup.add(item1)

    bot.send_message(message.chat.id, '📝 Menu'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('✏️ Dialog berikutnya')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)

        bot.send_message(chat_info[1], '❌ Teman bicara meninggalkan obrolan', reply_markup = markup)
        bot.send_message(message.chat.id, '❌ Anda telah keluar dari obrolan', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌ Anda belum memulai obrolan!', reply_markup = markup)


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Cari lawan bicara' or message.text == '✏️ Dialog berikutnya':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔎 Pria')
            item2 = types.KeyboardButton('🔎 Wanita')
            item3 = types.KeyboardButton('👩‍👨 Acak')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Siapa yang harus dicari?', reply_markup = markup)

            
        elif message.text == '❌ Berhenti mencari':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Pencarian dihentikan, tulis /menu', reply_markup = main_menu())

        
        elif message.text == '🔎 Pria':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari lawan bicara', reply_markup = stop_search())
            else:
                mess = 'Teman bicara ditemukan! Untuk menghentikan dialog, tulis /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        
        elif message.text == '🔎 Wanita':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari lawan bicara', reply_markup = stop_search())
            else:
                mess = 'Teman bicara ditemukan! Untuk menghentikan dialog, tulis /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        

        elif message.text == '👩‍👨 Acak':

            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari lawan bicara', reply_markup = stop_search())
            else:
                mess = 'Teman bicara ditemukan! Untuk menghentikan dialog, tulis /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '🗣 Beri tahu profil Anda':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🗣 Anda mengatakan profil Anda')
                else:
                    bot.send_message(message.chat.id, '❌ Tidak ditentukan di akun Anda username')
            else:
                bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')

        

        elif message.text == 'Я Парень 👨':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅ Jenis kelamin Anda telah berhasil ditambahkan!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Anda telah memasukkan jenis kelamin Anda. Hubungi dukungan @AndiNrdnsyh')
        
        elif message.text == 'Я Девушка 👩‍🦱':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅ Jenis kelamin Anda telah berhasil ditambahkan!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Anda telah memasukkan jenis kelamin Anda. Hubungi dukungan @AndiNrdnsyh')
        
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')


@bot.message_handler(content_types='stickers')
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')

@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')



bot.polling(none_stop = True)
