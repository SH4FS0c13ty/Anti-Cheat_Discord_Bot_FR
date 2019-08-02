import discord, sys, os, requests, json, ctypes
import ocr, tools, getcolor
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

ctypes.windll.kernel32.SetConsoleTitleW("Module Anti-Cheat Checker")

client = discord.Client()
bot = commands.Bot(command_prefix="./", description="Un bot Discord qui éjecte les tricheurs d'après leur liste de serveurs et leur ID Pokémon GO.")

arg = sys.argv[1]


@bot.event
async def on_member_join(member):
    global blacklisted
    blacklisted = 0
    userid = str(member.id)
    username = str(member.name)
    print("[INFO] " + username + " a rejoint le serveur.")
    try:
        file =  open("lists\\cheaters_ids.txt").read()
        if file.find(userid) != -1:
            print("[ATTE] " + "L'utilisateur " + userid + " est dans la liste des tricheurs.")
            print("[INFO] " + "Éjection de " + username + ".")
            user = usr(userid)
            await member.guild.kick(user)
        else:
            print("[INFO] " + username + " n'est pas dans la liste des tricheurs.")
    except:
        print("[ATTE] La liste des tricheurs est manquante. Impossible de vérifier " + username + ".")


@bot.command(pass_context=True)
async def verify(ctx, url=None):
    global pokeid
    global blacklisted
    blacklisted = 0
    userid = str(ctx.author.id)
    username = str(ctx.author.name)
    role = get(ctx.guild.roles, name="Verified")
    if role in ctx.author.roles:
        print("[ATTE] " + username + " a essayé d'utiliser ./verify mais est déjà vérifié.")
        await ctx.message.delete()
    else:
        if url is None:
            try:
                url = str(ctx.message.attachments[0].url)
            except:
                print("[ATTE] " + username + " a utilisé ./verify sans arguments.")
                await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                print("[INFO] Salon nettoyé.")
                return 0
        print("[INFO] " + username + " est en train d'être vérifié.")
        get_img(url, userid)
        if pokeid == "ERROR":
            print("[ATTE] Page Pokémon GO soumise incorrecte. Imposible de vérifier " + username + ".")
            await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: The image you submitted for verification is wrong!\n:flag_fr: L'image que vous avez soumis pour la vérification est incorrecte !")
            await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
        bcheck(userid)
        if blacklisted == 0:
            print("[INFO] " + "Nouvel utilisateur vérifié : " + username + ".")
            await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: Welcome to the server Pokémon GO Marseille!\n:flag_fr: Bienvenue dans le serveur Pokémon GO Marseille !")
            role = get(ctx.guild.roles, name="Verified")
            await ctx.author.add_roles(role)
            print("[INFO] " + "Rôle Verified appliqué à " + username + ".")
            global team
            teamrole = get(ctx.guild.roles, name=team)
            await ctx.author.add_roles(teamrole)
            print("[INFO] " + "Rôle " + team + " appliqué à " + username + ".")
            await ctx.author.edit(nick=pokeid)
            print("[INFO] " + "Surnom de " + username + " changé en " + pokeid + ".")
            blacklisted = 0
        if blacklisted == 1:
            print("[ATTE] " + "Tricheur détecté !\n[INFO] Éjection de " + username + ".")
            await ctx.author.send("[Pokémon GO Marseille]\n https://cdn.discordapp.com/attachments/451360093607297054/599226877277634561/IMG_20190511_111313.jpg \n:flag_us: You have been detected as a cheater, please contact an administrator and prove that you are not a cheater to access the server.\n:flag_fr: Vous êtes soupçonné d'être un tricheur, veuillez contacter un administrateur et lui prouver que vous n'êtes pas un tricheur afin d'accéder au serveur.")
            write_cheater_id(userid)
            user = usr(userid)
            await ctx.guild.kick(user)
            blacklisted = 0
        if blacklisted == 2:
            print("[ATTE] " + username + " n'a pas autorisé le bot a accéder à ses informations.")
            await ctx.author.send(":flag_us: You must authorize the bot to access your informations before verifying yourself!\n:flag_fr: Vous devez autoriser le bot à accéder à vos informations avant de vous vérifier !")
            blacklisted = 0
        await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
        print("[INFO] Salon nettoyé.")

def get_img(url, userid):
    filename = url.rsplit('/', 1)[1]
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    global team
    team = getcolor.main_color(filename)
    global pokeid
    pokeid = ocr.getid(filename, userid)

def write_cheater_id(id):
    if os.path.isfile("lists\\cheaters_ids.txt") == True:
        file = open("lists\\cheaters_ids.txt", "r").read()
        if file.find(id) != -1:
            print("[INFO] " + "L'utilisateur " + id + " est déjà dans la liste des tricheurs.")
        else:
            f=open("lists\\cheaters_ids.txt", "a+", encoding="utf-8")
            f.write(id + "\n")
            f.close()
            print("[INFO] " + "L'utilisateur " + id + " a été ajouté dans la liste des tricheurs.")
    else:
        f=open("lists\\cheaters_ids.txt", "w+", encoding="utf-8")
        f.write(id + "\n")
        f.close()
        print("[INFO] " + "L'utilisateur " + id + " a été ajouté dans la liste des tricheurs.")

