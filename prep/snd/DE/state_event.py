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

"""Module state_event_de."""

from biz.dfch.scnfmixr.core.state_event import StateEvent


class StateEventDe(dict[StateEvent, str]):
    """Texts for DE state event messages."""

    StateEvent.INITIALISE_LCL_ENTER = """
Menü zur "Initialisierung des lokalen Geräts"

Wählen Sie "1" für die Geräteerkennung.
Wählen Sie "2", um die Geräteerkennung zu überspringen.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.INITIALISE_HI1_ENTER = """
Menü zur "Initialisierung des lokalen Eingabegeräts EINS"

Wählen Sie "1" für die Geräteerkennung.
Wählen Sie "2", um die Geräteerkennung zu überspringen.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.SELECT_LANGUAGE_ENTER = """
Menü "Sprachauswahl"

Press "1" for english.
Wählen Sie "2" für deutsch.
Selectionner "3" pour français.
Scegliere "4" por italiano.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.INITIALISE_EX1_ENTER = """
Menü zur "Initialisierung des externen Geräts EINS"

Wählen Sie "1" für die Geräteerkennung.
Wählen Sie "2", um die Geräteerkennung zu überspringen.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.INITIALISE_EX2_ENTER = """
Menü zur "Initialisierung des Externen Geräts ZWEI"

Wählen Sie "1" für die Geräteerkennung.
Wählen Sie "2", um die Geräteerkennung zu überspringen.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.INITIALISE_RC1_ENTER = """
Menü zur "Initialisierung des Speichergeräts EINS"

Wählen Sie "1" für die Geräteerkennung.
Wählen Sie "2", um die Geräteerkennung zu überspringen.
Wählen Sie "6", um das Gerät zu formatieren.
Wählen Sie "7", um das Gerät zu verbinden.
Wählen Sie "8", um das Gerät zu trennen.
Wählen Sie "9", um das Gerät zu säubern.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.INITIALISE_RC2_ENTER = """
Menü zur "Initialisierung des Speichergeräts ZWEI"

Wählen Sie "1" für die Geräteerkennung.
Wählen Sie "2", um die Geräteerkennung zu überspringen.
Wählen Sie "6", um das Gerät zu formatieren.
Wählen Sie "7", um das Gerät zu verbinden.
Wählen Sie "8", um das Gerät zu trennen.
Wählen Sie "9", um das Gerät zu säubern.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    # OK
    StateEvent.SET_DATE_ENTER = """
Menü "Datum"

Geben Sie ein achtstelliges Datum ein, beginnend mit den 4 Ziffern des Jahres, gefolgt von den 2 Ziffern des Monats und den 2 Ziffern des Tages.

Um eine Ziffer zu löschen, drücken Sie die "RÜCK-TASTE" oder "BACK-SPACE" Taste.
Wenn Sie die Eingabe des Wertes abgeschlossen haben, oder von vorne beginnen möchten, drücken Sie die "EINGABE-TASTE" oder "ENTER" Taste.

Beispiel:

Eins-Neun-Zwei-Sieben

Null-Drei-Zwei-Sieben für den Siebenundzwanzigsten März 19 27.

Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.SET_TIME_ENTER = """
Menü "Uhrzeit"

Geben Sie eine vierstellige Uhrzeit ein, beginnend mit den 2 Ziffern im 24 Stundenformat, gefolgt von den 2 Ziffern für die Minuten.


Um eine Ziffer zu löschen, drücken Sie die "RÜCK-TASTE" oder "BACK-SPACE" Taste.
Wenn Sie die Eingabe des Wertes abgeschlossen haben, oder von vorne beginnen möchten, drücken Sie die "EINGABE-TASTE" oder "ENTER" Taste.

Beispiel:

Eins-Vier-Null-Drei für 14 Uhr und 3 Minuten.

Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.SET_NAME_ENTER = """
Menü "Dateiname"

Geben Sie einen achtstelligen Namen ein, der als eindeutiger Name in Ihrer Aufzeichnung verwendet wird.

Um eine Ziffer zu löschen, drücken Sie die "RÜCK-TASTE" oder "BACK-SPACE" Taste.
Wenn Sie die Eingabe des Wertes abgeschlossen haben, oder von vorne beginnen möchten, drücken Sie die "EINGABE-TASTE" oder "ENTER" Taste.

Beispiel:

Null-Acht-Eins-Fünf

Fünf-Sechs-Vier-Zwei für Null-Acht 15 56 42.

Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.MAIN_ENTER = """
"Hauptmenü"

Wählen Sie "1", um eine Stereoaufnahme zu starten.
Wählen Sie "2", um eine "dry iso"-Aufnahme mit einer zusätzlichen Stereoaufnahme zu starten.
Wählen Sie "3", um "wet iso"-Aufnahme und eine "dry iso"-Aufnahme mit einer zusätzlichen Stereoaufnahme zu starten.
Wählen Sie "4", um die Wiedergabe zu starten.
Wählen Sie "5", um zum "System-Menü" zu gelangen.
Wählen Sie "6", um einen neuen Namen für Ihre nächste Aufnahme festzulegen.
Wählen Sie "9", um das Gerät zu stoppen.
Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.SYSTEM_ENTER = """
Menü "System"

Wählen Sie "1", um zum "Hauptmenü" zu gelangen.
Wählen Sie "2", um die Sprache auszuwählen.
Wählen Sie "3", um zum Menü für "Speichergeräte" zu gelangen.
Wählen Sie "4", um ein Datum einzugeben.
Wählen Sie "6", um eine Uhrzeit einzugeben.
Wählen Sie "9", um das Gerät zu stoppen.

Wählen Sie "STERN", um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.STORAGE_MANAGEMENT_ENTER = """
Menü für "Speichergeräte"

Wählen Sie "0", um alle Speichergeräte zu trennen.
Wählen Sie "1", um "Speichergerät EINS" zu erkennen.
Wählen Sie "3", um "Speichergerät ZWEI" zu erkennen.
Wählen Sie "4", um "Speichergerät EINS" zu formatieren.
Wählen Sie "5", um zum "System-Menü" zu gelangen.
Wählen Sie "6", um "Speichergerät ZWEI" zu formatieren.
Wählen Sie "7", um "Speichergerät EINS" zu säubern.
Wählen Sie "9", um "Speichergerät ZWEI" zu säubern.

Wählen Sie "STERN" um diese Nachricht zu wiederholen.
"""  # noqa: E501

    StateEvent.INIT_AUDIO_LEAVE = """
Das Audio-System wurde vollständig initialisiert.
"""  # noqa: E501
