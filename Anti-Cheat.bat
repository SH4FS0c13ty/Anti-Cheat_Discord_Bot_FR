@echo off
title Anti-Cheat Discord Bot par SH4FS0c13ty
chcp 65001
cls
echo.
echo  █████╗ ███╗   ██╗████████╗██╗       ██████╗██╗  ██╗███████╗ █████╗ ████████╗
echo ██╔══██╗████╗  ██║╚══██╔══╝██║      ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝
echo ███████║██╔██╗ ██║   ██║   ██║█████╗██║     ███████║█████╗  ███████║   ██║   
echo ██╔══██║██║╚██╗██║   ██║   ██║╚════╝██║     ██╔══██║██╔══╝  ██╔══██║   ██║   
echo ██║  ██║██║ ╚████║   ██║   ██║      ╚██████╗██║  ██║███████╗██║  ██║   ██║   
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝       ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   
echo.
echo Anti-Cheat v1.3 (The Masterkiller) par SH4FS0c13ty
echo Un bot Discord qui éjecte les tricheurs d'après leur liste de serveurs et leur ID Pokémon GO.
echo.
echo Tapez "help" pour voir le menu d'aide.

:prompt
echo.
set /p start=Anti-Cheat:~$ 
echo.
if /i "%start%" EQU "exit" exit
if /i "%start%" EQU "help" goto help
if /i "%start%" EQU "about" goto about
if /i "%start%" EQU "license" goto license

if /i "%start%" EQU "start" goto start
if /i "%start%" EQU "stop" goto stop
if /i "%start%" EQU "restart" goto restart

if /i "%start%" EQU "show config" goto show_conf
if /i "%start%" EQU "show blacklist" goto show_bl
if /i "%start%" EQU "show cheaters_lists" goto show_cheaters

if /i "%start%" EQU "reset cheaters_lists" goto reset_cheaters
if /i "%start%" EQU "reset servers_lists" goto reset_servers
if /i "%start%" EQU "reset config" goto reset_conf

if /i "%start%" EQU "set CLIENT_ID" goto set_client_id
if /i "%start%" EQU "set CLIENT_SECRET" goto set_client_secret
if /i "%start%" EQU "set TOKEN" goto set_token
if /i "%start%" EQU "set HOST" goto set_host
if /i "%start%" EQU "set PORT" goto set_port
if /i "%start%" EQU "set REDIRECT_URL" goto set_redirect_url

echo Commande inconnue.

goto prompt

:help
echo Help - Panel de commandes
echo.
echo exit                              Quitter la console d'Anti-Cheat
echo help                              Voir ce menu
echo about                             Voir la section À Propos
echo license                           Voir la licence
echo.
echo start                             Démarrer Anti-Cheat (Bot et serveur web)
echo stop                              Arrêter Anti-Cheat (Bot et serveur web)
echo restart                           Redémarrer Anti-Cheat (Bot et serveur web)
echo.
echo show config                       Voir la configuration
echo show blacklist                    Voir la liste noire
echo show cheaters_lists               Voir les listes de tricheurs [MENU]
echo.
echo reset cheaters_lists              Réinitialiser les listes de tricheurs [MENU]
echo reset servers_lists               Réinitialiser les listes de serveurs
echo reset config                      Réinitialiser le fichier de configuration
echo.
echo set CLIENT_ID                     Définir la valeur OAUTH2_CLIENT_ID dans le fichier de configuration
echo set CLIENT_SECRET                 Définir la valeur OAUTH2_CLIENT_SECRET dans le fichier de configuration
echo set TOKEN                         Définir la valeur BOT_TOKEN dans le fichier de configuration
echo set HOST                          Définir la valeur de l'adresse IP de l'hôte du serveur web
echo set PORT                          Définir le numéro de port du serveur web dans le fichier de configuration
echo set REDIRECT_URL                  Définir la valeur de l'URL pour la redirection dans le fichier de configuration
goto prompt

