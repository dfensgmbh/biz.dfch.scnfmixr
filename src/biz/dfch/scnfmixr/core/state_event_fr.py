# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module state_event_fr."""

from .state_event import StateEvent


class StateEventEn(dict[StateEvent, str]):
    """Texts for FR state events messages."""

    StateEvent.INITIALISE_LCL_ENTER = """
Menu "initialiser le périphérique local"

Appuyez sur «1» pour la détection des périphériques.
Appuyez sur «2» pour ignorer la détection des périphériques.
Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_HI1_ENTER = """
Menu «initialisation du périphérique d'entrée n° 1»

Appuyez sur «1» pour lancer la détection du périphérique.
Appuyez sur «2» pour ignorer la détection du périphérique.
Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.SELECT_LANGUAGE_ENTER = """
Menu "séléction de la langue"

Press "1" for english.
Drücken Sie "2" für deutsch.
Selectionner "3" pour le français.
Scegliere "4" por italiano.
Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_EX1_ENTER = """
Menu "initialisier le périférique externe n° 1"

Appuyez sur «1» pour lancer la détection du périphérique.
Appuyez sur «2» pour ignorer la détection du périphérique.
Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_EX2_ENTER = """
Menu "initialisier le périphérique externe n° 2"

Appuyez sur «1» pour lancer la détection du périphérique.
Appuyez sur «2» pour ignorer la détection du périphérique.
Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_RC1_ENTER = """
Menu «initialiser le périphérique de mémoire n° 1»  

Appuyez sur «1» pour détecter le périphérique. 
Appuyez sur «2» pour ignorer la détection du périphérique. 
Appuyez sur «6» pour formater le périphérique. 
Appuyez sur «7» pour connecter le périphérique. 
Appuyez sur «8» pour déconnecter le périphérique. 
Appuyez sur «9» pour effacer le périphérique. 
Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_RC2_ENTER = """
Menu «initialiser le périphérique de mémoire n° 2»  

Appuyez sur «1» pour détecter le périphérique. 
Appuyez sur «2» pour ignorer la détection du périphérique. 
Appuyez sur «6» pour formater le périphérique. 
Appuyez sur «7» pour connecter le périphérique. 
Appuyez sur «8» pour déconnecter le périphérique. 
Appuyez sur «9» pour effacer le périphérique. 
Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.SET_DATE_ENTER = """
Le menu «Date»

Entrez une date à 8 chiffres en commençant par les 4 chiffres de l'année, suivis des 2 chiffres du mois et des 2 chiffres du jour.

Pour supprimer un chiffre, appuyez sur la touche «BACK-SPACE» ou «RETOUR ARRIÈRE».
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, appuyez sur la touche «ENTER» ou «ENTRÉE».

Exemple :

un-neuf-deux-sept

zéro-trois-deux-sept pour le 27 mars 1927.

Appuyez sur «ASTÉRISQUE» pour répéter ce message.
"""  # noqa: E501

    StateEvent.SET_TIME_ENTER = """
Le menu "Heure"

Entrez une heure à 4 chiffres en commençant par les 2 chiffres des heures, suivis des 2 chiffres des minutes.

Pour supprimer un chiffre, appuyez sur la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, appuyez sur la touche "ENTER" ou "ENTRÉE".

Exemple :

un-quatre-zéro-trois pour 2 heures et 3 minutes de l'après-midi.

Appuyez sur "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    # OK
    StateEvent.SET_NAME_ENTER = """
Le menu "Nom"

Entrez un nom à 8 chiffres qui servira de nom unique dans votre enregistrement.

Pour supprimer un chiffre, appuyez sur la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, appuyez sur la touche "ENTER" ou "ENTRÉE".

Exemple :

zéro-huit-un-cinq

cinq-six-quatre-deux pour 08 15 56 42.

Appuyez sur "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.MAIN_ENTER = """
Le menu "Principal"

Appuyez sur "1" pour démarrer un enregistrement stéréo.
Appuyez sur "2" pour démarrer un enregistrement dry iso et un enregistrement stéréo.
Appuyez sur "3" pour démarrer un enregistrement wet iso, un enregistrement dry iso et un enregistrement stéréo.
Appuyez sur "4" pour démarrer la lecture.
Appuyez sur "5" pour accéder au menu "Système".
Appuyez sur "6" pour attribuer un nouveau nom à votre prochain enregistrement.
Appuyez sur "9" pour arrêter l'appareil.
Appuyez sur "ASTÉRISQUE" pour répéter ce message. 

"""  # noqa: E501

    StateEvent.SYSTEM_ENTER = """
Le menu «Système»  

Appuyez sur «1» pour accéder au menu «Principal».
Appuyez sur «2» pour sélectionner la langue.
Appuyez sur «3» pour accéder au menu «Mémoire».
Appuyez sur «4» pour sélectionner la date.
Appuyez sur «5» pour sélectionner l'heure.
Appuyez sur «9» pour arrêter l'appareil.
Appuyez sur «ASTÉRISQUE» pour répéter ce message.  
"""  # noqa: E501
