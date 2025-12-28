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

"""Main app module."""

import sys

from biz.dfch.i18n import LanguageCode
from biz.dfch.logging import log
from biz.dfch.version import Version

from .application_context import ApplicationContext
from .args import Arguments
from .core import StateMachine
from .mixer import AudioMixer
from .mixer import AudioMixerConfiguration
from .mixer import JackSignalManager
from .mixer import DeviceFactory
from .system import SignalHandler, FuncExecutor
from .public.input import InputDevice
from .public.audio import AudioDevice, Format, FileFormat
from .public.storage.storage_device import StorageDevice
from .public.system import SystemTime
from .public.system.messages import SystemMessage


class App:  # pylint: disable=R0903
    """The application."""

    _VERSION_REQUIRED_MAJOR = 3
    _VERSION_REQUIRED_MINOR = 11

    # Note: also adjust in pyproject.toml
    _VERSION = "3.0.0"
    _PROG_NAME = "scnfmixr"

    _signal_handler: SignalHandler

    def __init__(self):

        Version().ensure_minimum_version(
            self._VERSION_REQUIRED_MAJOR,
            self._VERSION_REQUIRED_MINOR)

    def invoke(self) -> None:
        """Main entry point for this class."""

        args = Arguments(prog_name=self._PROG_NAME, version=self._VERSION).get()

        app_ctx = ApplicationContext.Factory.get()

        rec_params = app_ctx.recording_parameters

        # DFTODO - maybe find something more dynamic here?
        rec_params.skip_rc1 = "--skip-storage1" in sys.argv
        rec_params.skip_rc2 = "--skip-storage2" in sys.argv

        rec_params.file_format = FileFormat(args.file_format)
        rec_params.sampling_rate = args.sampling_rate
        match args.bit_depth:
            case 16:
                rec_params.format = Format.S16_LE
            case 24:
                rec_params.format = Format.S24_3LE
            case 32:
                rec_params.format = Format.S32_LE
            case points:
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
                # Format of usb_id: 'abcd:1234'.
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

        if args.service:
            log.info("Arg 'service' detected.")

            cfg = AudioMixerConfiguration.get_default()
            mixer = AudioMixer.Factory.get()
            mixer.initialise(cfg)

            JackSignalManager.Factory.get().acquire()

            mix_devices = DeviceFactory.create_mixbus_group()
            for mx in mix_devices:
                mx.acquire()
                mixer.mixbus.add_device(mx)

            log.warning("Device names [%s]", [
                e.name for e in mixer.mixbus.devices])
            log.debug("Device source points [%s]", [
                      e.name for e in mixer.mixbus.sources])
            log.debug("Device sink points [%s]", [
                      e.name for e in mixer.mixbus.sinks])

            _dr0_sources = next(e.as_source_set().points
                                for e in mixer.mixbus.devices
                                if "DR0" in e.name)
            for point in _dr0_sources:
                log.debug("Point '%s'.", point.name)

            points = [e
                      for e in mixer.mixbus.get_device(
                          "Mixbus:MX0").as_sink_set().points if e.name]
            for point in points:
                log.debug("Point '%s'", point)

            StateMachine().start()

            with FuncExecutor(
                lambda _: True,
                lambda e: isinstance(
                    e,
                    SystemMessage.StateMachine.StateMachineStopped)
            ) as sync:
                sync.wait(2**31)

            log.debug("Signalling application shutdown OK.")
