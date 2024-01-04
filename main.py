from discord.interactions import Interaction
import settings
import discord
from discord import app_commands

from googleapiclient.discovery import build

logger = settings.logging.getLogger("bot")

intents = discord.Intents.default()
intents.reactions = True

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False
    
    # Waits for sync to connect bot
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"{self.user} is in the houseee!")

class YoutubeSearchView(discord.ui.View):
    def __init__(self, video_results):
        super().__init__()
        self.video_results = video_results
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
    
    async def interaction_check(self, interaction):
        return interaction.user == self.video_results[0].get('author_id')

    def add_buttons(self):
        buttons = []
        n = 1
        for video in self.video_results:
            button = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label=f"{n}",
                url=video['url']
            )
            n += 1
            self.add_item(button)


client = aclient()
tree = discord.app_commands.CommandTree(client)

# Quick easy message command
@tree.command(name="salutations", description="Blesses John")
async def hi_john(ctx: discord.interactions):
    await ctx.response.send_message('Fuck you, John')

# YouTube Search Implementation:
YOUTUBE_API_KEY = settings.YOUTUBE_API  # Get API from settings
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@tree.command(name="youtube_search", description="Searches Youtube")

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
        video_duration = await get_video_duration(video_id=video_id)
        video_results.append({
            'title' : video_title,
            'url' : video_url,
            'duration' : video_duration
            })

    # Temp output
    view = YoutubeSearchView(video_results=video_results)
    view.add_buttons()
    embed = discord.Embed(
        title="Choose the right video:",
        description="Select from below options",
        color=discord.Color.dark_teal()
    )
    option_number = 1
    for video in video_results:
        embed.add_field(name=f"{option_number}. {video['title']} {video['duration']}", value="", inline=False)
        option_number += 1
    await ctx.response.send_message(embed=embed, view=view)

# Function to aqcuire video duration from Youtube API and convert to minutes:seconds format
async def get_video_duration(video_id):
    request = youtube.videos().list(
        part='contentDetails',
        id = video_id
    )
    response = request.execute()
    try:
        # Conversion to better format
        duration = response['items'][0]['contentDetails']['duration']
        minutes = int(duration[2:].split('M')[0])
        seconds = int(duration[-3:-1])
        duration = f"[{minutes}:{seconds}]"
        return duration
    except Exception as e:
        return ""

    
# Test run for interactive message menus
@tree.command(name="option_menu", description="experimental menu")
async def option_menu(ctx: discord.interactions):
    view = discord.ui.View(timeout=300)
    options = [
        discord.ui.Button(style=discord.ButtonStyle.primary, label="Option 1", custom_id="option_1"),
        discord.ui.Button(style=discord.ButtonStyle.secondary, label="Option 2", custom_id="option_2"),
        discord.ui.Button(style=discord.ButtonStyle.danger, label="Oh no", custom_id="close_menu")
    ]
    for option in options:
        view.add_item(option)
    await ctx.response.send_message("choose:", view=view)



client.run(settings.DISCORD_SECRET_API)
