# imports
import discord
import settings
import spotipy
import yt_dlp
import asyncio
from discord import FFmpegPCMAudio
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build

# logging setup
logger = settings.logging.getLogger("bot")

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True
intents.voice_states = True

# Spotify API
SPOTIFY_ID = settings.SPOTIFY_ID
SPOTIFY_SECRET = settings.SPOTIFY_SECRET
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET))

# YouTube API
YOUTUBE_API_KEY = settings.YOUTUBE_API  # Get API from settings
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


# CLASSES
# Bot start up and connection
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

# Audio playback
class audio_playback:
    def __init__(self):
      self.client = aclient()

    # Plays audio
    async def play_audio(self, ctx, audio_url):
        # Checks if in vc, then connects
        try:
            voice_channel = ctx.voice.channel
        except AttributeError as e:
            await ctx.response.send_message("You are not in a voice channel!")
            print(f"User channel error {e}")
            return
        
        vc = await voice_channel.connect()

        # TODO: Implement idling instead of disconnecting immediately - also timeout
        # TODO: Handle disconnections
        vc.play(FFmpegPCMAudio(audio_url, options="-vn -b:a 128k"), after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

# TODO: Add queuing
# Music View
class MusicSearchView(discord.ui.View):
    def __init__(self, video_results, voice_ops, user):
        super().__init__()
        self.video_results = video_results
        self.voice_ops = voice_ops
        self.user = user

    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(view=self)

    # Setting buttons to connect to vc and play audio
    # TODO: Fix "Interaction failed" although it works
    @discord.ui.button(label="1", style=discord.ButtonStyle.primary)
    async def first_option(self, button: discord.ui.Button, ctx: discord.Interaction):
        for child in self.children:
            child.disabled=True
        await self.play_audio(ctx, self.video_results[0].get('url'))
    
    @discord.ui.button(label="2", style=discord.ButtonStyle.primary)
    async def second_option(self, button: discord.ui.Button, ctx: discord.Interaction):
        for child in self.children:
            child.disabled=True
        await self.play_audio(ctx, self.video_results[1].get('url'))
    
    @discord.ui.button(label="3", style=discord.ButtonStyle.primary)
    async def third_option(self, button: discord.ui.Button, ctx: discord.Interaction):
        for child in self.children:
            child.disabled=True
        await self.play_audio(ctx, self.video_results[2].get('url'))
    
    @discord.ui.button(label="4", style=discord.ButtonStyle.primary)
    async def fourth_option(self, button: discord.ui.Button, ctx: discord.Interaction):
        for child in self.children:
            child.disabled=True
        await self.play_audio(ctx, self.video_results[3].get('url'))
    
    @discord.ui.button(label="5", style=discord.ButtonStyle.primary)
    async def fifth_option(self, button: discord.ui.Button, ctx: discord.Interaction):
        for child in self.children:
            child.disabled=True
        await self.play_audio(ctx, self.video_results[4].get('url'))


    async def play_audio(self, ctx: discord.Interaction, video_url):
        # Getting mp3 url from Youtube
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '320',
        }],
        'quiet': True,
        'noplaylist': True,
        'extract_flat': True,
        }

        # TODO: Optimize format filtering
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                formats = info_dict.get('formats', [info_dict])
                audio_url = None
                filtered = []
                for f in formats:
                    if f.get('ext') == 'webm' or f.get('ext') == 'mp4':
                        filtered.append(f)
                
                print(filtered)
                for w in filtered:
                    if w.get('acodec') == 'opus':
                        audio_url = w.get('url')
                
                print(f"\n{audio_url}")
                

        except Exception as e:
            print(f"Error extracting audio URL: {e}")
            return
        
        try:
            await self.voice_ops.play_audio(self.user, audio_url)
        except Exception as e:
            print(f"Error playing audio: {e}")
            return

# DECLARATIONS
client = aclient()
tree = discord.app_commands.CommandTree(client)


# Quick easy message command
@tree.command(name = "hi_john", description = "Blesses John")
async def hi_john(ctx: discord.interactions):
    await ctx.response.send_message('Hi John')

# TODO: Combine both searches into general "play" with optional param for YouTube or Spotify specifically
# YouTube Search
@tree.command(name="youtube_search", description="Plays audio from YouTube")
async def youtube_music_search(ctx: discord.interactions, *, query: str):
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
    voice_ops = audio_playback()
    user = ctx.user
    view = MusicSearchView(video_results=video_results, voice_ops=voice_ops, user=user)
    embed = discord.Embed(
        title="Choose the right video:",
        description="Select from below options",
        color=discord.Color.dark_teal()
    )
    for i,video in enumerate(video_results, start=1):
        embed.add_field(name=f"{i}. {video['title']} {video['duration']}", value="", inline=False)
    await ctx.response.send_message(embed=embed, view=view)

# Takes the video_id then finds the duration
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

# TODO: Check spotify functionality
# Spotify search
@tree.command(name="spotify_search", description="Play song on Spotify")
async def spotify_search(ctx: discord.interactions, *, query: str, max_results: int = 5):
    # Checks Spotify for track from query
    response = sp.search(q=query, limit=max_results, type='track')
    if not response['tracks']['items']:
        await ctx.send("No tracks found")
        return

    search_results = []
    for track in response['tracks']['items']:
        track_artist = track['artists'][0]['name']
        track_name = track['name']
        search_results.append({
            'artist' : track_artist,
            'name' : track_name,
            'url' : None
            })
    # Uses YT to get same song(hopefully) then get mp3 url
    for song in search_results:
        yt_request = youtube.search().list(
            part='snippet',
            q=f"{song.get('name')} {song.get('artist')} audio",
            type='video',
        )
        yt_response = yt_request.execute()
        video_Id = yt_response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_Id}'
        song.update({'url' : video_url})

    voice_ops = audio_playback()
    view = MusicSearchView(search_results=search_results)
    view.add_buttons()
    embed = discord.Embed(
        title="Choose the right video:",
        description="Select from below options",
        color=discord.Color.dark_teal()
    )
    option_number = 1
    for i,song in enumerate(search_results, start=1):
        embed.add_field(name=f"{i}. {song['name']} {song['artist']}", value="", inline=False)
    await ctx.response.send_message(embed=embed, view=view)


client.run(settings.DISCORD_SECRET_API)
