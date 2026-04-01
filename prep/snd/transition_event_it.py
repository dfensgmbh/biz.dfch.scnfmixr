# Copyright (c) 2025 - 2026 d-fens GmbH, http://d-fens.ch
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

"""Texts for IT transition event messages."""

# noqa: E501  # NOSONAR  python:S125
# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventIt: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
Tentativo di rilevare il Dispositivo di Ingresso UNO""",
    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
sound-intro.wav""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
Dispositivo di Ingresso UNO saltato
""",

    # Menu: Detect HID HI2.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
Tentativo di rilevare il Dispositivo di Ingresso DUE.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
sound-intro.wav
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
Dispositivo di Ingresso DUE saltato
""",


    # Menu: Detect HID HI3.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
Tentativo di rilevare il Dispositivo di Ingresso TRE.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
sound-intro.wav
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
Dispositivo di Ingresso TRE saltato.
""",

    # Menu: Detect Audio LCL.
    # OK. No audio menu necessary.

    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """
""",

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """
""",

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """
""",

    # Menu: Detect Audio EX1.
    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
Tentativo di rilevare il Dispositivo Esterno 1.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Dispositivo Esterno 1 rilevato con successo.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
Rilevamento del Dispositivo Esterno 1 non riuscito.
Controllare i cavi e la porta di connessione.
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
Dispositivo Esterno 1 saltato.
""",

    # Menu: Detect Audio EX2.
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Tentativo di rilevare il Dispositivo Esterno 2.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Dispositivo Esterno 2 rilevato con successo.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
Rilevamento del Dispositivo Esterno 2 non riuscito.
Controllare i cavi e la porta di connessione.
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
Dispositivo Esterno 2 saltato.
""",

    # Menu: Detect storage RC1.
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Tentativo di rilevare il Dispositivo di Archiviazione 1.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Dispositivo di Archiviazione 1 rilevato con successo.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
Rilevamento del Dispositivo di Archiviazione 1 non riuscito.
Controllare i cavi e la porta di connessione.
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Dispositivo di Archiviazione 1 saltato.
""",

    # Menu: Detect storage RC2.
    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Tentativo di rilevare il Dispositivo di Archiviazione 2.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Dispositivo di Archiviazione 2 rilevato con successo.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
Rilevamento del Dispositivo di Archiviazione 2 non riuscito.
Controllare i cavi e la porta di connessione.
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Dispositivo di Archiviazione 2 saltato.
""",

    # Menu: Clean storage RC1.
    # OK
    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
Tentativo di cancellazione delle registrazioni dal Dispositivo di Archiviazione 1.
""",
    # OK
    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
Cancellazione delle registrazioni dal Dispositivo di Archiviazione 1 riuscita.
""",

    # Menu: Clean storage RC2.
    # OK
    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
Tentativo di cancellazione delle registrazioni dal Dispositivo di Archiviazione 2.
""",
    # OK
    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
Cancellazione delle registrazioni dal Dispositivo di Archiviazione 2 riuscita.
""",

    # Menu: Detect IN1.
    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_ENTER: """
Tentativo di rilevamento del dispositivo effetti 1.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_LEAVE: """
Dispositivo effetti 1 rilevato con successo.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_FAILED: """
Il rilevamento del dispositivo effetti 1 non è riuscito.

Controllare i cavi e la porta di connessione.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_IN1_LEAVE: """
Il dispositivo effetti 1 è stato omesso.
""",

    # Menu: Detect IN2.
    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_ENTER: """
Tentativo di rilevamento del dispositivo effetti 2.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_LEAVE: """
Dispositivo effetti 2 rilevato con successo.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_FAILED: """
Il rilevamento del dispositivo effetti 2 non è riuscito.

Controllare i cavi e la porta di connessione.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_IN2_LEAVE: """
Il dispositivo effetti 2 è stato omesso.
""",


    # Menu: Initialise audio.
    # OK
    TransitionEvent.INITIALISING_AUDIO_ENTER: """
L'audio viene inizializzato.
""",
    # OK
    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
Audio inizializzato
""",

    # Menu: Main.
    # OK
    TransitionEvent.STARTING_RECORDING_ENTER: """
Preparazione alla registrazione.
""",
    # OK
    TransitionEvent.STARTING_RECORDING_LEAVE: """
Registrazione avviata.
""",

    # Menu: DeletingLastTakeConfirmation.
    # OK
    TransitionEvent.CONFIRMING_DELETING_LAST_TAKE_ENTER: """

""",
    # OK
    TransitionEvent.CONFIRMING_DELETING_LAST_TAKE_LEAVE: """
Eliminazione dell’ultima registrazione riuscita.
""",

    # OK
    TransitionEvent.DISMISSING_DELETING_LAST_TAKE_ENTER: """

""",

    # OK
    TransitionEvent.DISMISSING_DELETING_LAST_TAKE_LEAVE: """
Cancellazione interrotta.
""",

    # Menu: System.
    # OK
    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
Tentativo di scollegare il Dispositivo di Archiviazione.
""",
    # OK
    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
Disconnessione del Dispositivo di Archiviazione riuscita.
""",
    # OK
    TransitionEvent.FORMATTING_STORAGE_ENTER: """
Tentativo di formattare il Dispositivo di Archiviazione.
Tutti i dati su questo Dispositivo di Archiviazione verranno eliminati.
""",
    # OK
    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
Formattazione del Dispositivo di Archiviazione riuscita.
""",
    # OK
    TransitionEvent.STOPPING_SYSTEM_ENTER: """
Il sistema viene spento.
""",

    # Menu: OnRecord.
    # OK
    TransitionEvent.HELPING_ONRECORD_LEAVE: """
Il menu “Registrazione”.
Premi “1” per interrompere la registrazione.
Premi “2” per impostare un marcatore di riferimento.
Premi “Stella” per ripetere questo messaggio.
""",
    # OK
    TransitionEvent.STOPPING_RECORDING_ENTER: """
Interruzione della registrazione.
Potrebbero essere necessari alcuni secondi.
""",
    # OK
    TransitionEvent.STOPPING_RECORDING_LEAVE: """
Registrazione interrotta.
Ora puoi andare al menu di riproduzione per ascoltare o eliminare la
registrazione.
""",
    # No audio menu necessary.
    TransitionEvent.SETTING_CUEPOINT_LEAVE: """
""",
    # No audio menu necessary.
    TransitionEvent.TOGGLING_MUTE_LEAVE: """
""",
    # No audio menu necessary.
    TransitionEvent.SHOWING_STATUS_LEAVE: """
""",

    # Menu: Date, Time, Name

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_LEAVE: """""",

    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """0""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """1""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """2""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """3""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """4""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """5""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """6""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """7""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """8""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """9""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """OK""",
    # OK
    # No audio menu necessary.
    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """backspace""",

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
