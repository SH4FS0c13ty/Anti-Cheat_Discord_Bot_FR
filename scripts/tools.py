import sys, os, json
from excel2json import convert_from_file

arg = sys.argv[1]

def excel2json():
    try:
        EXCEL_FILE = "lists\\cheaters.xlsx"
        convert_from_file(EXCEL_FILE)
        for filename in os.listdir("lists\\"):
            if filename.endswith(".json"):
                os.rename("lists\\" + filename, "lists\\cheaters.json")
        print("[INFO] La liste des ID Pokémon GO des tricheurs a été réinitialisée.")
    except:
        print("[ATTE] Une erreur est survenue lors de la réinitialisation de la liste des ID Pokémon GO des tricheurs.")

def show_config():
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

    print("=========================================================================================")
    print("                           Configuration actuelle d'Anti-Cheat                           ")
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
    
def show_cheaters_pid():
    with open("lists\\cheaters.json") as json_file:
        data = json.load(json_file)
        for p in data:
            if p["Pseudo*"]:
                print(p["Pseudo*"])

def reset_json():
    res = {
          "CLIENT_ID" : "<CLIENT_ID>",
          "CLIENT_SECRET" : "<CLIENT_SECRET>",
          "TOKEN" : "<TOKEN>",
          "HOST" : "<HOST>",
          "PORT" : "<PORT>",
          "REDIRECT_URL" : "<REDIRECT_URL>",
          "OAUTH_WINDOW" : "SW_MINIMIZE",
          "CHECKER_WINDOW": "SW_MINIMIZE"
          }
    try:
        json_file = open("scripts\\config.json", "w")
        json.dump(res, json_file, indent=4)
        json_file.close()
        print("[INFO] Le fichier de configuration a été réinitialisé.")
    except:
        print("[ATTE] Une erreur est survenue lors de la réinitialisation du fichier de configuration.")

def set(var):
    val = input("Valeur pour " + var + ": ")
    
    json_file = open("scripts\\config.json", "r")
    res = json.load(json_file)
    res[var] = val
    json_file.close()
    
    json_file = open("scripts\\config.json", "w")
    json.dump(res, json_file, indent=4)
    json_file.close()

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
