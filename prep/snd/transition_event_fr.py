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

# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventFr: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.

    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
Détection appareil interface 1 entrer

""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
Détection appareil interface 1 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
Sauter appareil interface 1 quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Detect HID HI2.

    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
Détection appareil interface 2 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
Détection appareil interface 2 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
Sauter appareil interface 2 quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Detect HID HI3.

    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
Détection appareil interface 3 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
Détection appareil interface 3 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
Sauter appareil interface 3 quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Detect Audio LCL.

    TransitionEvent.DETECTING_DEVICE_LCL_ENTER: """
Détection appareil local entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_LCL_LEAVE: """
Détection appareil local quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_LCL_LEAVE: """
Sauter appareil local quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Detect Audio EX1.

    TransitionEvent.DETECTING_DEVICE_EX1_ENTER: """
Détection appareil externe 1 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Détection appareil externe 1 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
""",  # noqa: E501  # NOSONAR

    # Menu: Detect Audio EX2.

    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Détection appareil externe 2 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Détection appareil externe 2 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
""",  # noqa: E501  # NOSONAR

    # Menu: Detect storage RC1.

    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Détection appareil  clé 1 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Détection appareil clé 1 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Sauter appareil clé 1 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
""",  # noqa: E501  # NOSONAR

    # Menu: Detect storage RC2.

    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Détection appareil  clé 2 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Détection appareil clé 2 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Sauter appareil clé 2 quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
""",  # noqa: E501  # NOSONAR

    # Menu: Clean storage RC1.

    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
Effacer appareil clé 1 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
Effacer appareil clé 1 quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Clean storage RC2.

    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
Effacer appareil clé 2 entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
Effacer appareil clé 2 quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Select language.

    #     TransitionEvent.SELECTING_ENGLISH_ENTER: """
    # Selection anglais entrer
    # """,  # noqa: E501  # NOSONAR

    #     TransitionEvent.SELECTING_ENGLISH_LEAVE: """
    # Selection anglais quitter
    # """,  # noqa: E501  # NOSONAR

    #     TransitionEvent.SELECTING_GERMAN_ENTER: """
    # Selection allemand entrer
    # """,  # noqa: E501  # NOSONAR

    #     TransitionEvent.SELECTING_GERMAN_LEAVE: """
    # Selection allemand quitter
    # """,  # noqa: E501  # NOSONAR

    #     TransitionEvent.SELECTING_FRENCH_ENTER: """
    # Selection français entrer
    # """,  # noqa: E501  # NOSONAR

    #     TransitionEvent.SELECTING_FRENCH_LEAVE: """
    # Selection français quitter
    # """,  # noqa: E501  # NOSONAR

    #     TransitionEvent.SELECTING_ITALIAN_ENTER: """
    # Selection italien entrer
    # """,  # noqa: E501  # NOSONAR

    #     TransitionEvent.SELECTING_ITALIAN_LEAVE: """
    # Selection italien quitter
    # """,  # noqa: E501  # NOSONAR

    # Menu: Initialise audio.

    TransitionEvent.INITIALISING_AUDIO_ENTER: """
Initialisation audio entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
Initialisation audio quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Main.

    TransitionEvent.STARTING_RECORDING_ENTER: """
Démarrage enregistrement entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.STARTING_RECORDING_LEAVE: """
Démarrage enregistrement quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DELETING_LAST_TAKE_ENTER: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DELETING_LAST_TAKE_LEAVE: """
""",  # noqa: E501  # NOSONAR

    # Menu: System.

    TransitionEvent.MOUNTING_STORAGE_ENTER: """
Montage mémoire entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.MOUNTING_STORAGE_LEAVE: """
Montage mémoire quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
Déconnexion mémoire entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
Déconnexion mémoire quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.FORMATTING_STORAGE_ENTER: """
Formater mémoire entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
Formater mémoire quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.STOPPING_SYSTEM_ENTER: """
Arrêt système entrer
""",  # noqa: E501  # NOSONAR

    # Menu: OnRecord.

    TransitionEvent.HELPING_ONRECORD_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.STOPPING_RECORDING_ENTER: """
Arrêt enregistrement entrer
""",  # noqa: E501  # NOSONAR

    TransitionEvent.STOPPING_RECORDING_LEAVE: """
Arrêt enregistrement quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SETTING_CUEPOINT_LEAVE: """
Définition marqueur quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.TOGGLING_MUTE_LEAVE: """
Alternation muet quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SHOWING_STATUS_LEAVE: """
Afficher statut quitter
""",  # noqa: E501  # NOSONAR

    # Menu: Date, Time, Name

    TransitionEvent.PROCESSING_DIGIT_LEAVE: """
Traitement chiffre quitter
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """
""",  # noqa: E501  # NOSONAR

    # Menu: Playback

    TransitionEvent.LEAVING_PLAYBACK_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SELECTING_PAUSE_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SELECTING_RESUME_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.JUMPING_CUE_NEXT_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.JUMPING_CUE_PREVIOUS_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SEEKING_NEXT_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.SEEKING_PREVIOUS_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.HELPING_PLAYBACK_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.JUMPING_CLIP_NEXT_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.JUMPING_CLIP_PREVIOUS_LEAVE: """
""",  # noqa: E501  # NOSONAR

    # No specific menu.

    TransitionEvent.RETURNING_TRUE_LEAVE: """
""",  # noqa: E501  # NOSONAR

    TransitionEvent.RETURNING_FALSE_LEAVE: """
""",  # noqa: E501  # NOSONAR

}
