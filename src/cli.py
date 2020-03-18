import readline
from bot.bot import reply
from bot.telegram import API


def send_message(self, chat_id, text, *args, **kwargs):
    print(text)


API.send_message = send_message


while True:
    message = input('>>> ')
    update = {
        'message': {
            'text': message,
            'chat': {'id': 'console'},
        },
    }
    reply(update)
