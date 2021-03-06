import nextcord
from nextcord.ext import commands
import requests
from functions.get_czk import cur_conversion
import passwords

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="")
    async def crypto(self, ctx, crypto: str):
        
        # It takes a crypto currency name as an argument, gets the data from the API, and then sends it to the user in a discord embed

        emb = nextcord.Embed(
            title= "**Crypto info 💰**",
            colour= ctx.author.colour
        )

        url = f"https://data.messari.io/api/v1/assets/{crypto}/metrics"
        headers = {
            "x-messari-api-key": f"{passwords.crypto_api_key}"
        }
        response = requests.get(url=url, headers=headers)
        data = response.json()

        timestamp = data["status"]["timestamp"]
        symbol = data["data"]["symbol"]
        name = data["data"]["name"]

        price_usd = data["data"]["market_data"]["price_usd"]
        price_czk = cur_conversion.get_czk_rom_usd(f"{price_usd}")

        percent_change_1hour = data["data"]["market_data"]["percent_change_usd_last_1_hour"]
        percent_change_24hour = data["data"]["market_data"]["percent_change_usd_last_24_hours"]

        emb.set_footer(text=f"timetsamp: {timestamp} ( add one hour ;) )")
        emb.add_field(name="Name", value=name)
        emb.add_field(name="symbol", value=symbol)
        emb.add_field(name="Price in usd", value=price_usd, inline=False)
        emb.add_field(name="Price in czk", value=price_czk, inline=False)
        emb.add_field(name="% change in last 1 hour", value=percent_change_1hour)
        emb.add_field(name="% change in last 24 hours", value=percent_change_24hour)
        
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Crypto(bot))
