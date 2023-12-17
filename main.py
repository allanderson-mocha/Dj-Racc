import settings
import discord
from discord import app_commands

logger = settings.logging.getLogger("bot")

intents = discord.Intents(guild_messages = True, reactions = True, message_content = True)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"{self.user} is in the houseee!")

client = aclient()
tree = discord.app_commands.CommandTree(client)

@tree.command(description= "Blesses John")
async def hi_john(interaction: discord.interactions):
    await interaction.response.send_message('Fuck you, John')

client.run(settings.DISCORD_SECRET_API)
