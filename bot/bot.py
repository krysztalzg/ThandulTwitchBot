from twitchio.ext import commands

from .handlers.message_handler import handle_message
from .handlers.command_handlers import add_command

class Bot(commands.Bot):

    def __init__(self, bot_environment):
        super().__init__(
            token=f'oauth:{bot_environment.client_token}',
            prefix=bot_environment.prefix,
            client_secret=bot_environment.client_secret,
            initial_channels=bot_environment.channels
        )

    async def event_ready(self):
        print(f'Logged in as | {self.nick}({self.user_id})')

    async def event_message(self, message):
        handle_message(message)

    @commands.command()
    async def add(self, ctx: commands.Context):
        add_command(ctx)
