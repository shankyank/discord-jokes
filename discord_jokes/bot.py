import discord
import random

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith('/joke'):
        jokes = ['Why did the chicken cross the road? To get to the other side.', 'What do you call a dog magician? A labracadabrador.', 'I went to buy some camo pants but couldn't find any.']
        await message.channel.send(random.choice(jokes))

client.run('BOT_TOKEN')
