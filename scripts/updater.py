import itertools, threading, time, sys, subprocess, json, os, traceback
import tools, colorama, hashlib
from colorama import Fore, Style
import shutil
from shutil import copyfile

colorama.init()
arg = sys.argv[1]

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def updating():
    global done
    for c in itertools.cycle(['.  ', '.. ', '...']):
        if done:
            break
        sys.stdout.write('\rUpdating Anti-Cheat ' + c)
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\rUpdating Anti-Cheat ...\n')

def update(url):
    try:
        global done
        global new_checksum
        done = False

        t = threading.Thread(target=updating)
        t.start()

        tools.log("[INFO] Téléchargement de la nouvelle version d'Anti-Cheat version depuis " + url)
        dl = subprocess.Popen(args=["setup\\curl.exe", "-s", "-f", "-k", "--output", "Anti-Cheat_FR.zip", url])
        dl.wait()
        
        if sha256sum("Anti-Cheat_FR.zip").lower() == new_checksum.lower():
            tools.log("[INFO] Somme vérifiée pour Anti-Cheat_FR.zip: " + new_checksum)
            tools.log("[INFO] Extraction de l'archive Anti-Cheat_FR.zip ...")
            extract = subprocess.Popen(args=["setup\\7z.exe", "x", "Anti-Cheat_FR.zip", "-bb3", "-r"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            extract.wait()
            dir = os.getcwd()
            tools.log("[INFO] Suppression du nouveau fichier config.json par défaut.")
            os.remove(dir + "\\Anti-Cheat_Discord_Bot-master\\scripts\\config.json")
            tools.log("[INFO] Copie du nouveau dossier : Anti-Cheat_Discord_Bot-master/licenses.")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master\\licenses"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir + "\\licenses")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\licenses")
            tools.log("[INFO] Suppression du nouveau dossier : Anti-Cheat_Discord_Bot-master/licenses.")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\lists")
            tools.log("[INFO] Suppression du nouveau dossier : Anti-Cheat_Discord_Bot-master/lists.")
            tools.log("[INFO] Copie du nouveau dossier : Anti-Cheat_Discord_Bot-master/scripts.")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master\\scripts"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir + "\\scripts")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\scripts")
            tools.log("[INFO] Suppression du nouveau dossier : Anti-Cheat_Discord_Bot-master/scripts.")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\servers_lists")
            tools.log("[INFO] Suppression du nouveau dossier : Anti-Cheat_Discord_Bot-master/servers_lists.")
            tools.log("[INFO] Copie du nouveau dossier : Anti-Cheat_Discord_Bot-master/setup.")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master\\setup"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir + "\\setup")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\setup")
            tools.log("[INFO] Suppression du nouveau dossier : Anti-Cheat_Discord_Bot-master/setup.")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\user_ids")
            tools.log("[INFO] Suppression du nouveau dossier : Anti-Cheat_Discord_Bot-master/user_ids.")
            tools.log("[INFO] Copie du nouveau dossier : Anti-Cheat_Discord_Bot-master/")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir)
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master")
            tools.log("[INFO] Suppression du nouveau dossier : Anti-Cheat_Discord_Bot-master/")
            tools.log("[INFO] Installation des nouvelles dépendances Python ...")
            pysetup = subprocess.Popen(args=["python", "-m", "pip", "-r", "setup\\requirements.txt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            pysetup.wait()
            tools.log("[INFO] Anti-Cheat a été mis à jour.")
            print("[INFO] Anti-Cheat a été mis à jour.\n\nVeuillez fermer cette fenêtre sans utiliser la commande exit et redémarrer la console principale d'Anti-Cheat.")
            while True:
                time.sleep(1)
        else:
            done = True
            time.sleep(0.5)
            print(Fore.RED + Style.BRIGHT + "[WARN] Somme incorrecte. Le fichier peut être corrompu ou altéré." + Style.RESET_ALL)
            print("[INFO] Abandon de la mise à jour.")
            tools.log("[WARN] Somme incorrecte. Le fichier peut être corrompu ou altéré.")
            tools.log("[INFO] Abandon de la mise à jour.")
        os.remove("Anti-Cheat_FR.zip")
        time.sleep(1)
        done = True
    except KeyboardInterrupt:
        done = True
        os.remove("updates.json")
        return
    except Exception as e:
        done = True
        time.sleep(0.5)
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenue lors de la mise à jour. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[WARN] Une erreur est survenue lors de la mise à jour.")
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())


def check_updates(command):
    try:
        name = "Anti-Cheat FR"
        version = "v1.4.0"
        date = "04/09/19"

        print("Vérification des mises à jour ...")
        tools.log("[INFO] Vérification des mises à jour ...")
        check = subprocess.Popen(args=["setup\\curl.exe", "-s", "-f", "-k", "--output", "updates.json", "https://sh4fs0c13ty.tk/updates/updates.json"])
        check.wait()
        with open("updates.json") as json_file:
            data = json.load(json_file)
            for p in data:
                if "Anti-Cheat FR" == p['App']:
                    new_version = p['Version']
                    new_codename = p['Codename']
                    new_url = p['Link']
                    new_date = p['Release date']
                    global new_checksum
                    new_checksum = p['Checksum']
            if version < new_version:
                if date < new_date:
                    if command == "update":
                        update(new_url)
                    elif command == "check":
                        print("Une nouvelle mise à jour est disponible : Anti-Cheat " + new_version + " (" + new_codename + ") publiée le " + new_date + ".")
                        print("Veuillez utiliser la commande \"update\" pour mettre à jour vers la nouvelle version.")
                        tools.log("[INFO] Une nouvelle mise à jour est disponible : Anti-Cheat " + new_version + " (" + new_codename + ") publiée le " + new_date + ".")
                else:
                    print("Vous avez déjà la dernière version d'Anti-Cheat !")
                    tools.log("[INFO] Aucune nouvelle mise à jour trouvée.")
            else:
                print("Vous avez déjà la dernière version d'Anti-Cheat !")
                tools.log("[INFO] Aucune nouvelle mise à jour trouvée.")
    except KeyboardInterrupt:
        os.remove("updates.json")
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur est survenue pendant la recherche de mises à jour. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[WARN] Une erreur est survenue pendant la recherche de mises à jour.")
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        os.remove("updates.json")

if arg == "update":
    check_updates(arg)
elif arg == "check":
    check_updates(arg)
else:
    print("Argument invalide.")
    
os.remove("updates.json")