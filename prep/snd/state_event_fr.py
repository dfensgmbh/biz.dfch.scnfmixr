# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Texts for FR state event messages."""

# cSpell:disable

from biz.dfch.scnfmixr.core.state_event import StateEvent


StateEventFr: dict[StateEvent, str] = {

    # OK
    StateEvent.INITIALISE_LCL_ENTER: """
Menu "initialiser le périphérique local"

Appuyez sur "1" pour lancer la détection des périphériques.
Appuyez sur "2" pour ignorer la détection des périphériques.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_LCL_LEAVE: """""",  # noqa: E501

    StateEvent.INITIALISE_HI1_ENTER: """
Menu "initialisation du périphérique d'entrée numéro 1"

Appuyez sur "1" pour lancer la détection du périphérique.
Appuyez sur "2" pour ignorer la détection du périphérique.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_HI1_LEAVE: """""",  # noqa: E501

    # OK
    StateEvent.SELECT_LANGUAGE_ENTER: """
Menu "sélection de la langue"

Press "1" for english.
Wählen Sie "2" für deutsch.
Appuyez sur "3" pour le français.
Scegliere "4" per italiano.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_EX1_ENTER: """
Menu "initialiser le périphérique externe numéro 1"

Appuyez sur "1" pour lancer la détection du périphérique.
Appuyez sur "2" pour ignorer la détection du périphérique.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_EX2_ENTER: """
Menu "initialiser le périphérique externe numéro 2"

Appuyez sur "1" pour lancer la détection du périphérique.
Appuyez sur "2" pour ignorer la détection du périphérique.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_RC1_ENTER: """
Menu "initialiser le périphérique de mémoire numéro 1"

Appuyez sur "1" pour détecter le périphérique.
Appuyez sur "2" pour ignorer la détection du périphérique.
Appuyez sur "6" pour formater le périphérique.
Appuyez sur "7" pour connecter le périphérique.
Appuyez sur "8" pour déconnecter le périphérique.
Appuyez sur "9" pour effacer le périphérique.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_RC2_ENTER: """
Menu "initialiser le périphérique de mémoire numéro 2"

Appuyez sur "1" pour détecter le périphérique.
Appuyez sur "2" pour ignorer la détection du périphérique.
Appuyez sur "6" pour formater le périphérique.
Appuyez sur "7" pour connecter le périphérique.
Appuyez sur "8" pour déconnecter le périphérique.
Appuyez sur "9" pour effacer le périphérique.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.SET_DATE_ENTER: """
Menu "Date"

Entrez une date à 8 chiffres en commençant par les 4 chiffres de l'année, suivis des 2 chiffres du mois et des 2 chiffres du jour.

Pour supprimer un chiffre, appuyez sur la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur, ou pour recommencer depuis le début, appuyez sur la touche "ENTER" ou "ENTRÉE".

Exemple :

un-neuf-deux-sept

zéro-trois-deux-sept pour le 27 mars 1927.

Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.SET_TIME_ENTER: """
Menu "Heure"

Entrez une heure à 4 chiffres en commençant par les 2 chiffres des heures, suivis des 2 chiffres des minutes.

Pour supprimer un chiffre, appuyez sur la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, appuyez sur la touche "ENTER" ou "ENTRÉE".

Exemple :

un-quatre-zéro-trois pour 2 heures et 3 minutes de l'après-midi.

Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.SET_NAME_ENTER: """
Menu "Nom"

Entrez un nom à 8 chiffres qui servira de nom unique pour votre enregistrement.

Pour supprimer un chiffre, appuyez sur la touche "BACK-SPACE" ou "RETOUR ARRIÈRE".
Lorsque vous avez terminé de saisir la valeur ou pour recommencer depuis le début, appuyez sur la touche "ENTER" ou "ENTRÉE".

Exemple :

zéro-huit-un-cinq

cinq-six-quatre-deux pour zéro-huit 15 56 42.

Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.MAIN_ENTER: """
Menu "Principal"

Appuyez sur "1" pour démarrer un enregistrement stéréo.
Appuyez sur "2" pour démarrer un enregistrement "dry iso" et un enregistrement stéréo.
Appuyez sur "3" pour démarrer un enregistrement "wet iso", un enregistrement "dry iso" et un enregistrement stéréo.
Appuyez sur "4" pour démarrer la lecture.
Appuyez sur "5" pour accéder au menu "Système".
Appuyez sur "6" pour attribuer un nouveau nom à votre prochain enregistrement.
Appuyez sur "9" pour arrêter l'appareil.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.

""",  # noqa: E501

    # OK
    StateEvent.SYSTEM_ENTER: """
Menu "Système"

Appuyez sur "1" pour accéder au menu "Principal".
Appuyez sur "2" pour sélectionner la langue.
Appuyez sur "3" pour accéder au menu "Mémoire".
Appuyez sur "4" pour sélectionner la date.
Appuyez sur "5" pour sélectionner l'heure.
Appuyez sur "9" pour arrêter l'appareil.
Appuyez sur la touche "ASTÉRISQUE" pour répéter ce message.
""",  # noqa: E501

    # OK
    StateEvent.STORAGE_MANAGEMENT_ENTER: """
""",  # noqa: E501

    # OK
    StateEvent.INIT_AUDIO_LEAVE: """
Le système audio est entièrement initialisé.
""",  # noqa: E501

    # OK
    StateEvent.SWALLOW_STATE_ENTER_LEAVE: """""",  # noqa: E501
}
