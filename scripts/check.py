import discord, sys, os, requests, json, ctypes, traceback
import ocr, tools, getcolor
from discord.ext import commands
from discord.ext.commands import has_permissions, CommandNotFound
from discord.utils import get
import colorama
from colorama import Fore, Style

colorama.init()

ctypes.windll.kernel32.SetConsoleTitleW("Module Anti-Cheat Checker")

client = discord.Client()
bot = commands.Bot(command_prefix="./", description="Un bot Discord qui éjecte les tricheurs d'après leur liste de serveurs et leur ID Pokémon GO.")

arg = sys.argv[1]

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        user = str(ctx.author)
        userid = str(ctx.author.id)
        print(Fore.RED + Style.BRIGHT + "[WARN] Une commande inconnue a été soumise. Veuillez vérifier le fichier Anti-Cheat.log pour en savoir plus." + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "[WARN] Erreur déclenchée par " + user + " avec  l'ID " + userid + "." + Style.RESET_ALL)
        tools.log("[WARN] L'utilisateur " + user + " avec l'ID " + userid + " a déclenché l'erreur suivante:")
        tools.log("[ERRO] " + str(error))

@bot.event
async def on_member_join(member):
    try:
        global blacklisted
        blacklisted = 0
        userid = str(member.id)
        username = str(member.name)
        print("[INFO] " + username + " a rejoint le serveur.")
        tools.log("[INFO] " + username + " a rejoint le serveur.")
        try:
            file =  open("lists\\cheaters_ids.txt").read()
            if file.find(userid) != -1:
                print(Fore.RED + Style.BRIGHT + "[WARN] " + "L'utilisateur " + userid + " est dans la liste des tricheurs." + Style.RESET_ALL)
                print("[INFO] " + "Éjection de " + username + ".")
                tools.log("[WARN] " + "L'utilisateur " + userid + " est dans la liste des tricheurs.")
                tools.log("[INFO] " + "Éjection de " + username + ".")
                user = usr(userid)
                await member.guild.kick(user)
            else:
                print("[INFO] " + username + " n'est pas dans la liste des tricheurs.")
                tools.log("[INFO] " + username + " n'est pas dans la liste des tricheurs.")
        except:
            print(Fore.RED + Style.BRIGHT + "[WARN] La liste des tricheurs est manquante. Impossible de vérifier " + username + "." + Style.RESET_ALL)
            tools.log("[WARN] La liste des tricheurs est manquante. Impossible de vérifier " + username + ".")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
    

@bot.command(pass_context=True)
async def verify(ctx, url=None):
    try:
        global pokeid
        global blacklisted
        blacklisted = 0
        userid = str(ctx.author.id)
        username = str(ctx.author.name)
        role = get(ctx.guild.roles, name="Verified")
        if role in ctx.author.roles:
            print(Fore.RED + Style.BRIGHT + "[WARN] " + username + " a essayé d'utiliser ./verify mais est déjà vérifié." + Style.RESET_ALL)
            tools.log("[WARN] " + username + " a essayé d'utiliser ./verify mais est déjà vérifié.")
            await ctx.message.delete()
        else:
            if url is None:
                try:
                    url = str(ctx.message.attachments[0].url)
                except:
                    print(Fore.RED + Style.BRIGHT + "[WARN] " + username + " a utilisé ./verify sans arguments." + Style.RESET_ALL)
                    tools.log("[WARN] " + username + " a utilisé ./verify sans arguments.")
                    await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                    print("[INFO] Salon nettoyé.")
                    tools.log("[INFO] Salon nettoyé.")
                    return 0
            print("[INFO] " + username + " est en train d'être vérifié.")
            tools.log("[INFO] " + username + " est en train d'être vérifié.")
            get_img(url, userid)
            if pokeid == "ERROR":
                print(Fore.RED + Style.BRIGHT + "[WARN] Page Pokémon GO soumise incorrecte. Impossible de vérifier " + username + "." + Style.RESET_ALL)
                tools.log("[WARN] Page Pokémon GO soumise incorrecte. Impossible de vérifier " + username + ".")
                await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: The image you submitted for verification is wrong!\n:flag_fr: L'image que vous avez soumis pour la vérification est incorrecte !")
                await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                return 0
            bcheck(userid)
            if blacklisted == 0:
                print("[INFO] " + "Nouvel utilisateur vérifié : " + username + ".")
                tools.log("[INFO] " + "Nouvel utilisateur vérifié : " + username + ".")
                await ctx.author.send("[Pokémon GO Marseille]\n:flag_us: Welcome to the server Pokémon GO Marseille!\n:flag_fr: Bienvenue dans le serveur Pokémon GO Marseille !")
                role = get(ctx.guild.roles, name="Verified")
                await ctx.author.add_roles(role)
                print("[INFO] " + "Rôle Verified appliqué à " + username + ".")
                tools.log("[INFO] " + "Rôle Verified appliqué à " + username + ".")
                global team
                teamrole = get(ctx.guild.roles, name=team)
                await ctx.author.add_roles(teamrole)
                print("[INFO] Rôle " + team + " appliqué à " + username + ".")
                tools.log("[INFO] Rôle " + team + " appliqué à " + username + ".")
                await ctx.author.edit(nick=pokeid)
                print("[INFO] Surnom " + username + " changé en " + pokeid + ".")
                tools.log("[INFO] Surnom " + username + " changé en " + pokeid + ".")
                blacklisted = 0
            if blacklisted == 1:
                print(Fore.RED + Style.BRIGHT + "[WARN] " + "Tricheur détecté!\n[WARN] Éjection de " + username + "." + Style.RESET_ALL)
                tools.log("[WARN] " + "Tricheur détecté !\n[WARN] Éjection de " + username + ".")
                await ctx.author.send("[Pokémon GO Marseille]\n https://cdn.discordapp.com/attachments/451360093607297054/599226877277634561/IMG_20190511_111313.jpg \n:flag_us: You have been detected as a cheater, please contact an administrator and prove that you are not a cheater to access the server.\n:flag_fr: Vous êtes soupçonné d'être un tricheur, veuillez contacter un administrateur et lui prouver que vous n'êtes pas un tricheur afin d'accéder au serveur.")
                write_cheater_id(userid)
                user = usr(userid)
                await ctx.guild.kick(user)
                blacklisted = 0
            if blacklisted == 2:
                print(Fore.RED + Style.BRIGHT + "[WARN] " + username + " n'a pas autorisé le bot à accéder à ses informations." + Style.RESET_ALL)
                tools.log("[WARN] " + username + " n'a pas autorisé le bot à accéder à ses informations.")
                await ctx.author.send(":flag_us: You must authorize the bot to access your informations before verifying yourself!\n:flag_fr: Vous devez autoriser le bot à accéder à vos informations avant de vous vérifier !")
                blacklisted = 0
            await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
            print("[INFO] Salon nettoyé.")
            tools.log("[INFO] Salon nettoyé.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@verify.error
async def verify_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenue lors de l'utilisation de ./verify. Veuillez vérifier le fichier Anti-Cheat.log pour en savoir plus." + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Erreur déclenchée par " + user + " avec l'ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] L'utilisateur " + user + " avec l'ID " + userid + " a déclenché l'erreur suivante en utilisant ./verify :")
    tools.log("[ERRO] " + str(error))

