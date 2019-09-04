import sys, os, json, subprocess, traceback
from excel2json import convert_from_file
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init()

if len(sys.argv) > 1:
    arg = sys.argv[1]

def log(event):
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    
    if os.path.isfile("logs\\Anti-Cheat.log") == True:
        file = open("logs\\Anti-Cheat.log", "a")
        if event == "NEW_SESSION":
            file.write("\n\n" + str(timestamp) + "  " + "NOUVELLE SESSION DU MODULE CHECKER DÉMARRÉE\n")
        else:
            file.write(str(timestamp) + "  " + str(event) + "\n")
        file.close()
    else:
        file = open("logs\\Anti-Cheat.log", "w")
        if event == "NEW_SESSION":
            file.write(str(timestamp) + "  " + "NOUVELLE SESSION DU MODULE CHECKER DÉMARRÉE\n")
        else:
            file.write(str(timestamp) + "  " + str(event) + "\n")
        file.close()

def log_traceback(event):
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    if os.path.isfile("logs\\Anti-Cheat_traceback.log") == True:
        file = open("logs\\Anti-Cheat_traceback.log", "a")
        file.write("=================================================================\n")
        file.write("Traceback à " + str(timestamp) + "\n" + event + "\n")
        file.write("=================================================================\n")
        file.close()
    else:
        file = open("logs\\Anti-Cheat_traceback.log", "w")
        file.write("Traceback à " + str(timestamp) + "\n" + event + "\n\n")
        file.close()

def excel2json():
    try:
        try:
            EXCEL_FILE = "lists\\cheaters.xlsx"
            convert_from_file(EXCEL_FILE)
            for filename in os.listdir("lists\\"):
                if filename.endswith(".json"):
                    os.rename("lists\\" + filename, "lists\\cheaters.json")
            print("[INFO] La liste des IDs des tricheurs Pokémon GO a été réinitialisée.")
            log("[INFO] La liste des IDs des tricheurs Pokémon GO a été réinitialisée.")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenue lors de la réinitialisation de la liste des IDs des tricheurs Pokémon GO." + Style.RESET_ALL)
            log("[WARN] Une erreur est survenue lors de la réinitialisation de la liste des IDs des tricheurs Pokémon GO.")
            log("[ERRO] " + str(e))
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichier Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)

def show_config():
    try:
        json_file = open("scripts\\config.json")
        res = json.load(json_file)

        CLIENT_ID = res["CLIENT_ID"]
        CLIENT_SECRET = res["CLIENT_SECRET"]
        TOKEN = res["TOKEN"]
        HOST = res["HOST"]
        PORT = res["PORT"]
        REDIRECT_URL = res["REDIRECT_URL"]
        OAUTH_WINDOW = res["OAUTH_WINDOW"]
        CHECKER_WINDOW = res["CHECKER_WINDOW"]
        AUTOSTART = res["AUTOSTART"]

        print("=========================================================================================")
        print("                          Configuration actuelle d'Anti-Cheat                            ")
        print("=========================================================================================")
        print("                                 Paramètres fonctionnels                                 ")
        print("=========================================================================================")
        print(" CLIENT_ID:            " + CLIENT_ID)
        print(" CLIENT_SECRET:        " + CLIENT_SECRET)
        print(" TOKEN:                " + TOKEN)
        print(" HOST:                 " + HOST)
        print(" PORT:                 " + PORT)
        print(" REDIRECT_URL:         " + REDIRECT_URL)
        print("=========================================================================================")
        print("                                 Paramètres des fenêtres                                 ")
        print("=========================================================================================")
        print(" OAUTH_WINDOW:         " + OAUTH_WINDOW)
        print(" CHECKER_WINDOW:       " + CHECKER_WINDOW)
        print("=========================================================================================")
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)

