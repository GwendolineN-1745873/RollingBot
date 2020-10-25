# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# The roll command: !roll {amount}d{sides} 
# (amount is optional, default = 1)
@bot.command(name='roll', help='Simulates rolling dice. (Uses format "{amount}d{sides} {advantage}", with amount being optional (default = 1), and {advantage} being either empty, -a for advantage or -d for disadvantage. Advantage/disadvantage only works for a single d20 roll.')
async def roll(ctx, dice: str, advantage=""):
    pattern = re.compile("^[1-9]?d[1-9]\\d*$")
    
    if not pattern.match(dice):
        #not a valid command
        response = str(ctx.author)+", that's not a valid roll!"
        await ctx.send(response)
        return
    
    if (dice.split('d')[0] == ''):
        number_of_dice = 1
    else:
        number_of_dice = dice.split('d')[0]

    # Gets info from format "{amount}d{sides}"
    number_of_dice = int(number_of_dice)
    number_of_sides = int(dice.split('d')[1])
    
    if(number_of_sides not in [4, 6, 8, 10, 12, 20, 100]):
        response = str(ctx.author)+", we don't use that dice here!"
        await ctx.send(response)
        return
    
    # Percentile dice requires different step
    if (number_of_sides == 100):
        step = 10
        rolls = [
            str(random.randrange(0, 101, step))
            for _ in range(number_of_dice)
        ]
    
    else:
        # Roll d20 with advantage/disadvantage
        if (number_of_sides == 20 and number_of_dice == 1 and (advantage == "-a" or advantage == "-d")):
            rolls = []
            rolls.append(random.randrange(1, number_of_sides + 1))
            rolls.append(random.randrange(1, number_of_sides + 1))
            
            if (advantage == "-a"):
                roll = max(rolls)
                advantage_string = "advantage"
            elif (advantage == "-d"):
                roll = min(rolls)
                advantage_string = "disadvantage"
                
            response = str(ctx.author)+", you rolled with "+advantage_string+": "+str(rolls[0])+" and "+str(rolls[1])+". So your roll is "+str(roll)+"."

        # Normal roll
        else:
            rolls = [
                str(random.randrange(1, number_of_sides + 1))
                for _ in range(number_of_dice)
            ]
    
            response = str(ctx.author)+", you rolled: "+str(', '.join(rolls))+"."
    
    # Give sum of the rolls if more than one dice was used
    if (number_of_dice > 1):
        addition = 0
        for roll in rolls:
            addition += int(roll)
        response +=" This adds up to "+str(addition)+"."
    
    if (advantage == "-a" or advantage == "-d"):
        if (number_of_sides != 20 or number_of_dice != 1):
            response +="\nAdvantage/disadvantage ignored. (Only for single d20 rolls!)"
        
    await ctx.send(response)

bot.run(TOKEN)