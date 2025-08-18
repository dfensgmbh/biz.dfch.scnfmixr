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


class StateEventFr(dict[StateEvent, str]):
    """Texts for FR state event messages."""

    StateEvent.INITIALISE_LCL_ENTER = """
Menu "initialiser le périphérique local"

Sélectionnez "1" pour la détection des périphériques.
Sélectionnez "2" pour ignorer la détection des périphériques.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_HI1_ENTER = """
Menu "initialisation du périphérique d'entrée numéro 1"

Sélectionnez "1" pour lancer la détection du périphérique.
Sélectionnez "2" pour ignorer la détection du périphérique.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.SELECT_LANGUAGE_ENTER = """
Menu "séléction de la langue"

Press "1" for english.
Wählen Sie "2" für deutsch.
Sélectionnez "3" pour le français.
Scegliere "4" por italiano.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_EX1_ENTER = """
Menu "initialisier le périférique externe numéro 1"

Sélectionnez "1" pour lancer la détection du périphérique.
Sélectionnez "2" pour ignorer la détection du périphérique.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_EX2_ENTER = """
Menu "initialisier le périphérique externe numéro 2"

Sélectionnez "1" pour lancer la détection du périphérique.
Sélectionnez "2" pour ignorer la détection du périphérique.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_RC1_ENTER = """
Menu "initialiser le périphérique de mémoire numéro 1"

Sélectionnez "1" pour détecter le périphérique.
Sélectionnez "2" pour ignorer la détection du périphérique.
Sélectionnez "6" pour formater le périphérique.
Sélectionnez "7" pour connecter le périphérique
Sélectionnez "8" pour déconnecter le périphérique.
Sélectionnez "9" pour effacer le périphérique.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.INITIALISE_RC2_ENTER = """
Menu "initialiser le périphérique de mémoire numéro 2"

Sélectionnez "1" pour détecter le périphérique.
Sélectionnez "2" pour ignorer la détection du périphérique.
Sélectionnez "6" pour formater le périphérique.
Sélectionnez "7" pour connecter le périphérique.
Sélectionnez "8" pour déconnecter le périphérique.
Sélectionnez "9" pour effacer le périphérique.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.SET_DATE_ENTER = """
Le menu "Date"

Entrez une date à 8 chiffres en commençant par les 4 chiffres de l'année, suivis des 2 chiffres du mois et des 2 chiffres du jour.

Pour supprimer un chiffre, Sélectionnez la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, Sélectionnez la touche "ENTER" ou "ENTRÉE".

Exemple :

un-neuf-deux-sept

zéro-trois-deux-sept pour le 27 mars 1927.

Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.SET_TIME_ENTER = """
Le menu "Heure"

Entrez une heure à 4 chiffres en commençant par les 2 chiffres des heures, suivis des 2 chiffres des minutes.

Pour supprimer un chiffre, Sélectionnez la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, Sélectionnez la touche "ENTER" ou "ENTRÉE".

Exemple :

un-quatre-zéro-trois pour 2 heures et 3 minutes de l'après-midi.

Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    # OK
    StateEvent.SET_NAME_ENTER = """
Le menu "Nom"

Entrez un nom à 8 chiffres qui servira de nom unique dans votre enregistrement.

Pour supprimer un chiffre, Sélectionnez la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, Sélectionnez la touche "ENTER" ou "ENTRÉE".

Exemple :

zéro-huit-un-cinq

cinq-six-quatre-deux pour zéro-huit 15 56 42.

Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.MAIN_ENTER = """
Le menu "Principal"

Sélectionnez "1" pour démarrer un enregistrement stéréo.
Sélectionnez "2" pour démarrer un enregistrement "dry iso" et un enregistrement stéréo.
Sélectionnez "3" pour démarrer un enregistrement "wet iso", un enregistrement "dry iso" et un enregistrement stéréo.
Sélectionnez "4" pour démarrer la lecture.
Sélectionnez "5" pour accéder au menu "Système".
Sélectionnez "6" pour attribuer un nouveau nom à votre prochain enregistrement.
Sélectionnez "9" pour arrêter l'appareil.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.

"""  # noqa: E501

    StateEvent.SYSTEM_ENTER = """
Le menu "Système"

Sélectionnez "1" pour accéder au menu "Principal".
Sélectionnez "2" pour sélectionner la langue.
Sélectionnez "3" pour accéder au menu "Mémoire".
Sélectionnez "4" pour sélectionner la date.
Sélectionnez "5" pour sélectionner l'heure.
Sélectionnez "9" pour arrêter l'appareil.
Sélectionnez "ASTÉRISQUE" pour répéter ce message.
"""  # noqa: E501

    StateEvent.INIT_AUDIO_LEAVE = """
Système audio entièrement initialisé.
"""  # noqa: E501
