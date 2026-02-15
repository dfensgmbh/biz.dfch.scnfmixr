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

    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
Versuche, Eingabegerät DREI zu erkennen.
""",

    # DFTODO: Duplicate intro sound from HI1.
    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """""",

    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
Eingabegerät DREI übersprungen.
""",

    # Menu: Detect Audio LCL.

    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """
guid:902be5b8-cde4-4e89-b2d1-a531b70bed4e
""",

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """
guid:a2ff549b-b12c-4fe7-8f46-0500f3689327
""",

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """
guid:58411c9d-5876-4242-9862-9e10e3ad4846
""",

    # Menu: Detect Audio EX1.

    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
Versuche, externes Gerät EX1 zu erkennen.
""",

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Externes Gerät EX1 erfolgreich erkannt.
""",

    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
Erkennung des externen Geräts EX1 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
Externes Gerät EX1 wurde übersprungen.
""",

    # Menu: Detect Audio EX2.

    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Versuche, externes Gerät EX2 zu erkennen.
""",

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Externes Gerät EX2 erfolgreich erkannt.
""",

    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
Erkennung des externen Geräts EX2 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
Externes Gerät EX2 wurde übersprungen.
""",

    # Menu: Detect storage RC1.

    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Versuche, Speichergerät RC1 zu erkennen.
""",

    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Speichergerät RC1 erfolgreich erkannt.
""",

    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
Erkennung des Speichergerät RC1 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Speichergerät RC1 wurde übersprungen.
""",

    # Menu: Detect storage RC2.

    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Versuche, Speichergerät RC2 zu erkennen.
""",

    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Speichergerät RC2 erfolgreich erkannt.
""",

    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
Erkennung des Speichergerät RC2 fehlgeschlagen.

Überprüfen Sie die Kabel und den Anschluss.
""",

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Speichergerät RC2 wurde übersprungen.
""",

    # Menu: Clean storage RC1.

    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
Versuche, Aufnahmen vom Speichergerät RC1 zu löschen.
""",

    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
Löschen der Aufnahmen vom Speichergerät RC1 erfolgreich.
""",

    # Menu: Clean storage RC2.

    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
Versuche, Aufnahmen vom Speichergerät RC2 zu löschen.
""",

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

    TransitionEvent.INITIALISING_AUDIO_ENTER: """
Audio wird initialisiert
""",

    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
Audio ist initialisiert
""",

    # Menu: Main.

    TransitionEvent.STARTING_RECORDING_ENTER: """
Bereite Aufnahme vor.
""",

    TransitionEvent.STARTING_RECORDING_LEAVE: """
Aufnahme gestartet.
""",

    TransitionEvent.DELETING_LAST_TAKE_ENTER: """
Versuche, die letzte Aufnahme zu löschen.
""",

    TransitionEvent.DELETING_LAST_TAKE_LEAVE: """
Löschen der letzten Aufnahme erfolgreich.
""",

    # Menu: System.

    TransitionEvent.MOUNTING_STORAGE_ENTER: """
Versuche das Speichermedium zu installieren.
""",

    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
Speichermedium erfolgreich installiert.
""",

    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
Versuche das Speichermedium zu trennen.
""",

    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
Speichermedium erfolgreich getrennt.
""",

    TransitionEvent.FORMATTING_STORAGE_ENTER: """
Versuche das Speichermedium zu formatieren.
Alle Daten auf diesem Speichermedium werden gelöscht.
""",

    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
Formatieren des Speichermediums erfolgreich.
""",

    TransitionEvent.STOPPING_SYSTEM_ENTER: """
Das System wird heruntergefahren.
""",

    # Menu: OnRecord.

    TransitionEvent.HELPING_ONRECORD_LEAVE: """
Das Menü „Aufnahme“.
Drücken Sie „1“, um die Aufnahme zu stoppen.
Drücken Sie „2“, um einen Cue-Marker zu setzen.
Drücken Sie „Stern“, um diese Nachricht zu wiederholen.
""",

    TransitionEvent.STOPPING_RECORDING_ENTER: """
Stoppe Aufnahme.
Dies kann einige Sekunden dauern.
""",

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
    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """""",

    # No audio menu necessary.
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
