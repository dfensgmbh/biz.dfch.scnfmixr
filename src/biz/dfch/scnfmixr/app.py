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
import datetime

from biz.dfch.i18n import LanguageCode
from biz.dfch.logging import log
from biz.dfch.version import Version

from .application_context import ApplicationContext
from .args import Arguments
from .core import StateMachine
from .mixer import AudioMixer
from .mixer import AudioMixerConfiguration
from .public.input import InputDevice
from .public.audio import AudioDevice, Format, FileFormat
from .public.storage.storage_device import StorageDevice
from .public.system import SystemTime


class App:  # pylint: disable=R0903
    """The application."""

    _VERSION_REQUIRED_MAJOR = 2
    _VERSION_REQUIRED_MINOR = 0

    # Note: also adjust in pyproject.toml
    _VERSION = "2.1.0"
    _PROG_NAME = "scnfmixr"

    def __init__(self):

        Version().ensure_minimum_version(
            self._VERSION_REQUIRED_MAJOR,
            self._VERSION_REQUIRED_MINOR)

    def invoke(self) -> None:
        """Main entry point for this class."""

        args = Arguments(prog_name=self._PROG_NAME, version=self._VERSION).get()

        app_ctx = ApplicationContext.Factory.get()

        rec_params = app_ctx.recording_parameters
        rec_params.file_format = FileFormat(args.file_format)
        rec_params.sampling_rate = args.sampling_rate
        match args.bit_depth:
            case 16:
                rec_params.format = Format.S16_LE
            case 24:
                rec_params.format = Format.S24_3LE
            case 32:
                rec_params.format = Format.S32_LE
            case _:
                rec_params.format = Format.S24_3LE

        app_ctx.audio_device_map = {
            AudioDevice.LCL: args.LCL,
            AudioDevice.EX1: args.EX1,
            AudioDevice.EX2: args.EX2,
        }
        app_ctx.storage_device_map = {
            StorageDevice.RC1: args.RC1,
            StorageDevice.RC2: args.RC2,
        }
        app_ctx.input_device_map = {
            InputDevice.HI1: args.HI1,
            InputDevice.HI2: args.HI2,
            InputDevice.HI3: args.HI3,
        }
        app_ctx.ui_parameters.language = LanguageCode[args.language]

        now = SystemTime.Factory.get().set().now()
        if args.use_current_date:
            app_ctx.date_time_name_input.set_date(now.date())
        if args.use_current_time:
            app_ctx.date_time_name_input.set_time(now.time())
        if args.use_random_name:
            app_ctx.date_time_name_input.set_pseudo_random_name()

        # Note: Use name from StorageParameters.allowed_usb_ids.
        usb_ids = args.allowed_usb_ids
        if usb_ids:
            for usb_id in usb_ids:
                segments = usb_id.split(':')
                assert 1 <= len(segments) <= 2
                match len(segments):
                    case 1:
                        pair = (segments[0].lower(), None)
                    case 2:
                        pair = (segments[0].lower(), segments[1].lower())

                app_ctx.storage_parameters.allowed_usb_ids.append(pair)

        log.info("Snd map: '%s'.", app_ctx.audio_device_map)
        log.info("Sto map: '%s'.", app_ctx.storage_device_map)
        log.info("Inp map: '%s'.", app_ctx.input_device_map)
        log.info("Rec opt: '%s'.", app_ctx.recording_parameters)
        log.info("App ctx: '%s'.", app_ctx)

        if args.test:
            # pylint: disable=C0415
            from biz.dfch.asyn import ConcurrentQueueT
            from .core.transitions.detecting_hi1 import DetectingHi1
            from .core.fsm import ExecutionContext
            from .core.fsm import StateBase

            fsm = StateMachine()

            state = StateBase(None, None)
            transition = DetectingHi1("0", state)
            ctx = ExecutionContext(
                None, None, events=ConcurrentQueueT(str, True))
            transition.invoke(ctx)

            return

        if args.service:
            log.info("Arg 'startup' detected.")

            cfg = AudioMixerConfiguration.get_default()
            AudioMixer.Factory.get().initialise(cfg)

            fsm = StateMachine()
            fsm.start()

            while fsm.is_started:
                time.sleep(1)
