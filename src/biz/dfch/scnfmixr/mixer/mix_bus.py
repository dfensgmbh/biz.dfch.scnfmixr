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

"""Module mix_bus."""

import time

from biz.dfch.asyn import Process
from biz.dfch.logging import log
from biz.dfch.scnfmixr.jack_commands import (
    JackConnection,
    JackPort,
)


class Mixbus():
    """Sets up the mix bus. **WIP**."""

    _process: Process | None

    def __init__(self):

        self._process = None

    def start(self) -> bool:
        """Starts the bus."""

        log.debug("Starting ...")

        if self._process is not None:
            if self._process.is_running:
                log.warning(
                    "Starting FAILED. Process running [%s].",
                    self._process.pid)
            else:
                log.error(
                    "Starting FAILED. Process not None [%s].",
                    self._process.pid)

            return False

        cmd = [
            'ecasound', '-r:80', '-B:rt',

            '-G:jack,MixBus,notransport',

            '-a:LCL-I-DRY', '-f:f32_le,2,48000', '-efh:80',
            '-i:jack,,LCL-I-DRY-I', '-o:jack,,LCL-I-DRY-O',

            '-a:EX1-I-DRY', '-f:f32_le,2,48000', '-efh:80',
            '-i:jack,,EX1-I-DRY-I', '-o:jack,,EX1-I-DRY-O',

            '-a:EX2-I-DRY', '-f:f32_le,2,48000', '-efh:80',
            '-i:jack,,EX2-I-DRY-I', '-o:jack,,EX2-I-DRY-O',

            '-a:LCL-I-WET', '-f:f32_le,2,48000', '-etr:40,0,55',
            '-i:jack,,LCL-I-WET-I', '-o:jack,,LCL-I-WET-O',

            '-a:EX1-I-WET', '-f:f32_le,2,48000', '-etr:40,0,55',
            '-i:jack,,EX1-I-WET-I', '-o:jack,,EX1-I-WET-O',

            '-a:EX2-I-WET', '-f:f32_le,2,48000', '-etr:40,0,55',
            '-i:jack,,EX2-I-WET-I', '-o:jack,,EX2-I-WET-O',

            '-a:MX0', '-f:f32_le,2,48000', '-efh:80',
            '-i:jack,,MX0-I', '-o:jack,,MX0-O',

            '-a:MX1', '-f:f32_le,2,48000', '-efh:80',
            '-i:jack,,MX1-I', '-o:jack,,MX1-O',

            '-a:MX2', '-f:f32_le,2,48000', '-efh:80',
            '-i:jack,,MX2-I', '-o:jack,,MX2-O',

            '-a:MX3', '-f:f32_le,2,48000', '-efh:80',
            '-i:jack,,MX3-I', '-o:jack,,MX3-O',

            '-a:MX4', '-f:f32_le,12,48000', '-efh:80',
            '-i:jack,,MX4-I', '-o:jack,,MX4-O',
        ]

        self._process = Process.start(
            cmd, wait_on_completion=False,
            capture_stdout=True,
            capture_stderr=True)

        log.debug("exit_code '%s'", self._process.exit_code)
        log.debug("stdout '%s'", self._process.stdout)
        log.debug("stderr '%s'", self._process.stderr)

        while True:

            result = JackConnection.get_client_names()
            log.debug("Current JACK clients: [%s]", result)

            if "MixBus" in result:
                break

            time.sleep(0.1)

        # Connect DRY to WET in stereo
        JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:LCL-I-WET-I_1")
        JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:LCL-I-WET-I_2")
        JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:EX1-I-WET-I_1")
        JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:EX1-I-WET-I_2")
        JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:EX2-I-WET-I_1")
        JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:EX2-I-WET-I_2")

        # Setup mix-minus DRY for busses for LCL, EX1, EX2 on MX0, MX1, MX2.
        JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX0-I_1")
        JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX0-I_2")
        JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX0-I_1")
        JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX0-I_2")

        JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX1-I_1")
        JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX1-I_2")
        JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX1-I_1")
        JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX1-I_2")

        JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX2-I_1")
        JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX2-I_2")
        JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX2-I_1")
        JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX2-I_2")

        # Setup stereo master mix.
        JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX3-I_1")
        JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX3-I_2")
        JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX3-I_1")
        JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX3-I_2")
        JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX3-I_1")
        JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX3-I_2")

        # Setup iso mix
        JackPort("MixBus:LCL-I-DRY-O_1").connect_to("MixBus:MX4-I_1")
        JackPort("MixBus:LCL-I-DRY-O_2").connect_to("MixBus:MX4-I_2")
        JackPort("MixBus:EX1-I-DRY-O_1").connect_to("MixBus:MX4-I_3")
        JackPort("MixBus:EX1-I-DRY-O_2").connect_to("MixBus:MX4-I_4")
        JackPort("MixBus:EX2-I-DRY-O_1").connect_to("MixBus:MX4-I_5")
        JackPort("MixBus:EX2-I-DRY-O_2").connect_to("MixBus:MX4-I_6")
        JackPort("MixBus:LCL-I-WET-O_1").connect_to("MixBus:MX4-I_7")
        JackPort("MixBus:LCL-I-WET-O_2").connect_to("MixBus:MX4-I_8")
        JackPort("MixBus:EX1-I-WET-O_1").connect_to("MixBus:MX4-I_9")
        JackPort("MixBus:EX1-I-WET-O_2").connect_to("MixBus:MX4-I_10")
        JackPort("MixBus:EX2-I-WET-O_1").connect_to("MixBus:MX4-I_11")
        JackPort("MixBus:EX2-I-WET-O_2").connect_to("MixBus:MX4-I_12")

        log.info("Starting OK.")

        return True

    def stop(self) -> None:
        """Stops the bus."""

        log.debug("Stopping ...")

        if self._process is None:
            log.warning("Stopping FAILED [None].")
            return

        result = self._process.stop(force=True)
        if not result:
            log.warning("Stopping FAILED [%s].", result)
            return

        self._process = None

        log.info("Stopping OK.")
