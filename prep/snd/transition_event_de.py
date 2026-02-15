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

"""Texts for DE transition event messages."""

# noqa: E501  # NOSONAR  python:S125
# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventDe: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
Versuche, Eingabegerät EINS zu erkennen.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
<<<sound-intro.wav>>>
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
Eingabegerät EINS übersprungen.
""",

    # Menu: Detect HID HI2.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
Versuche, Eingabegerät ZWEI zu erkennen.
""",

    # DFTODO: Duplicate intro sound from HI1.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
<<<sound-intro.wav>>>""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
Eingabegerät ZWEI übersprungen.
""",

    # Menu: Detect HID HI3.
    # OK

    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
Versuche, Eingabegerät DREI zu erkennen.
""",

    # DFTODO: Duplicate intro sound from HI1.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
<<<sound-intro.wav>>>""",

    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
Eingabegerät DREI übersprungen.
""",

    # Menu: Detect Audio LCL.
    # OK. No audio menu necessary.

    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """""",

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """""",

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """""",

    # Menu: Detect Audio EX1.
    # OK

    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
Versuche, externes Gerät EX1 zu erkennen.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Externes Gerät EX1 erfolgreich erkannt.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
Erkennung des externen Geräts EX1 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
Externes Gerät EX1 wurde übersprungen.
""",

    # Menu: Detect Audio EX2.

    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Versuche, externes Gerät EX2 zu erkennen.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Externes Gerät EX2 erfolgreich erkannt.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
Erkennung des externen Geräts EX2 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
Externes Gerät EX2 wurde übersprungen.
""",

    # Menu: Detect storage RC1.

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Versuche, Speichergerät RC1 zu erkennen.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Speichergerät RC1 erfolgreich erkannt.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
Erkennung des Speichergeräts RC1 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Speichergerät RC1 wurde übersprungen.
""",

    # Menu: Detect storage RC2.

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Versuche, Speichergerät RC2 zu erkennen.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Speichergerät RC2 erfolgreich erkannt.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
Erkennung des Speichergerät RC2 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Speichergerät RC2 wurde übersprungen.
""",

    # Menu: Clean storage RC1.

    # OK
    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
Versuche, Aufnahmen vom Speichergerät RC1 zu löschen.
""",

    # OK
    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
Löschen der Aufnahmen vom Speichergerät RC1 erfolgreich.
""",

    # Menu: Clean storage RC2.

    # OK
    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
Versuche, Aufnahmen vom Speichergerät RC2 zu löschen.
""",

    # OK
    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
Löschen der Aufnahmen vom Speichergerät RC2 erfolgreich.
""",


    # Menu: Detect IN1.
    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_ENTER: """
Versuche Effektgerät 1 zu erkennen.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_LEAVE: """
Effektgerät 1 erfolgreich erkannt.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_FAILED: """
Erkennung des Effektgeräts 1 war nicht erfolgreich.

Überprüfen Sie die Kabel und den Anschluss.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_IN1_LEAVE: """
Effektgerät 1 wurde übersprungen.
""",

    # Menu: Detect IN2.
    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_ENTER: """
Versuche Effektgerät 2 zu erkennen.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_LEAVE: """
Effektgerät 2 erfolgreich erkannt.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_FAILED: """
Erkennung des Effektgeräts 2 war nicht erfolgreich.

Überprüfen Sie die Kabel und den Anschluss.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_IN2_LEAVE: """
Effektgerät 2 wurde übersprungen.
""",

    # Menu: Initialise audio.

    # OK
    TransitionEvent.INITIALISING_AUDIO_ENTER: """
Audio wird initialisiert
""",

    # OK
    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
Audio ist initialisiert
""",

    # Menu: Main.

    # OK
    TransitionEvent.STARTING_RECORDING_ENTER: """
Aufnahme wird vorbereitet.
""",

    # OK
    TransitionEvent.STARTING_RECORDING_LEAVE: """
Aufnahme gestartet.
""",

    # OK
    TransitionEvent.DELETING_LAST_TAKE_ENTER: """
Versuche, die letzte Aufnahme zu löschen.
""",

    # OK
    TransitionEvent.DELETING_LAST_TAKE_LEAVE: """
Löschen der letzten Aufnahme erfolgreich.
""",

    # Menu: System.

    # OK
    TransitionEvent.MOUNTING_STORAGE_ENTER: """
Versuche das Speichergerät zu aktivieren.
""",

    # OK
    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
Speichergerät erfolgreich aktiviert.
""",

    # OK
    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
Versuche das Speichergerät zu trennen.
""",

    # OK
    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
Speichergerät erfolgreich getrennt.
""",

    # OK
    TransitionEvent.FORMATTING_STORAGE_ENTER: """
Versuche das Speichergerät zu formatieren.
Alle Daten auf diesem Speichergerät werden gelöscht.
""",

    # OK
    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
Formatieren des Speichergeräts erfolgreich.
""",

    # OK
    TransitionEvent.STOPPING_SYSTEM_ENTER: """
Das System wird heruntergefahren.
""",

    # Menu: OnRecord.

    # OK
    TransitionEvent.HELPING_ONRECORD_LEAVE: """
Das Menü „Aufnahme“.
Drücken Sie „1“, um die Aufnahme zu stoppen.
Drücken Sie „2“, um einen Cue-Marker zu setzen.
Drücken Sie „Stern“, um diese Nachricht zu wiederholen.
""",

    # OK
    TransitionEvent.STOPPING_RECORDING_ENTER: """
Stoppe die Aufnahme.
Dies kann einige Sekunden dauern.
""",

    # OK
    TransitionEvent.STOPPING_RECORDING_LEAVE: """
Aufnahme gestoppt.
Sie können jetzt zum Wiedergabemenü gehen und die Aufnahme anhören oder löschen.
""",

    # No audio menu necessary.
    TransitionEvent.SETTING_CUEPOINT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.TOGGLING_MUTE_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SHOWING_STATUS_LEAVE: """""",

    # Menu: Date, Time, Name

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_LEAVE: """""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """
Null""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """
Eins""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """
Zwei""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """
Drei""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """
Vier""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """
Fünf""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """
Sechs""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """
Sieben""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """
Acht""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """
Neun""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """""",

    # No audio menu necessary.
    # OK
    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """""",

    # Menu: Playback

    # No audio menu necessary.
    TransitionEvent.LEAVING_PLAYBACK_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SELECTING_PAUSE_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SELECTING_RESUME_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CUE_NEXT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CUE_PREVIOUS_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SEEKING_NEXT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.SEEKING_PREVIOUS_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.HELPING_PLAYBACK_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CLIP_NEXT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.JUMPING_CLIP_PREVIOUS_LEAVE: """""",

    # No specific menu.

    # No audio menu necessary.
    TransitionEvent.RETURNING_TRUE_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.RETURNING_FALSE_LEAVE: """""",
}
