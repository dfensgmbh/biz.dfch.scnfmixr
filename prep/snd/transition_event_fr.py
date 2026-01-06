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

"""Texts for FR transition event messages."""

# noqa: E501  # NOSONAR  python:S125
# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventFr: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.

    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
Détection appareil interface 1 entrer

""",

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
Détection appareil interface 1 quitter
""",

    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
Sauter appareil interface 1 quitter
""",

    # Menu: Detect HID HI2.

    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
Détection appareil interface 2 entrer
""",

    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
Détection appareil interface 2 quitter
""",

    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
Sauter appareil interface 2 quitter
""",

    # Menu: Detect HID HI3.

    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
Détection appareil interface 3 entrer
""",

    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
Détection appareil interface 3 quitter
""",

    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
Sauter appareil interface 3 quitter
""",

    # Menu: Detect Audio LCL.

    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """
Détection appareil local entrer
""",

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """
Détection appareil local quitter
""",

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """
Sauter appareil local quitter
""",

    # Menu: Detect Audio EX1.

    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
Détection appareil externe 1 entrer
""",

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Détection appareil externe 1 quitter
""",

    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
""",

    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
""",

    # Menu: Detect Audio EX2.

    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Détection appareil externe 2 entrer
""",

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Détection appareil externe 2 quitter
""",

    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
""",

    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
""",

    # Menu: Detect storage RC1.

    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Détection appareil  clé 1 entrer
""",

    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Détection appareil clé 1 quitter
""",

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Sauter appareil clé 1 quitter
""",

    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
""",

    # Menu: Detect storage RC2.

    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Détection appareil  clé 2 entrer
""",

    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Détection appareil clé 2 quitter
""",

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Sauter appareil clé 2 quitter
""",

    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
""",

    # Menu: Clean storage RC1.

    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
Effacer appareil clé 1 entrer
""",

    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
Effacer appareil clé 1 quitter
""",

    # Menu: Clean storage RC2.

    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
Effacer appareil clé 2 entrer
""",

    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
Effacer appareil clé 2 quitter
""",

    # Menu: Select language.

    # Menu: Initialise audio.

    TransitionEvent.INITIALISING_AUDIO_ENTER: """
Initialisation audio entrer
""",

    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
Initialisation audio quitter
""",

    # Menu: Main.

    TransitionEvent.STARTING_RECORDING_ENTER: """
Démarrage enregistrement entrer
""",

    TransitionEvent.STARTING_RECORDING_LEAVE: """
Démarrage enregistrement quitter
""",

    TransitionEvent.DELETING_LAST_TAKE_ENTER: """
""",

    TransitionEvent.DELETING_LAST_TAKE_LEAVE: """
""",

    # Menu: System.

    TransitionEvent.MOUNTING_STORAGE_ENTER: """
Montage mémoire entrer
""",

    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
Montage mémoire quitter
""",

    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
Déconnexion mémoire entrer
""",

    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
Déconnexion mémoire quitter
""",

    TransitionEvent.FORMATTING_STORAGE_ENTER: """
Formater mémoire entrer
""",

    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
Formater mémoire quitter
""",

    TransitionEvent.STOPPING_SYSTEM_ENTER: """
Arrêt système entrer
""",

    # Menu: OnRecord.

    TransitionEvent.HELPING_ONRECORD_LEAVE: """
""",

    TransitionEvent.STOPPING_RECORDING_ENTER: """
Arrêt enregistrement entrer
""",

    TransitionEvent.STOPPING_RECORDING_LEAVE: """
Arrêt enregistrement quitter
""",

    TransitionEvent.SETTING_CUEPOINT_LEAVE: """
Définition marqueur quitter
""",

    TransitionEvent.TOGGLING_MUTE_LEAVE: """
Alternation muet quitter
""",

    TransitionEvent.SHOWING_STATUS_LEAVE: """
Afficher statut quitter
""",

    # Menu: Date, Time, Name

    TransitionEvent.PROCESSING_DIGIT_LEAVE: """
Traitement chiffre quitter
""",

    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """
""",

    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """
""",

    # Menu: Playback

    TransitionEvent.LEAVING_PLAYBACK_LEAVE: """
""",

    TransitionEvent.SELECTING_PAUSE_LEAVE: """
""",

    TransitionEvent.SELECTING_RESUME_LEAVE: """
""",

    TransitionEvent.JUMPING_CUE_NEXT_LEAVE: """
""",

    TransitionEvent.JUMPING_CUE_PREVIOUS_LEAVE: """
""",

    TransitionEvent.SEEKING_NEXT_LEAVE: """
""",

    TransitionEvent.SEEKING_PREVIOUS_LEAVE: """
""",

    TransitionEvent.HELPING_PLAYBACK_LEAVE: """
""",

    TransitionEvent.JUMPING_CLIP_NEXT_LEAVE: """
""",

    TransitionEvent.JUMPING_CLIP_PREVIOUS_LEAVE: """
""",

    # No specific menu.

    TransitionEvent.RETURNING_TRUE_LEAVE: """
""",

    TransitionEvent.RETURNING_FALSE_LEAVE: """
""",

}
