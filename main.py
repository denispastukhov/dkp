import os
import random
from loguru import logger
from tabulate import tabulate
import discord
#from dotenv import load_dotenv
from discord.ext import commands
import db_helpers
import sql_scripts
import datetime

#load_dotenv()
TOKEN = ''
db = db_helpers.Database()

bot = commands.Bot(command_prefix='dkp!')
#client = discord.Client()
LOGGER = logger

@bot.command(name='add_points',help='adds points to members')
async def nine_nine(ctx, *, args):
    print(args)
    user_dict = {}
    rows = args.split('\n')
    print (rows)
    for r in rows:
        temp = r.split(' ')
        user_dict[temp[0]] = temp[1]
    print (user_dict)

    #await ctx.send(response)
    
#TODO rework as command
@bot.command(name='regsrv',help='register current server in bot database')  
async def reg_server(ctx):
    registered_server = db.select_rows_dict_cursor(sql_scripts.select_guilds, ctx.guild.id)
    if registered_server is None:
        db.update_rows(sql_scripts.insert_guild, ctx.guild.id, ctx.guild.name)
        logger.info(f"added server {ctx.guild.name}" )
        await ctx.send (f"server {ctx.guild.name} successfully registered")
    else:
        await ctx.send (f"{ctx.guild.name} already registered")
   

@bot.command(name='regme',help='registers current user in bot database')  
async def reg_user(ctx):
    guild_users = db.select_one_row_dict_cursor(sql_scripts.select_users, ctx.guild.id, ctx.author.id)
    #check if user in list
    if guild_users is None:
        db.update_rows(sql_scripts.insert_user, ctx.author.name, ctx.author.id, ctx.guild.id)
        await ctx.send ('registration succesfull...i guess?')
    else:
        await ctx.send (f"{ctx.author.name} already registered")

@bot.command(name="start_period", help="starts reporting period")
async def start_period(ctx, *force):
    active_periods = db.select_rows_dict_cursor(sql_scripts.select_active_periods,ctx.guild.id)
    if len(active_periods)!=0 and len(force)==0:
        await ctx.send (f"you have {len(active_periods)} active periods. Add force to command to start new one")
    elif len(active_periods)==0:
        insert = db.update_rows(sql_scripts.insert_active_period, ctx.guild.id)
        print(insert)
    elif len(active_periods)!=0 and len(force)>0 and force[0]=='force':
        insert = db.update_rows(sql_scripts.insert_active_period, ctx.guild.id)

@bot.command(name="get_periods", help="starts reporting period")
async def get_periods(ctx, *status):
    script = sql_scripts.select_periods
    if len(status)>1:
        await ctx.send ("pls specify only 1 of 'active, closed, all'")
    elif len(status)==1 and status[0]=='closed':
        script += 'and close_date is not null'
    elif len(status)==1 and status[0]=='active':
        script += 'and close_date is null'
    elif len(status)==0:
        script += ''
    periods = db.select_rows_dict_cursor(script, ctx.guild.id)
    colnames = db.select_column_headers('public.payment_periods')
    response = ''
    for p in periods:
        response += f"ID = {p['id']} | START = {(p['open_date']).strftime('%d-%m-%y %H:%M')}\n"
    await ctx.send (response)
        




def main():
    print("hello")
    #db_helpers.db_init()
    db.select_rows_dict_cursor("select * from users", {})
    bot.run(TOKEN)

if __name__ == "__main__":   
    main()

