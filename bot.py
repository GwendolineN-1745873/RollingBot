# bot.py
import os
import random

import discord
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
                adv_roll = max(rolls)
                advantage_string = "advantage"
            elif (advantage == "-d"):
                adv_roll = min(rolls)
                advantage_string = "disadvantage"
                
            #response = str(ctx.author)+", you rolled with "+advantage_string+": "+str(rolls[0])+" and "+str(rolls[1])+". So your roll is "+str(roll)+"."

        # Normal roll
        else:
            rolls = [
                str(random.randrange(1, number_of_sides + 1))
                for _ in range(number_of_dice)
            ]
    
            response = str(ctx.author)+", you rolled: "+str(', '.join(rolls))+"."
    
    
    # Creates the embed to make the message pretty!
    embed=discord.Embed(title=f'Rolling {number_of_dice}d{number_of_sides}', description=f'The RollingBot has rolled the dice for you, {ctx.author}.', color=0x509590)
    embed.set_author(name=ctx.author, url='', icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://i.pinimg.com/originals/3f/54/c7/3f54c788ff090c52ad9782f96b78000e.jpg")
    
    # Display the roll(s)
    for i in range(0, len(rolls)):
        roll_nr = i+1
        embed.add_field(name=f'Roll {roll_nr}', value=str(rolls[i]), inline=True)
            
    # Give sum of the rolls if more than one dice was used
    if (number_of_dice > 1):
        total = 0
        for i in range(0, len(rolls)):
            total += int(rolls[i])
            
        #response +=" This adds up to "+str(total)+"."
        embed.add_field(name="Total", value=str(total), inline=False)
    
    if (advantage == "-a" or advantage == "-d"):
        if (number_of_sides != 20 or number_of_dice != 1):
            #response +="\nAdvantage/disadvantage ignored. (Only for single d20 rolls!)"
            embed.set_footer(text="Advantage/disadvantage ignored. (Only for single d20 rolls!)")
        else:
            advantage_title = advantage_string.title()
            embed.add_field(name=f'{advantage_title} roll:', value=str(adv_roll), inline=False)
            
            # Check if natural 1 or 20
            if (adv_roll == 1):
                embed.add_field(name="Ouch, a natural 1. That must suck.", value="My bad! :)", inline=True)
            
            elif (adv_roll == 20):
                embed.add_field(name="A natural 20! HELL YEAH!!", value="You're welcome, by the way. :)", inline=True)

            embed.set_footer(text=f'Rolled with {advantage_string}.')

    #await ctx.send(response, embed=embed)
    await ctx.send(None, embed=embed)

bot.run(TOKEN)