import nextcord
from nextcord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Sends server info")
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        serverinfoEmbed = nextcord.Embed(
            timestamp=ctx.message.created_at, 
            color=nextcord.Color.blurple()
            )
        serverinfoEmbed.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        serverinfoEmbed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
        serverinfoEmbed.add_field(name="Highest role", value=ctx.guild.roles[-2], inline=False)
        serverinfoEmbed.add_field(name="Number of roles", value=str(role_count), inline=False)
        serverinfoEmbed.add_field(name="Bots", value=", ".join(list_of_bots), inline=False)

        await ctx.send(embed=serverinfoEmbed)


    @commands.command(description="Voting message")
    async def poll(self, ctx, *, message):
        emb = nextcord.Embed(
            title= " POLL ",
            description=f"{message}",
            colour=nextcord.Color.blurple()
        )
        msg = await ctx.send(embed=emb)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await ctx.message.delete()


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: nextcord.Member, *, reason=None):
        if reason==None:
            reason="no reason provided"
        await ctx.guild.kick(member)
        await ctx.send(f'User {member.mention} has been kicked for {reason}')    


def setup(bot):
    bot.add_cog(Moderation(bot))
