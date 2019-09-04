import pytesseract, os, sys, traceback
import tools
from PIL import Image
import colorama
from colorama import Fore, Style

colorama.init()

def getid(file, userid):
    try:
        global filename
        filename = file
        ocr_result = ocr_core(file)
        if ocr_result.find("&") != -1:
            pokeid = text_process(ocr_result, userid)
        elif ocr_result.find("PROGRESDELASEMAINE") != -1:
            pokeid = text_processfr(ocr_result, userid, 1)
        elif ocr_result.find("PROGRSDELASEMAINE") != -1:
            pokeid = text_processfr(ocr_result, userid, 2)
        else:
            pokeid = "ERROR"
        os.remove(file)
        return pokeid
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def ocr_core(filename):
    try:
        print("[INFO] " + "OCR en cours ...")
        tools.log("[INFO] " + "OCR en cours ...")
        text = pytesseract.image_to_string(Image.open(filename), lang="ita", config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789&")
        return text
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def text_process(text, userid):
    try:
        sep = "&"
        rest = text.split(sep, 1)[0]

        file=open("user_ids\\" + userid + ".txt", "w")
        file.write(rest)
        file.close()

        file = open("user_ids\\" + userid + ".txt", "r")
        lastl = list(file)[-1]
        file.close()

        file = open("user_ids\\" + userid + ".txt", "w")
        file.write(lastl)
        file.close()
        
        file = open("user_ids\\" + userid + ".txt", "r")
        lines = file.read().splitlines()
        file.close()
        
        last_line = lastl

        if "\n" in last_line:
            sep = "\n"
            last_line = last_line.split(sep, 1)[0]
        else:
            pass

        if " " in last_line:
            tools.log("[INFO] " + "Résultat de l'OCR : " + last_line)
            print(Fore.RED + Style.BRIGHT + "[WARN] Espace détecté dans le nom d'utilisateur. Des erreurs peuvent découler des procédures suivantes." + Style.RESET_ALL)
            tools.log("[WARN] Espace détecté dans le nom d'utilisateur. Des erreurs peuvent découler des procédures suivantes.")
            last_line = fallback(userid, 2)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(last_line)
            file.close()
        else:
            print("[INFO] " + "Résultat de l'OCR : " + last_line)
            tools.log("[INFO] " + "Résultat de l'OCR : " + last_line)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(last_line)
            file.close()
        return last_line
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        return "ERROR"

def text_processfr(text, userid, idsep):
    try:
        if idsep == 1:
            sep = "PROGRESDELASEMAINE"
        if idsep == 2:
            sep = "PROGRSDELASEMAINE"
        
        rest = text.split(sep, 1)[0]
        
        file=open("user_ids\\" + userid + ".txt", "w")
        file.write(rest)
        file.close()
        
        file = open("user_ids\\" + userid + ".txt", "r")
        lines = file.read().splitlines()
        last_line = lines[-1]
        file.close()
        
        while last_line.find("et") == -1:
            lines = lines[:-1]
            last_line = lines[-1]
        
        lines = lines[:-1]
        last_line = lines[-1]

        if last_line != "":
            pass
        else:
            lines = lines[:-1]
            last_line = lines[-1]
        
        if " " in last_line:
            tools.log("[INFO] " + "Résultat de l'OCR : " + last_line)
            print(Fore.RED + Style.BRIGHT + "[WARN] Espace détecté dans le nom d'utilisateur. Des erreurs peuvent découler des procédures suivantes." + Style.RESET_ALL)
            tools.log("[WARN] Espace détecté dans le nom d'utilisateur. Des erreurs peuvent découler des procédures suivantes.")
            last_line = fallback(userid, 1)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(last_line)
            file.close()
        else:
            print("[INFO] " + "Résultat de l'OCR : " + last_line)
            tools.log("[INFO] " + "Résultat de l'OCR : " + last_line)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()
        return last_line
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        return "ERROR"

def fallback(userid, method):
    try:
        global filename
        print("[INFO] Utilisation de la fonction de secours pour détecter le nom d'utilisateur.")
        tools.log("[INFO] Utilisation de la fonction de secours pour détecter le nom d'utilisateur.")

        text = os.popen("tesseract -l ita " + filename + " stdout quiet").read()
        
        if method == 1:
            sep = "PROGRÃˆS DE LA SEMAINE"
            rest = text.split(sep, 1)[0]

            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()

            file = open("user_ids\\" + userid + ".txt", "r")
            lines = file.read().splitlines()
            last_line = lines[-1]

            while last_line.find("et") == -1:
                lines = lines[:-1]
                last_line = lines[-1]

            lines = lines[:-1]
            last_line = lines[-1]

            if last_line != "":
                pass
            else:
                lines = lines[:-1]
                last_line = lines[-1]

            if " " in last_line:
                sep = " "
                rest = last_line.split(sep, 1)[0]

            print("[INFO] " + "Résultat de l'OCR de secours : " + rest)
            tools.log("[INFO] " + "Résultat de l'OCR de secours: " + rest)
            return rest
        elif method == 2:
            sep = "&"
            rest = text.split(sep, 1)[0]

            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()

            file = open("user_ids\\" + userid + ".txt", "r")
            lastl = list(file)[-1]
            file.close()

            file = open("user_ids\\" + userid + ".txt", "w")
            file.write(lastl)
            file.close()
            
            file = open("user_ids\\" + userid + ".txt", "r")
            lines = file.read().splitlines()
            file.close()

            last_line = lastl

            if "\n" in last_line:
                sep = "\n"
                last_line = last_line.split(sep, 1)[0]
            else:
                pass

            if " " in last_line:
                sep = " "
                rest = last_line.split(sep, 1)[0]

            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()

            print("[INFO] " + "Résultat de l'OCR de secours: " + rest)
            tools.log("[INFO] " + "Résultat de l'OCR de secours: " + rest)
            return rest
        else:
            print(Fore.RED + Style.BRIGHT + "[WARN] Méthode de secours incorrect. Abandon." + Style.RESET_ALL)
            tools.log("[WARN] Méthode de secours incorrecte. Abandon.")
            return "ERROR"
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] Une erreur inconnue est survenue. Veuillez vérifier les fichiers Anti-Cheat.log et Anti-Cheat_traceback.log pour en savoir plus." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        return "ERROR"
