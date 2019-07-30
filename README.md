# Anti-Cheat Discord Bot
Anti-Cheat v1.3 (The Masterkiller) par SH4FS0c13ty<br />
Un bot Discord qui éjecte les tricheurs d'après leur liste de serveurs et leur ID Pokémon GO.<br />
<br />
English version : https://github.com/SH4FS0c13ty/Anti-Cheat_Discord_Bot
<br />

## Dépendances

Les dépendances ci-dessous peuvent être installées en exécutant "Anti-Cheat Requirements Installer.bat".<br />
Voir la section Installation section pour en savoir plus.<br />
 - Windows 10
 - [Python 3.7.4](https://www.python.org/downloads/release/python-374/)
 - [Tesseract OCR](https://opensource.google.com/projects/tesseract)

## Installation

Exécutez "Anti-Cheat Requirements Installer.bat" et sélectionnez l'installation correspondant à votre système.
<br />
L'installation va commencer et aucune autre action n'est requise.
<br />

## Utilisation

Exécutez "Anti-Cheat.bat" et entrez la commande que vous voulez utiliser.<br />

### Panel de commandes<br />
Processus Anti-Cheat :<br />
`start|stop|restart`<br />
Voir les listes et la configuration d'Anti-Cheat :<br />
`show config|blacklist|cheaters_lists`<br />
Réinitialiser les listes et la configuration d'Anti-Cheat :<br />
`reset config|cheaters_lists|servers_lists`<br />
Définir la configuration d'Anti-Cheat :<br />
`set CLIENT_ID|CLIENT_SECRET|TOKEN|HOST|PORT`<br />
<br />
### Fiichiers utilisés<br />
Fichier de configuration :<br />
`scripts/config.json`<br />
Liste noire des serveurs :<br />
`lists/blacklist.txt`<br />
Liste des IDs Pokémon Go des tricheurs (voir le modèle inclus):<br />
`lists/cheaters.xlsx`<br />
Les des IDs Discord des tricheurs :<br />
`lists/cheaters_id.txt`<br />
Listes des IDs associés des tricheurs (<ID_POKEMON_GO>:<ID_DISCORD>):<br />
`lists/Associated_IDs.txt`<br />
Listes des serveurs des utilisateurs :<br />
`server_lists/<DISCORD_ID>.txt`<br />
<br />
N'oubliez pas de configurer Anti-Cheat avant de l'utiliser !<br />
Pour le configurer, modifiez le fichier "config.json" ou utilisez la commande `set <PARAM>`.<br />
Vous devez aussi modifier les fichiers "blacklist.txt et "cheaters.xlsx" pour le faire fonctionner correctement.<br />
<br />
### Commandes du bot
 - ./verify <URL_IMAGE_OU_IMAGE_INCLUSE>
 - ./kick <NOM_UTILISATEUR>
 - ./recheck <NOM_UTILISATEUR>
 
## Licence

Licence MIT (https://opensource.org/licenses/mit-license.php)<br />

Copyright (c) 2019 SH4FS0c13ty & 123321mario<br />

Par les présentes, la permission est accordée, sans frais, à toute personne obtenant une copie de ce<br />
logiciel et des fichiers de documentation associés (le " Logiciel "), d'utiliser le Logiciel sans<br />
restriction, y compris, sans limitation, les droits d'utiliser, copier, modifier, fusionner, publier,<br />
distribuer, sous-licencier et/ou vendre des copies du Logiciel, et d'en permettre l'utilisation aux<br />
personnes auxquelles il est fourni, sous réserve des conditions suivantes :<br />

L'avis de droit d'auteur ci-dessus et cet avis d'autorisation doivent être inclus dans toutes les<br />
copies ou parties substantielles du Logiciel.<br />

LE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE, EXPRESSE OU IMPLICITE, Y COMPRIS,<br />
MAIS SANS S'Y LIMITER, LES GARANTIES DE QUALITÉ MARCHANDE, D'ADAPTATION À UN USAGE PARTICULIER ET DE<br />
NON-CONTREFAÇON. EN AUCUN CAS, LES AUTEURS OU LES DÉTENTEURS DE DROITS D'AUTEUR NE PEUVENT ÊTRE TENUS<br />
RESPONSABLES DE TOUTE RÉCLAMATION, DOMMAGE OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS LE CADRE D'UNE<br />
ACTION EN RESPONSABILITÉ CONTRACTUELLE, DÉLICTUELLE OU AUTRE, DÉCOULANT DU LOGICIEL OU DE L'UTILISATION<br />
OU D'AUTRES TRANSACTIONS DU LOGICIEL OU EN RAPPORT AVEC CELUI-CI.<br />
<br />

## Credits

Auteurs :
<br />
SH4FS0c13ty (Site web : https://sh4fs0c13ty.tk/ , Twitter : @SH4FS0c13ty, Discord : SH4FS0c13ty#1562, Github : https://github.com/SH4FS0c13ty)<br />
123321mario (Site web : http://123321mario.tk/ , Twitter : @123321mario, Discord : 123321mario#1337, Github : https://github.com/123321mario)<br />
<br />
Merci à Stanislav Vishnevskiy pour son module Discord OAuth2 (https://github.com/discordapp/discord-oauth2-example)