def autostart_config(arg2):
    try:
        json_file = open("scripts\\config.json")
        res = json.load(json_file)

        CLIENT_ID = res["CLIENT_ID"]
        CLIENT_SECRET = res["CLIENT_SECRET"]
        TOKEN = res["TOKEN"]
        HOST = res["HOST"]
        PORT = res["PORT"]
        REDIRECT_URL = res["REDIRECT_URL"]
        OAUTH_WINDOW = res["OAUTH_WINDOW"]
        CHECKER_WINDOW = res["CHECKER_WINDOW"]
        AUTOSTART = res["AUTOSTART"]

        if arg2 == "start":
            if AUTOSTART == "0":
                log("[INFO] Démarrage automatique désactivé. Reprise.")
                pass
            elif AUTOSTART == "1":
                print("[INFO] Démarrage automatique activé. Démarrage d'Anti-Cheat.\n")
                log("[INFO] Démarrage automatique activé. Démarragé d'Anti-Cheat.")
                startp = subprocess.Popen(args=["python", "scripts\\main.py", "scripts\\config.json"])
                startp.wait()
            else:
                print(Fore.RED + Style.BRIGHT + "[WARN] Paramètre de démarrage automatique incorrect." + Style.RESET_ALL)
                log("[WARN] Paramètre de démarrage automatique incorrect.")
        elif arg2 == "config":
            if AUTOSTART == "0":
                log("[INFO] Démarrage automatique désactivé. Changement du paramètre de démarrage automatique à 1.")
                print("[INFO] Démarrage automatique désactivé. Changement du paramètre de démarrage automatique à 1.")
                res = {
                      "CLIENT_ID" : CLIENT_ID,
                      "CLIENT_SECRET" : CLIENT_SECRET,
                      "TOKEN" : TOKEN,
                      "HOST" : HOST,
                      "PORT" : PORT,
                      "REDIRECT_URL" : REDIRECT_URL,
                      "OAUTH_WINDOW" : OAUTH_WINDOW,
                      "CHECKER_WINDOW": CHECKER_WINDOW,
                      "AUTOSTART": "1"
                      }
                json_file = open("scripts\\config.json", "w")
                json.dump(res, json_file, indent=4)
                json_file.close()
            elif AUTOSTART == "1":
                log("[INFO] Démarrage automatique activé. Changement du paramètre de démarrage automatique à 0.")
                print("[INFO] Démarrage automatique activé. Changement du paramètre de démarrage automatique à 0.")
                res = {
                      "CLIENT_ID" : CLIENT_ID,
                      "CLIENT_SECRET" : CLIENT_SECRET,
                      "TOKEN" : TOKEN,
                      "HOST" : HOST,
                      "PORT" : PORT,
                      "REDIRECT_URL" : REDIRECT_URL,
                      "OAUTH_WINDOW" : OAUTH_WINDOW,
                      "CHECKER_WINDOW": CHECKER_WINDOW,
                      "AUTOSTART": "0"
                      }
                json_file = open("scripts\\config.json", "w")
                json.dump(res, json_file, indent=4)
                json_file.close()
            else:
                print(Fore.RED + Style.BRIGHT + "[WARN] Paramètre de démarrage automatique incorrect." + Style.RESET_ALL)
                log("[WARN] Paramètre de démarrage automatique incorrect.")
        else:
            print(Fore.RED + Style.BRIGHT + "[WARN] Paramètre de démarrage automatique incorrect." + Style.RESET_ALL)
            log("[WARN] Paramètre de démarrage automatique incorrect.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)

def show_cheaters_pid():
    try:
        with open("lists\\cheaters.json") as json_file:
            data = json.load(json_file)
            for p in data:
                if p["Pseudo*"]:
                    print(p["Pseudo*"])
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)

def reset_json():
    try:
        res = {
              "CLIENT_ID" : "<CLIENT_ID>",
              "CLIENT_SECRET" : "<CLIENT_SECRET>",
              "TOKEN" : "<TOKEN>",
              "HOST" : "<HOST>",
              "PORT" : "<PORT>",
              "REDIRECT_URL" : "<REDIRECT_URL>",
              "OAUTH_WINDOW" : "SW_MINIMIZE",
              "CHECKER_WINDOW": "SW_MINIMIZE",
              "AUTOSTART": "0"
              }
        try:
            json_file = open("scripts\\config.json", "w")
            json.dump(res, json_file, indent=4)
            json_file.close()
            print("[INFO] Le fichier de configuration a été réinitialisé.")
            log("[INFO] Le fichier de configuration a été réinitialisé.")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenu lors de la réinitialisation du fichier de configuration." + Style.RESET_ALL)
            log("[WARN] Une erreur est survenue lors de la réinitialisation du fichier de configuration.")
            log("[ERRO] " + str(e))
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)

def set(var):
    try:
        val = input("Valeur pour " + var + " : ")
        
        json_file = open("scripts\\config.json", "r")
        res = json.load(json_file)
        res[var] = val
        json_file.close()
        
        json_file = open("scripts\\config.json", "w")
        json.dump(res, json_file, indent=4)
        json_file.close()
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)

def contact():
    print("==============================================")
    print("|                SH4FS0c13ty                 |")
    print("==============================================")
    print("|                                            |")
    print("| Discord :   SH4FS0c13ty#1562               |")
    print("| Twitter :   @SH4FS0c13ty                   |")
    print("| Github :    https://github.com/SH4FS0c13ty |")
    print("| Site web :  https://sh4fs0c13ty.tk/        |")
    print("|                                            |")
    print("| Autre projets :                            |")
    print("|                                            |")
    print("|  - TigerXDragon (Kit de Traduction pour    |")
    print("|                  Toradora! Portable        |")
    print("|                                            |")
    print("|  - Toradora! FR (Projet de traduction de   |")
    print("|                  Toradora! Portable        |")
    print("|                  https://toradora-fr.tk)   |")
    print("|                                            |")
    print("==============================================")

if arg == "show_config":
    show_config()

if arg == "show_cheaters_pid":
    show_cheaters_pid()

if arg == "reset_json":
    reset_json()

if arg == "set":
    arg2 = sys.argv[2]
    set(arg2)

if arg == "contact":
    contact()

if arg == "autostart":
    arg2 = sys.argv[2]
    autostart_config(arg2)
