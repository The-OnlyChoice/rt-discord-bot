import discord
import os
from dotenv import load_dotenv

def run():
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True
    intents.members = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("Logged in as {0.user}".format(client))

    @client.event
    async def on_raw_reaction_add(payload):
        # Check if reacion is the correct emoji
        if str(payload.emoji) != "🔁":
            return

        message_channel = client.get_channel(payload.channel_id)
        message = await message_channel.fetch_message(payload.message_id)
        guild = message.guild

        # Getting the "retweets" channel
        retweet_channel = discord.utils.get(guild.text_channels, name="retweets")
        # Creating a "retweets" channel if one does not exist
        if not retweet_channel:
            retweet_channel = await guild.create_text_channel("retweets")

        # Checking if this reaction is the first one
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        if reaction.count > 1:
            return

        author = guild.get_member(message.author.id)
        # Send embed with author and message content
        emb = discord.Embed()
        emb.set_author(name=author.nick, url=None, icon_url=author.display_avatar.url)
        emb.add_field(name="\u200b", value='"' + message.content + '"', inline=False)
        emb.add_field(name="\u200b", value="- " + str(author), inline=False)
        await retweet_channel.send(embed=emb)

    client.run(os.getenv("token"))