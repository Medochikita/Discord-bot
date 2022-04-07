import nextcord
from nextcord.ext import commands

class Server_comm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Sends server info")
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        serverinfoEmbed = nextcord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
        serverinfoEmbed.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        serverinfoEmbed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
        serverinfoEmbed.add_field(name="Highest role", value=ctx.guild.roles[-2], inline=False)
        serverinfoEmbed.add_field(name="Number of roles", value=str(role_count), inline=False)
        serverinfoEmbed.add_field(name="Bots", value=", ".join(list_of_bots), inline=False)

        await ctx.send(embed=serverinfoEmbed)
        print("Command -- Server_commands.py -- serverinfo")


    @commands.command(description="Voting message")
    async def poll(self, ctx, *, message):
        emb = nextcord.Embed(
            title= " HLASOVÁNÍ ",
            description=f"{message}",
            colour=ctx.author.colour
        )
        msg = await ctx.send(embed=emb)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        print("Command -- Server_commands.py -- poll")

    

        


def setup(bot):
    bot.add_cog(Server_comm(bot))
