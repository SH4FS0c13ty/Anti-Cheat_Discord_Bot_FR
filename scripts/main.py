import subprocess, sys, json, traceback
import tools
import colorama
from colorama import Fore, Style

try:
    arg = sys.argv[1]

    NEW_CONSOLE = 0x00000010

    json_file = open(arg)
    res = json.load(json_file)

    CLIENT_ID = res["CLIENT_ID"]
    CLIENT_SECRET = res["CLIENT_SECRET"]
    TOKEN = res["TOKEN"]
    HOST = res["HOST"]
    PORT = res["PORT"]
    REDIRECT_URL = res["REDIRECT_URL"]
    OAUTH_WINDOW = res["OAUTH_WINDOW"]
    CHECKER_WINDOW = res["CHECKER_WINDOW"]

    print("Démarrage d'Anti-Cheat avec les paramètres suivants ...\n")
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
    print("=========================================================================================\n")
    
    tools.log("NEW_SESSION")
    tools.log("Démarrage d'Anti-Cheat avec les paramètres suivants ...\n")
    tools.log("=========================================================================================")
    tools.log("                                 Paramètres fonctionnels                                 ")
    tools.log("=========================================================================================")
    tools.log(" CLIENT_ID:            " + CLIENT_ID)
    tools.log(" CLIENT_SECRET:        " + CLIENT_SECRET)
    tools.log(" TOKEN:                " + TOKEN)
    tools.log(" HOST:                 " + HOST)
    tools.log(" PORT:                 " + PORT)
    tools.log(" REDIRECT_URL:         " + REDIRECT_URL)
    tools.log("=========================================================================================")
    tools.log("                                 Paramètres des fenêtres                                 ")
    tools.log("=========================================================================================")
    tools.log(" OAUTH_WINDOW:         " + OAUTH_WINDOW)
    tools.log(" CHECKER_WINDOW:       " + CHECKER_WINDOW)
    tools.log("=========================================================================================\n")

    SW_HIDE = 0
    SW_MINIMIZE = 6
    SW_MAXIMIZE = 3
    SW_SHOW = 5

    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_MINIMIZE

    if OAUTH_WINDOW == "SW_HIDE":
        info.wShowWindow = SW_HIDE
    if OAUTH_WINDOW == "SW_MINIMIZE":
        info.wShowWindow = SW_MINIMIZE
    if OAUTH_WINDOW == "SW_MAXIMIZE":
        info.wShowWindow = SW_MAXIMIZE
    if OAUTH_WINDOW == "SW_SHOW":
        info.wShowWindow = SW_SHOW

    info2 = subprocess.STARTUPINFO()
    info2.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info2.wShowWindow = SW_MINIMIZE

    if CHECKER_WINDOW == "SW_HIDE":
        info2.wShowWindow = SW_HIDE
    if CHECKER_WINDOW == "SW_MINIMIZE":
        info2.wShowWindow = SW_MINIMIZE
    if CHECKER_WINDOW == "SW_MAXIMIZE":
        info2.wShowWindow = SW_MAXIMIZE
    if CHECKER_WINDOW == "SW_SHOW":
        info2.wShowWindow = SW_SHOW

    pid = subprocess.Popen(args=["python", "scripts\\oauth.py", CLIENT_ID, CLIENT_SECRET, HOST, PORT, REDIRECT_URL], creationflags=NEW_CONSOLE, startupinfo=info).pid
    print("Module Anti-Cheat OAauth2 démarré avec le PID " + str(pid) + ".")
    tools.log("[INFO] Module Anti-Cheat OAauth2 démarré avec le PID " + str(pid) + ".")

    f = open("scripts\\oauth_pid.txt", "w")
    f.write(str(pid))
    f.close()

    pid2 = subprocess.Popen(args=["python", "scripts\\check.py", TOKEN], creationflags=NEW_CONSOLE, startupinfo=info2).pid
    print("Module Anti-Cheat Checker démarré avec le PID " + str(pid2) + ".")
    tools.log("[INFO] Module Anti-Cheat Checker démarré avec le PID " + str(pid2) + ".")

    f = open("scripts\\check_pid.txt", "w")
    f.write(str(pid2))
    f.close()
except KeyboardInterrupt:
    exit
except Exception as e:
    tools.log("[ERRO] " + str(e))
    tools.log_traceback(traceback.format_exc())
    print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
