import discord
from discord.ext import commands
import random
from webserver import keep_alive
import os


client = commands.Bot(command_prefix=".")

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def piskvorky(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("Právě je na řadě <@" + str(player1.id) + ">")
        elif num == 2:
            turn = player2
            await ctx.send("Právě je na řadě <@" + str(player2.id) + ">")
    else:
        await ctx.send("Právě se hraje pokud chceš začít hru musíš počkat než se dohraje.")

@client.event
async def on_ready():
  print ('Bot je připraven.')
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('.piskvorky | .pole'))

@client.command()
async def pole(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " vyhrává!🎉")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Je to remíza!🏁")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Nelze napsat číslo které je v políčku.")
        else:
            await ctx.send("Právě hraje protihráč.")
    else:
        await ctx.send("Začněte hru napsáním příkazu .piskvorky")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@piskvorky.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Prosím označ dva hráče.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Buď si jístý že pinguješ! (příklad. <@jméno>).")

@pole.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Napiš tvojí pozici kam chceš umístit políčko.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Ujistěte se, že jste zadali číslo.")



keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run("TOKEN TVÉHO BOTA")