def get_img(url, userid):
    try:
        filename = url.rsplit('/', 1)[1]
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        global team
        team = getcolor.main_color(filename)
        global pokeid
        pokeid = ocr.getid(filename, userid)
    except KeyboardInterrupt:
        return
    except IndexError as i:
        print(Fore.RED + Style.BRIGHT + "[WARN] URL soumises incorrecte. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(i))
        tools.log_traceback(traceback.format_exc())
        pokeid = "ERROR"
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def write_cheater_id(id):
    try:
        if os.path.isfile("lists\\cheaters_ids.txt") == True:
            file = open("lists\\cheaters_ids.txt", "r").read()
            if file.find(id) != -1:
                print("[INFO] " + "L'utilisateur " + id + " est déjà dans la liste des tricheurs.")
                tools.log("[INFO] " + "L'utilisateur " + id + " est déjà dans la liste des tricheurs.")
            else:
                f=open("lists\\cheaters_ids.txt", "a+", encoding="utf-8")
                f.write(id + "\n")
                f.close()
                print("[INFO] " + "L'utilisateur " + id + " a été ajouté à la liste des tricheurs.")
                tools.log("[INFO] " + "L'utilisateur " + id + " a été ajouté à la liste des tricheurs.")
        else:
            f=open("lists\\cheaters_ids.txt", "w+", encoding="utf-8")
            f.write(id + "\n")
            f.close()
            print("[INFO] " + "L'utilisateur " + id + " a été ajouté à la liste des tricheurs.")
            tools.log("[INFO] " + "L'utilisateur " + id + " a été ajouté à la liste des tricheurs.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@bot.event
async def on_ready():
    try:
        bot_id = str(bot.user.id)
        print("Connecté avec succès.")
        print("Nom : " + bot.user.name)
        print("ID : " + bot_id)
        print("========================")
        tools.log("[INFO] Connecté en tant que " + bot.user.name + " avec l'ID " + bot_id + ".")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier le fichier Anti-Cheat.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def kick(ctx, user: discord.Member):
    try:
        username = str(user.name)
        print("[INFO] " + "Utilisateur éjecté : " + username + ".")
        tools.log("[INFO] " + "Utilisateur éjecté : " + username + ".")
        await user.send(":flag_us: You have been kicked from the server. Please verify yourself again to access the server.\n:flag_fr: Vous avez été kické du serveur. Veuillez vous soumettre à une nouvelle vérification afin d'accéder au serveur.")
        await ctx.guild.kick(user)
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@kick.error
async def kick_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenue lors de l'utilisation de ./kick. Veuillez vérifier le fichier Anti-Cheat.log pour en savoir plus" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Erreur déclenchée par " + user + " avec l'ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] L'utilisateur " + user + " avec l'ID " + userid + " a déclenché l'erreur suivante en utilisant ./kick :")
    tools.log("[ERRO] " + str(error))

def bcheck(userid):
    try:
        global blacklisted
        global pokeid
        blacklisted = 0
        blacklist = open("lists\\blacklist.txt", "r")
        if os.path.isfile("servers_lists\\" + userid + "_servers_list.txt") == True:
            print("[INFO] " + "Vérification des serveurs sur la liste noire ...")
            tools.log("[INFO] " + "Vérification des serveurs sur la liste noire ...")
            guilds = open("servers_lists\\" + userid + "_servers_list.txt", "r")
            bline = blacklist.readlines()
            gline = guilds.readlines()
            for x in bline:
                x = x.split("\n", 1)[0]
                for y in gline:
                    y = y.split("\n", 1)[0]
                    if x == y:
                        print("[INFO] " + "Serveur sur la liste noire trouvé !")
                        tools.log("[INFO] " + "Serveur sur la liste noire trouvé !")
                        blacklisted = 1
            blacklist.close()
            guilds.close()
            if blacklisted != 1:
                print("[INFO] " + "Aucun serveur présent sur la liste noire n'a été trouvé.")
                tools.log("[INFO] " + "Aucun serveur présent sur la liste noire n'a été trouvé.")
            json_check(pokeid, userid)
        else:
            blacklisted = 2
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def json_check(pokid, usrid):
    try:
        global blacklisted
        print("[INFO] " + "Vérification de la liste des tricheurs Pokémon GO ...")
        tools.log("[INFO] " + "Vérification de la liste des tricheurs Pokémon GO ...")
        if os.path.isfile("lists\\cheaters.json") == False:
            tools.excel2json()
        with open("lists\\cheaters.json") as json_file:
            data = json.load(json_file)
            for p in data:
                if pokeid == p["Pseudo*"]:
                    print(Fore.RED + Style.BRIGHT + "[WARN] " + "Tricheur Pokémon GO connu détecté." + Style.RESET_ALL)
                    tools.log("[WARN] " + "Tricheur Pokémon GO connu détecté.")
                    if os.path.isfile("lists\\Associated_IDs.txt") == False:
                        f = open("lists\\Associated_IDs.txt", "w")
                        f.write("Pokémon_GO_ID:Discord_ID\n")
                        f.close()
                    associated_ids = str(pokid + ":" + usrid + "\n")
                    file = open("lists\\Associated_IDs.txt", "r").read()
                    if file.find(associated_ids) != -1:
                        print("[INFO] " + "IDs déjà associés : " + pokid + ":" + usrid)
                        tools.log("[INFO] " + "IDs déjà associés : " + pokid + ":" + usrid)
                    else:
                        f = open("lists\\Associated_IDs.txt", "a")
                        f.write(pokid + ":" + usrid + "\n")
                        f.close()
                    blacklisted = 1
        if blacklisted != 1:
            print("[INFO] " + pokeid + " n'est pas dans la liste des tricheurs.")
            tools.log("[INFO] " + pokeid + " n'est pas dans la liste des tricheurs.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

class usr():
    def __init__(self, userid):
        self.id = userid

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck(ctx, user: discord.Member):
    try:
        userid = str(user.id)
        username = str(user.name)
        print("[INFO] Une nouvelle vérification pour " + username + " a été demandée.")
        tools.log("[INFO] Une nouvelle vérification pour " + username + " a été demandée.")
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
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@recheck.error
async def recheck_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenue lors de l'utilisation de ./recheck. Veuillez vérifier le fichier Anti-Cheat.log pour en savoir plus." + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Erreur déclenchée par " + user + " avec l'ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] L'utilisateur " + user + " avec l'ID " + userid + " a déclenché l'erreur suivante en utilisant ./recheck :")
    tools.log("[ERRO] " + str(error))

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def recheck_all(ctx):
    try:
        print("[INFO] Une nouvelle vérification a été demandée à tout le monde.")
        tools.log("[INFO] Une nouvelle vérification a été demandée à tout le monde.")
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
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

@recheck_all.error
async def recheck_all_error(ctx, error):
    user = str(ctx.author)
    userid = str(ctx.author.id)
    print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenue lors de l'utilisation de ./recheck_all. Veuillez vérifier le fichier Anti-Cheat.log pour en savoir plus." + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "[WARN] Erreur déclenché par " + user + " avec l'ID " + userid + "." + Style.RESET_ALL)
    tools.log("[WARN] L'utilisateur " + user + " avec l'ID " + userid + " a déclenché l'erreur suivante en utilisant ./recheck_all :")
    tools.log("[ERRO] " + str(error))

bot.run(arg)
