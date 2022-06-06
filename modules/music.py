import asyncio
import nextcord
import youtube_dl
from nextcord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="joins a voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.reply("**❌ You need to be in a voice channel to use this command!**")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)


    @commands.command(description="streams music")
    async def play(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        
        await ctx.reply('🎶 Now playing: **{}**'.format(player.title))
    
    
    @commands.command(description="stops and disconnects the bot from voice")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    
    @commands.command()
    async def pause(self, ctx):
        SongPlaying = ctx.voice_client.is_playing()
        
        Paused = ctx.voice_client.is_paused()
        
        if Paused != True:
            ctx.voice_client.pause()
            await ctx.reply("**✅ The music is now paused**")
        else:
            if SongPlaying == True:
                await ctx.reply("**❌ The music is already paused.**")
            else:
                await ctx.reply("**❌ There is no song currently playing.**")


    @commands.command()
    async def resume(self, ctx):
        Paused = ctx.voice_client.is_paused()
        
        if Paused == True:
            ctx.voice_client.resume()
            await ctx.reply("**✅ Resumed your music**")
        else:
            await ctx.reply("**❌ The music is not paused**")


    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.reply("**❌ Not connected to a voice channel.**")

        ctx.voice_client.source.volume = volume / 100
        await ctx.reply(f"**🔊 Changed volume to {volume}%**")

    
    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.stop()

    
    @commands.command()
    async def playing(self, ctx):
        if ctx.voice_client is None:
            return await ctx.reply("**❌ Not connected to a voice channel.**")

        if ctx.voice_client.is_playing():
            await ctx.reply(f"**🎶 Now playing: {ctx.voice_client.source.title}**")
        else:
            await ctx.reply("**❌ There is no song currently playing.**")


    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("**❌ You are not connected to a voice channel.**")
                raise commands.CommandError("❌ Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))