@bot.event
async def on_ready():
    bot_id = str(bot.user.id)
    print("Connecté avec succès.")
    print("Nom : " + bot.user.name)
    print("ID : " + bot_id)
    print("========================")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def kick(ctx, user: discord.Member):
    username = str(user.name)
    print("[INFO] " + "Utilisateur éjecté : " + username + ".")
    await user.send(":flag_us: You have been kicked from the server. Please verify yourself again to access the server.\n:flag_fr: Vous avez été kické du serveur. Veuillez vous soumettre à une nouvelle vérification afin d'accéder au serveur.")
    await ctx.guild.kick(user)

def bcheck(userid):
    global blacklisted
    global pokeid
    blacklisted = 0
    blacklist = open("lists\\blacklist.txt", "r")
    if os.path.isfile("servers_lists\\" + userid + "_servers_list.txt") == True:
        print("[INFO] " + "Vérification de la liste noire des serveurs ...")
        guilds = open("servers_lists\\" + userid + "_servers_list.txt", "r")
        bline = blacklist.readlines()
        gline = guilds.readlines()
        for x in bline:
            x = x.split("\n", 1)[0]
            for y in gline:
                y = y.split("\n", 1)[0]
                if x == y:
                    print("[INFO] " + "Serveur sur la liste noire trouvé !")
                    blacklisted = 1
        blacklist.close()
        guilds.close()
        if blacklisted != 1:
            print("[INFO] " + "Aucun serveur sur la liste noire n'a été trouvé.")
        json_check(pokeid, userid)
    else:
        blacklisted = 2

def json_check(pokid, usrid):
    global blacklisted
    print("[INFO] " + "Vérification de la liste de tricheurs Pokémon GO ...")
    if os.path.isfile("lists\\cheaters.json") == False:
        tools.excel2json()
    with open("lists\\cheaters.json") as json_file:
        data = json.load(json_file)
        for p in data:
            if pokeid == p["Pseudo*"]:
                print("[ATTE] " + "Tricheur connu de Pokémon GO détecté.")
                if os.path.isfile("lists\\Associated_IDs.txt") == False:
                    f = open("lists\\Associated_IDs.txt", "w")
                    f.write("ID_Pokémon_GO:ID_Discord\n")
                    f.close()
                associated_ids = str(pokid + ":" + usrid + "\n")
                file = open("lists\\Associated_IDs.txt", "r").read()
                if file.find(associated_ids) != -1:
                    print("[INFO] " + "IDs déjà associés : " + pokid + ":" + usrid)
                else:
                    f = open("lists\\Associated_IDs.txt", "a")
                    f.write(pokid + ":" + usrid + "\n")
                    f.close()
                blacklisted = 1
    if blacklisted != 1:
        print("[INFO] " + pokeid + " n'est pas dans la liste des tricheurs.")

class usr():
    def __init__(self, userid):
        self.id = userid

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck(ctx, user: discord.Member):
    userid = str(user.id)
    username = str(user.name)
    print("[INFO] " + "Une nouvelle vérification pour " + username + " a été demandée.")
    role = get(ctx.guild.roles, name="Verified")
    if role in user.roles:
        await user.remove_roles(role)
    role = get(ctx.guild.roles, name="instinct")
    if role in user.roles:
        await user.remove_roles(role)
    role = get(ctx.guild.roles, name="valor")
    if role in user.roles:
        await user.remove_roles(role)
    role = get(ctx.guild.roles, name="mystic")
    if role in user.roles:
        await user.remove_roles(role)
    os.remove("servers_lists\\" + userid + "_servers_list.txt")
    await user.send("[Pokémon GO Marseille]\n:flag_us: You have been asked for a new verification, please follow the autorisation link and use ./verify to verify yourself.\n:flag_fr: Une nouvelle vérification de votre part est requise, veuillez suivre le lien d'autorisation et utilisez ./verify pour vous vérifier.")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck_all(ctx):
    print("[INFO] Une nouvelle vérification pour tout le monde a été demandée.")
    await ctx.send("@everyone\n[Pokémon GO Marseille]\n:flag_us: Everyone must be verified again, please follow the autorisation link and use ./verify to verify yourself.\n:flag_fr: Tout le monde doit être vérifié une nouvelle fois, veuillez suivre le lien d'autorisation et utilisez ./verify pour vous vérifier.")
    for member in ctx.message.guild.members:
        userid = member.id
        flag = False
        role = get(ctx.guild.roles, name="Admin")
        if role in member.roles:
            flag = True
        if userid == bot.user.id:
            flag=True
        if flag != True:
            role = get(ctx.guild.roles, name="Verified")
            if role in member.roles:
                await member.remove_roles(role)
            role = get(ctx.guild.roles, name="instinct")
            if role in member.roles:
                await member.remove_roles(role)
            role = get(ctx.guild.roles, name="valor")
            if role in member.roles:
                await member.remove_roles(role)
            role = get(ctx.guild.roles, name="mystic")
            if role in member.roles:
                await member.remove_roles(role)
            if os.path.isfile("servers_lists\\" + str(userid) + "_servers_list.txt") == True:
                os.remove("servers_lists\\" + str(userid) + "_servers_list.txt")

bot.run(arg)
