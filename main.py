import settings
import discord
from discord import app_commands
<<<<<<< HEAD
from googleapiclient.discovery import build
=======
>>>>>>> 0e8979bed29512934155fbfdc73ccbcd8e71e4f3

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

<<<<<<< HEAD
@tree.command(name = "bye_john", description = "Blesses John")
async def bye_john(ctx: discord.interactions):
    await ctx.response.send_message('Fuck you, John')

async def nuh_uh(ctx: discord.interactions):
    await ctx.response.send_message('Fuck you, John')

# YouTube Search Implementation:
YOUTUBE_API_KEY = settings.YOUTUBE_API  # Get API from settings
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@tree.command(name = "youtube_search", description = "Searches Youtube")
async def youtube_music_search(ctx: discord.interactions, *, query: str, max_results: int = 5):
    # Calling search.list for search results including snippet and contentDetails
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
    )
    response = request.execute()

    # Processing response to obtain video title, URL, and duration
    video_results = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_results.append({
            'title' : video_title,
            'url' : video_url,
            })

    formatted_response = '\n'.join([f"Title: {video['title']}\nURL: {video['url']}" for video in video_results])
    await ctx.response.send_message(video_results)
=======
@tree.command(description= "Blesses John")
async def hi_john(interaction: discord.interactions):
    await interaction.response.send_message('Fuck you, John')
>>>>>>> 0e8979bed29512934155fbfdc73ccbcd8e71e4f3

client.run(settings.DISCORD_SECRET_API)
