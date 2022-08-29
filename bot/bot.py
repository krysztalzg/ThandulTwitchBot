from cgi import test
from twitchio.ext import commands

from .handlers.command_handlers import handle_add_command, handle_done_command, handle_clear_command

from sys import path
path.append('...')
from web_app.db import get_db_detached

class Bot(commands.Bot):

    def __init__(self, bot_environment):
        super().__init__(
            token=f'oauth:{bot_environment.client_token}',
            prefix=bot_environment.prefix,
            client_secret=bot_environment.client_secret,
            initial_channels=bot_environment.channels
        )
        self.db = get_db_detached()

    def close_db(self):
        if self.db is not None:
            self.db.close()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}({self.user_id})')

    @commands.command()
    async def add(self, ctx: commands.Context):
        if self.db is None:
            return
        await handle_add_command(ctx, self.db)

    @commands.command()
    async def done(self, ctx: commands.Context):
        if self.db is None:
            return
        await handle_done_command(ctx, self.db)

    @commands.command()
    async def clear(self, ctx: commands.Context):
        if self.db is None:
            return
        await handle_clear_command(ctx, self.db)
