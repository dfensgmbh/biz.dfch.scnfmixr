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

"""Texts for IT state event messages."""

# cSpell:disable

from biz.dfch.scnfmixr.core.state_event import StateEvent


StateEventIt: dict[StateEvent, str] = {

    # Detection of local audio device.
    StateEvent.INITIALISE_LCL_ENTER: """
Il menu "Inizializzazione Dispositivo Locale"  
  
Premere "1" per il rilevamento del dispositivo.  
Premere "2" per saltare il rilevamento del dispositivo.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_LCL_LEAVE: """""",  # noqa: E501

    # Detection of input device.
    StateEvent.INITIALISE_HI1_ENTER: """
Il menu "Inizializzazione Dispositivo di Ingresso Uno"  
  
Premere "1" per il rilevamento del dispositivo.  
Premere "2" per saltare il rilevamento del dispositivo.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    # OK
    StateEvent.INITIALISE_HI1_LEAVE: """""",  # noqa: E501

    StateEvent.SELECT_LANGUAGE_ENTER: """
Il menu "Selezione Lingua"  
  
Press "1" for english.
Wählen Sie "2" für deutsch.
Selectionner "3" pour français.
Scegliere "4" per italiano.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.INITIALISE_EX1_ENTER: """
Il menu "Inizializzazione Dispositivo Esterno Uno"  
  
Premere "1" per il rilevamento del dispositivo.  
Premere "2" per saltare il rilevamento del dispositivo.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.INITIALISE_EX2_ENTER: """
Il menu "Inizializzazione Dispositivo Esterno Due"  
  
Premere "1" per il rilevamento del dispositivo.  
Premere "2" per saltare il rilevamento del dispositivo.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.INITIALISE_RC1_ENTER: """
Il menu "Inizializzazione Dispositivo di Archiviazione Uno"  
  
Premere "1" per il rilevamento del dispositivo.  
Premere "2" per saltare il rilevamento del dispositivo.  
Premere "6" per formattare il dispositivo.  
Premere "7" per montare il dispositivo.  
Premere "8" per smontare il dispositivo.  
Premere "9" per pulire il dispositivo.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.INITIALISE_RC2_ENTER: """
Il menu "Inizializzazione Dispositivo di Archiviazione Due"  
  
Premere "1" per il rilevamento del dispositivo.  
Premere "2" per saltare il rilevamento del dispositivo.  
Premere "6" per formattare il dispositivo.  
Premere "7" per montare il dispositivo.  
Premere "8" per smontare il dispositivo.  
Premere "9" per pulire il dispositivo.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.SET_DATE_ENTER: """
Il menu "Data"  
  
Inserire una data di 8 cifre iniziando con l'anno di 4 cifre, seguito dal mese di 2 cifre e dal giorno di 2 cifre.  
  
Per cancellare una cifra, premere il tasto "BACK-SPACE".  
Quando si è finito di inserire il valore, o per ricominciare dall'inizio, premere il tasto "INVIO" o "RETURN".  
  
Esempio:  
  
uno-nove-due-sette  
  
zero-tre-due-sette per il 27 marzo del 19 27.  
  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.SET_TIME_ENTER: """
Il menu "Ora"  
  
Inserire un orario di 4 cifre iniziando con le ore di 2 cifre in formato 24 ore, seguite dai minuti di 2 cifre.  
  
Per cancellare una cifra, premere il tasto "BACK-SPACE".  
Quando si è finito di inserire il valore, o per ricominciare dall'inizio, premere il tasto "INVIO" o "RETURN".  
  
Esempio:  
  
uno-quattro-zero-tre per le 2 e 3 minuti del pomeriggio.  
  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.SET_NAME_ENTER: """
Il menu "Nome"  
  
Inserire un nome di 8 cifre utilizzato come nome univoco nella registrazione.  
  
Per cancellare una cifra, premere il tasto "BACK-SPACE".  
Quando si è finito di inserire il valore, o per ricominciare dall'inizio, premere il tasto "INVIO" o "RETURN".  
  
Esempio:  
  
zero-otto-uno-cinque  
  
cinque-sei-quattro-due per zero-otto 15 56 42.  
  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.INIT_AUDIO_LEAVE: """
""",  # noqa: E501

    StateEvent.MAIN_ENTER: """
Il menu "Principale"  
  
Premere "1" per avviare una registrazione stereo.  
Premere "2" per avviare una registrazione dry iso e stereo.  
Premere "3" per avviare una registrazione wet iso, dry iso e stereo.  
Premere "4" per avviare la riproduzione.  
Premere "5" per andare al menu "Sistema".  
Premere "6" per impostare un nuovo nome per la prossima registrazione.  
Premere "7" per eliminare l'ultima registrazione.  
Premere "9" per arrestare il dispositivo.  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.SYSTEM_ENTER: """
Il menu "Sistema"  
  
Premere "1" per andare al menu "Principale".  
Premere "2" per selezionare la lingua.  
Premere "3" per andare al menu "Archiviazione".  
Premere "4" per impostare la data.  
Premere "6" per impostare l'ora.  
Premere "9" per arrestare il dispositivo.  
  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.STORAGE_MANAGEMENT_ENTER: """
Il menu "Archiviazione"  
  
Premere "0" per disconnettere tutti i dispositivi di archiviazione.  
Premere "1" per rilevare il "Dispositivo di Archiviazione Uno".  
Premere "3" per rilevare il "Dispositivo di Archiviazione Due".  
Premere "4" per formattare il "Dispositivo di Archiviazione Uno".  
Premere "5" per andare al menu "Sistema".  
Premere "6" per formattare il "Dispositivo di Archiviazione Due".  
Premere "7" per pulire il "Dispositivo di Archiviazione Uno".  
Premere "9" per pulire il "Dispositivo di Archiviazione Due".  
  
Premere "ASTERISCO" per ripetere questo messaggio.
""",  # noqa: E501

    StateEvent.INIT_AUDIO_LEAVE: """
Sistema audio completamente inizializzato.
""",  # noqa: E501

    # OK
    StateEvent.SWALLOW_STATE_ENTER_LEAVE: """""",  # noqa: E501
}
