import discord
import os
from dotenv import load_dotenv

def run():
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True

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

        # Send message content
        await retweet_channel.send('"' + message.content + '"\n' + "- " + message.author.display_name)

        # Send embed with author's display avatar
        emb = discord.Embed()
        emb.set_image(url=message.author.display_avatar.url)
        await retweet_channel.send(embed=emb)

    client.run(os.getenv("token"))