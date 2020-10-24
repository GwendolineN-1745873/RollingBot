# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='roll', help='Simulates rolling dice. (Uses format "{amount}d{sides}", with amount being optional (default = 1).')
async def roll(ctx, dice: str):
    pattern = re.compile("^[1-9]?d[1-9]\\d*$")
    
    if not pattern.match(dice):
        #not a valid command
        response = str(ctx.author)+", that's not a valid roll!"
        await ctx.send(response)
        return
    
    number_of_dice = dice.split('d')[0]
    if (dice.split('d')[0] == ''):
        number_of_dice = 1

    number_of_dice = int(number_of_dice)
        
    number_of_sides = int(dice.split('d')[1])
    
    if(number_of_sides not in [4, 6, 8, 10, 12, 20, 100]):
        response = str(ctx.author)+", we don't use that dice here!"
        await ctx.send(response)
        return
    
    if (number_of_sides == 100):
        step = 10
        rolls = [
            str(random.randrange(0, 100, step))
            for _ in range(number_of_dice)
        ]
    
    else:
        rolls = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
    
    addition = 0
    for roll in rolls:
        addition += int(roll)
    
    response = str(ctx.author)+", you rolled: "+str(', '.join(rolls))+"."
    if (number_of_dice > 1):
        response +=" This adds up to "+str(addition)+"."
    
    await ctx.send(response)

bot.run(TOKEN)