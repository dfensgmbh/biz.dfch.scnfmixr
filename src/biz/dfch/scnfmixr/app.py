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

"""Main app module."""

import time

from biz.dfch.i18n import LanguageCode
from biz.dfch.logging import log
from biz.dfch.version import Version

from .app_ctx import ApplicationContext
from .args import Arguments
from .audio import AudioDevices, RecordingParameters
from .core import StateMachine
from .hi_devices import HiDevices
from .rc_devices import RcDevices


class App():
    """The application."""

    _VERSION_REQUIRED_MAJOR = 2
    _VERSION_REQUIRED_MINOR = 0

    # Note: also adjust in pyproject.toml
    _VERSION = "2.1.0"
    _PROG_NAME = "scnfmixr"

    def __init__(self):
        """Creates an instance of this class."""

        Version().ensure_minimum_version(
            self._VERSION_REQUIRED_MAJOR,
            self._VERSION_REQUIRED_MINOR)

    def invoke(self) -> None:
        """Main entry point for this"""

        args = Arguments(prog_name=self._PROG_NAME, version=self._VERSION).get()

        app_ctx = ApplicationContext()

        app_ctx.recording_parameters = RecordingParameters(
            format=args.format,
            sampling_rate=args.sampling_rate,
            bit_depth=args.bit_depth,
            is_dual=args.dual_recording,
        )

        app_ctx.audio_device_map = {
            AudioDevices.LCL: args.LCL,
            AudioDevices.EX1: args.EX1,
            AudioDevices.EX2: args.EX2,
        }
        app_ctx.storage_device_map = {
            RcDevices.RC1: args.RC1,
            RcDevices.RC2: args.RC2,
        }
        app_ctx.input_device_map = {
            HiDevices.HI1: args.HI1,
            HiDevices.HI2: args.HI2,
            HiDevices.HI3: args.HI3,
        }
        app_ctx.language = LanguageCode[args.language]

        log.info("Snd map: '%s'.", app_ctx.audio_device_map)
        log.info("Sto map: '%s'.", app_ctx.storage_device_map)
        log.info("Inp map: '%s'.", app_ctx.input_device_map)
        log.info("Rec opt: '%s'.", app_ctx.recording_parameters)
        log.info("App ctx: '%s'.", app_ctx)

        if args.test:
            from biz.dfch.asyn import ConcurrentQueueT
            from .core.transitions.detecting_hi1 import DetectingHi1
            from .ui import ExecutionContext
            from .ui import StateBase

            fsm = StateMachine()

            state = StateBase(None, None)
            transition = DetectingHi1("0", state)
            ctx = ExecutionContext(
                None, None, events=ConcurrentQueueT(str, True))
            transition.invoke(ctx)

            return

        if args.service:
            log.info("Arg 'startup' detected.")

            fsm = StateMachine()
            fsm.start()

            while fsm.is_started:
                time.sleep(1)

            # time.sleep(2)
            # time.sleep(5)

            # # Select language.
            # for event in ["3"]:
            #     fsm.invoke(event)
            # time.sleep(2)

            # # Enter date
            # for event in ["2", "0", "2", "5", "0", "7", "0", "6"]:
            #     fsm.invoke(event)
            # time.sleep(3)

            # # Enter time
            # for event in ["0", "5", "4", "2"]:
            #     fsm.invoke(event)
            # time.sleep(2)

            # # Enter name
            # for event in ["3", "1", "3", "3", "7", "6", "6", "7"]:
            #     fsm.invoke(event)
            # time.sleep(3)

            # # Do sth else
            # for event in ["1", "3", "3", "2", "1", "9", "1"]:
            #     fsm.invoke(event)
            # time.sleep(3)

            # end = time.time_ns() + 5000 * 10**6
            # while time.time_ns() < end:

            #     log.info("Spinning ...")

            #     time.sleep(500 / 1000)

            # log.info("Spinning ended.")