:about
cls
echo.
echo  █████╗ ███╗   ██╗████████╗██╗       ██████╗██╗  ██╗███████╗ █████╗ ████████╗
echo ██╔══██╗████╗  ██║╚══██╔══╝██║      ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝
echo ███████║██╔██╗ ██║   ██║   ██║█████╗██║     ███████║█████╗  ███████║   ██║   
echo ██╔══██║██║╚██╗██║   ██║   ██║╚════╝██║     ██╔══██║██╔══╝  ██╔══██║   ██║   
echo ██║  ██║██║ ╚████║   ██║   ██║      ╚██████╗██║  ██║███████╗██║  ██║   ██║   
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝       ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   
echo.
echo Anti-Cheat v1.3 (The Masterkiller) by SH4FS0c13ty
echo Un bot Discord qui éjecte les tricheurs d'après leur liste de serveurs et leur ID Pokémon GO.
echo.
echo Ce projet est né sur une demande de 123321mario (http://123321mario.tk/) qui
echo voulait empêcher les tricheurs d'entrer dans des serveurs légitimes de Pokémon GO.
echo Comme j'aime mettre les mains dans le cambouis, j'ai commencé ce projet, l'ai
echo amélioré jusqu'à la dernière version disponible ici :
echo https://github.com/SH4FS0c13ty/Anti-Cheat_Discord_Bot
echo.
scripts\tools.py contact
goto prompt

:license
type LICENSE
goto prompt

:start
python scripts\\main.py scripts\\config.json
goto prompt

:stop
for /F %%q in (scripts\\oauth_pid.txt) do (
	echo Arrêt du module Anti-Cheat OAuth2 avec le PID %%q ...
	taskkill /F /PID:%%q
)
for /F %%p in (scripts\\check_pid.txt) do (
	echo Arrêt du module Anti-Cheat Checker avec le PID %%p ...
	taskkill /F /PID:%%p
)
goto prompt

:restart
echo Redémarrage d'Anti-Cheat ...
for /F %%q in (scripts\\oauth_pid.txt) do (
	echo Arrêt du module Anti-Cheat OAuth2 avec le PID %%q ...
	taskkill /F /PID:%%q
)
for /F %%p in (scripts\\check_pid.txt) do (
	echo Arrêt du module Anti-Cheat Checker avec le PID %%p ...
	taskkill /F /PID:%%p
)
echo.
python scripts\\main.py scripts\\config.json
goto prompt

:show_conf
python scripts\\tools.py show_config
goto prompt

:show_bl
type lists\\blacklist.txt
goto prompt

:show_cheaters
cls
echo.
echo Menu des listes de tricheurs
echo ============================
echo.
echo 1 - Voir les IDs Discord des tricheurs
echo 2 - Voir les IDs Pokémon GO des tricheurs
echo 3 - Voir les IDs associés des tricheurs
echo.
echo 0 - Quitter ce menu
echo.
set /p menu1=Entrez un chiffre [0~3]:~$ 
echo.
if /i "%menu1%" EQU "0" cls && goto prompt
if /i "%menu1%" EQU "1" goto show_cheaters_did
if /i "%menu1%" EQU "2" goto show_cheaters_pid
if /i "%menu1%" EQU "3" goto show_cheaters_aid

echo Chiffre inconnu.

goto show_cheaters

:show_cheaters_did
echo IDs Discord des tricheurs
echo =========================
echo.
type lists\\cheaters_ids
echo.
pause
goto show_cheaters

:show_cheaters_pid
echo IDs Pokémon GO des tricheurs
echo ============================
echo.
python scripts\\tools.py show_cheaters_pid
pause
goto show_cheaters

:show_cheaters_aid
echo IDs associés des tricheurs
echo ==========================
echo.
type lists\\Associated_IDs.txt
echo.
pause
goto show_cheaters

:reset_cheaters
cls
echo.
echo Menu des listes de tricheurs
echo ============================
echo.
echo 1 - Réinitialiser les IDs Discord des tricheurs
echo 2 - Réinitialiser les IDs Pokémon GO des tricheurs
echo 3 - Réinitialiser les IDs associés des tricheurs
echo.
echo 0 - Quitter ce menu
echo.
set /p menu2=Entrez un chiffre [0~3]:~$ 
echo.
if /i "%menu2%" EQU "0" cls && goto prompt
if /i "%menu2%" EQU "1" goto reset_cheaters_did
if /i "%menu2%" EQU "2" goto reset_cheaters_pid
if /i "%menu2%" EQU "3" goto reset_cheaters_aid

echo Unknown number.

goto reset_cheaters

:reset_cheaters_did
del /Q lists\\cheaters_ids
echo.
echo Liste des IDs Discord de tricheurs supprimée.
echo.
pause
goto reset_cheaters

:reset_cheaters_pid
del /Q lists\\cheaters.json
echo.
echo Liste des IDs Pokémon GO de tricheurs supprimée.
echo.
pause
goto reset_cheaters

:reset_cheaters_aid
del /Q lists\\Associated_IDs.txt
echo.
echo Liste des IDs associés de tricheurs supprimée.
echo.
pause
goto reset_cheaters

:reset_servers
del /Q servers_lists\\*
echo Les listes des serveurs ont été supprimées.
goto prompt

:reset_conf
echo Réinitialisation du fichier de configuration ...
scripts\\tools.py reset_json
goto prompt

:set_client_id
echo La valeur de CLIENT_ID doit être un nombre.
echo.
scripts\\tools.py set CLIENT_ID
goto prompt

:set_client_secret
scripts\\tools.py set CLIENT_SECRET
goto prompt

:set_token
scripts\\tools.py set TOKEN
goto prompt

:set_host
echo La valeur de HOST doit être quelque chose comme XXX.XXX.XXX.XXX (le nombre de X n'importe pas).
echo.
scripts\\tools.py set HOST
goto prompt

:set_port
echo La valeur de PORT doit être un nombre.
echo.
scripts\\tools.py set PORT
goto prompt

:set_redirect_url
scripts\\tools.py set REDIRECT_URL
goto prompt