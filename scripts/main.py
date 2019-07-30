import subprocess, sys, json

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

print("Démarrage d'Anti-Cheat avec les paramètres suivants ...")
print("=========================================================================================")
print("ID_CLIENT :           " + CLIENT_ID)
print("SECRET_CLIENT :       " + CLIENT_SECRET)
print("JETON :               " + TOKEN)
print("HÔTE :                " + HOST)
print("PORT :                " + PORT)
print("URL_REDIRECTION :     " + REDIRECT_URL)
print("=========================================================================================\n")

SW_MINIMIZE = 6
info = subprocess.STARTUPINFO()
info.dwFlags = subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = SW_MINIMIZE

pid = subprocess.Popen(args=["python", "scripts\\oauth.py", CLIENT_ID, CLIENT_SECRET, HOST, PORT, REDIRECT_URL], creationflags=NEW_CONSOLE, startupinfo=info).pid
print("Module Anti-Cheat OAauth2 démarré avec le PID " + str(pid) + " avec une console réduite.")

f = open("scripts\\oauth_pid.txt", "w")
f.write(str(pid))
f.close()

pid2 = subprocess.Popen(args=["python", "scripts\\check.py", TOKEN], creationflags=NEW_CONSOLE, startupinfo=info).pid
print("Module Anti-Cheat Checker démarré avec le PID " + str(pid2) + " avec une console réduite.")

f = open("scripts\\check_pid.txt", "w")
f.write(str(pid2))
f.close()
