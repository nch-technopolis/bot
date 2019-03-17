

class Bot:
    def __init__(self, api):
        self.api = api

    def message_received(self, message):
        text = message['text'].lower()
        if 'денис' in text and 'как дела' in text:
            chat_id = message['chat']['id']
            text = 'Ленар меня предал'
            self.api.send_message(chat_id=chat_id, text=text)

