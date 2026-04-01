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

"""Texts for FR transition event messages."""

# noqa: E501  # NOSONAR  python:S125
# cSpell:disable

from biz.dfch.scnfmixr.core.transition_event import TransitionEvent


TransitionEventFr: dict[TransitionEvent, str] = {

    # Menu: Detect HID HI1.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_ENTER: """
Tentative de détection du périphérique d'entrée UN""",

    # OK
    TransitionEvent.DETECTING_DEVICE_HI1_LEAVE: """
sound-intro.wav""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_HI1_LEAVE: """
Périphérique d'entrée UN ignoré
""",

    # Menu: Detect HID HI2.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI2_ENTER: """
Tentative de détection du périphérique d'entrée DEUX"
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_HI2_LEAVE: """
sound-intro.wav
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_HI2_LEAVE: """
Périphérique d'entrée DEUX ignoré.
""",

    # Menu: Detect HID HI3.
    # OK
    TransitionEvent.DETECTING_DEVICE_HI3_ENTER: """
Tentative de détection du périphérique d'entrée TROIS.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_HI3_LEAVE: """
sound-intro.wav
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_HI3_LEAVE: """
Périphérique d'entrée TROIS ignoré.
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
Tentative de détection du périphérique externe numéro 1.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_LEAVE: """
Périphérique externe numéro 1 détecté avec succès.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX1_FAILED: """
Échec de la détection du périphérique externe numéro 1.
Vérifiez les câbles et le port de connexion.""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_EX1_LEAVE: """
Périphérique externe numéro 1 ignoré.""",

    # Menu: Detect Audio EX2.
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_ENTER: """
Tentative de détection du périphérique externe numéro 2.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_LEAVE: """
Périphérique externe numéro 2 détecté avec succès.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_EX2_FAILED: """
Échec de la détection du périphérique externe numéro 2.
Vérifiez les câbles et le port de connexion.
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_EX2_LEAVE: """
Périphérique externe numéro 2 ignoré.""",

    # Menu: Detect storage RC1.
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_ENTER: """
Tentative de détection du périphérique de mémoire numéro 1
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_LEAVE: """
Périphérique de mémoire numéro 1 détecté avec succès
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_RC1_LEAVE: """
Périphérique de mémoire numéro 1 ignoré.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC1_FAILED: """
Échec de la détection du périphérique de mémoire numéro 1.
Vérifiez les câbles et le port de connexion.""",

    # Menu: Detect storage RC2.
    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_ENTER: """
Tentative de détection du périphérique de mémoire numéro 2.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_LEAVE: """
Périphérique de mémoire numéro 2 détecté avec succès.
""",
    # OK
    TransitionEvent.SKIPPING_DEVICE_RC2_LEAVE: """
Périphérique de mémoire numéro 2 ignoré.
""",
    # OK
    TransitionEvent.DETECTING_DEVICE_RC2_FAILED: """
Échec de la détection du périphérique de mémoire numéro 2.
Vérifiez les câbles et le port de connexion.""",

    # Menu: Clean storage RC1.
    # OK
    TransitionEvent.CLEANING_DEVICE_RC1_ENTER: """
Tentative de suppression des enregistrements du périphérique
de mémoire numéro 1.
""",
    # OK
    TransitionEvent.CLEANING_DEVICE_RC1_LEAVE: """
Suppression des enregistrements du périphérique de mémoire numéro 1 réussi.
""",

    # Menu: Clean storage RC2.
    # OK
    TransitionEvent.CLEANING_DEVICE_RC2_ENTER: """
Tentative de suppression des enregistrements du périphérique
de mémoire numéro 2.
""",
    # OK
    TransitionEvent.CLEANING_DEVICE_RC2_LEAVE: """
Suppression des enregistrements du périphérique de mémoire numéro 2 réussi.
""",

    # Menu: Detect IN1.
    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_ENTER: """
Tentative de détection de l’appareil d’effet 1.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_LEAVE: """
Appareil d’effet 1 détecté avec succès.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN1_FAILED: """
La détection de l’appareil d’effet 1 a échoué.

Vérifiez les câbles et le port de connexion.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_IN1_LEAVE: """
L’appareil d’effet 1 a été ignoré.
""",

    # Menu: Detect IN2.
    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_ENTER: """
Tentative de détection de l’appareil d’effet 1.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_LEAVE: """
Appareil d’effet 2 détecté avec succès.
""",

    # OK
    TransitionEvent.DETECTING_DEVICE_IN2_FAILED: """
La détection de l’appareil d’effet 2 a échoué.

Vérifiez les câbles et le port de connexion.
""",

    # OK
    TransitionEvent.SKIPPING_DEVICE_IN2_LEAVE: """
L’appareil d’effet 2 a été ignoré.
""",


    # Menu: Select language.

    # Menu: Initialise audio.
    # OK
    TransitionEvent.INITIALISING_AUDIO_ENTER: """
L'audio est en cours d'initialisation.
""",
    # OK
    TransitionEvent.INITIALISING_AUDIO_LEAVE: """
L'audio a été initialisé.
""",

    # Menu: Main.
    # OK
    TransitionEvent.STARTING_RECORDING_ENTER: """
Préparation à l’enregistrement.
""",
    # OK
    TransitionEvent.STARTING_RECORDING_LEAVE: """
Enregistrement démarré.
""",

    # Menu: DeletingLastTakeConfirmation.
    # OK
    TransitionEvent.CONFIRMING_DELETING_LAST_TAKE_ENTER: """

""",
    # OK
    TransitionEvent.CONFIRMING_DELETING_LAST_TAKE_LEAVE: """
Suppression du dernier enregistrement réussie.
""",

    # OK
    TransitionEvent.DISMISSING_DELETING_LAST_TAKE_ENTER: """

""",

    # OK
    TransitionEvent.DISMISSING_DELETING_LAST_TAKE_LEAVE: """
Suppression annulée.
""",

    # Menu: System.
    # OK
    TransitionEvent.DISCONNECTING_STORAGE_ENTER: """
Tentative de déconnection du périphérique de mémoire.
""",
    # OK
    TransitionEvent.DISCONNECTING_STORAGE_LEAVE: """
Déconnexion du périphérique de mémoire réussie.
""",
    # OK
    TransitionEvent.FORMATTING_STORAGE_ENTER: """
Tentative de formatage du périphérique de mémoire.
Toutes les données sur ce périphérique seront supprimées.
""",
    # OK
    TransitionEvent.FORMATTING_STORAGE_LEAVE: """
Formatage du périphérique de mémoire réussi.
""",
    # OK
    TransitionEvent.STOPPING_SYSTEM_ENTER: """
Le système est en cours d'arrêt.
""",

    # Menu: OnRecord.
    # OK
    TransitionEvent.HELPING_ONRECORD_LEAVE: """
Le menu « Enregistrement ».
Appuyez sur «1» pour arrêter l’enregistrement.
Appuyez sur «2» pour définir un marqueur de repère.
Appuyez sur «Étoile» pour répéter ce message.""",
    # OK
    TransitionEvent.STOPPING_RECORDING_ENTER: """
Arrêt de l’enregistrement.
Cela peut prendre quelques secondes.
""",
    # OK
    TransitionEvent.STOPPING_RECORDING_LEAVE: """
Enregistrement arrêté.
Vous pouvez maintenant accéder au menu de lecture pour
écouter ou supprimer l’enregistrement.
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
    TransitionEvent.PROCESSING_DIGIT_LEAVE: """
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT0_LEAVE: """zéro
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT1_LEAVE: """un
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT2_LEAVE: """deux
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT3_LEAVE: """trois
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT4_LEAVE: """quatre
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT5_LEAVE: """cinq
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT6_LEAVE: """six
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT7_LEAVE: """sept
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT8_LEAVE: """huit
""",
    # OK
    TransitionEvent.PROCESSING_DIGIT9_LEAVE: """neuf
""",

    TransitionEvent.PROCESSING_DIGIT_OK_LEAVE: """OK
""",

    TransitionEvent.PROCESSING_DIGIT_BACKSPACE_LEAVE: """retour arrière
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
