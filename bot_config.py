from telebot import TeleBot
import os



def save(val, path="uzs.txt"):
    with open(path, 'w') as f:
        f.write(str(val))


def load_value(path):
    with open(path, 'r') as f:
        val = float(f.read())
    return val


@tg_bot.message_handler(commands=['uzs'], content_types=['text'])
def set_uzs(message):
    try:
        uzs = float(message.text.split()[1])
        tg_bot.send_message(message.chat.id, f'You set UZS={uzs}')
        save(uzs, 'uzs.txt')
    except ValueError:
        tg_bot.send_message(message.chat.id, 'A wrong value entered')
    except IndexError:
        tg_bot.send_message(message.chat.id, f'UZS={load_value("uzs.txt")}')


if __name__ == '__main__':
    tg_bot = TeleBot('5426997463:AAFXiIKKH4x4OfBAJMlIuE_fI8tSO37-7aY')
    DEFAULT = '169.4915'
    if not os.path.exists("uzs.txt"):
        save(DEFAULT, "uzs.txt")

    tg_bot.polling()
