import readline
from unittest.mock import MagicMock

from bot.runner import Runner
from bot.configured import denis


class CLIRunner(Runner):
    def get_update(self):
        message = input('>>> ')
        return {
            'message': {
                'chat': {'id': 0},
                'text': message,
                'from': {
                    'id': 42,
                },
            },
        }


if __name__ == '__main__':
    print("Емельянов слушает тебя")
    bot = denis(chats_cls=set)
    bot.api = MagicMock()
    bot.api.send_message.side_effect = lambda chat_id, text: print(text)
    runner = CLIRunner(bot)
    runner.run()
