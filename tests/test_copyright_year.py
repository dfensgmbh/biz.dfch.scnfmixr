# Copyright (c) 2024 - 2026 d-fens GmbH, http://d-fens.ch
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

"""Module test copyright."""

from pathlib import Path
import re
import unittest


class TestCopyright(unittest.TestCase):
    """Class testing template."""

    # Get all py files that changed since 2026-01-01
    # git log --since="2026-01-01" --name-only --pretty=format: | sls \.py | sort -u
    files = """prep/snd/state_event_de.py
prep/snd/state_event_en.py
prep/snd/state_event_fr.py
prep/snd/state_event_it.py
prep/snd/transition_event_de.py
prep/snd/transition_event_en.py
prep/snd/transition_event_fr.py
prep/snd/transition_event_it.py
setup.py
src/_text/__init__.py
src/_text/MultiLineTextParser.py
src/_text/MultiLineTextParserContext.py
src/_text/TextUtils.py
src/biz/__main__.py
src/biz/dfch/scnfmixr/alsa_usb/alsa_stream_info_parser.py
src/biz/dfch/scnfmixr/alsa_usb/alsa_stream_info_visitor.py
src/biz/dfch/scnfmixr/app.py
src/biz/dfch/scnfmixr/application_context.py
src/biz/dfch/scnfmixr/args.py
src/biz/dfch/scnfmixr/audio/audio_device_info.py
src/biz/dfch/scnfmixr/core/fsm/execution_context.py
src/biz/dfch/scnfmixr/core/state_event.py
src/biz/dfch/scnfmixr/core/state_machine.py
src/biz/dfch/scnfmixr/core/states/__init__.py
src/biz/dfch/scnfmixr/core/states/change_language.py
src/biz/dfch/scnfmixr/core/states/final_state.py
src/biz/dfch/scnfmixr/core/states/initialise_audio.py
src/biz/dfch/scnfmixr/core/states/initialise_ex1.py
src/biz/dfch/scnfmixr/core/states/initialise_ex2.py
src/biz/dfch/scnfmixr/core/states/initialise_hi1.py
src/biz/dfch/scnfmixr/core/states/initialise_hi2.py
src/biz/dfch/scnfmixr/core/states/initialise_hi3.py
src/biz/dfch/scnfmixr/core/states/initialise_in1.py
src/biz/dfch/scnfmixr/core/states/initialise_in2.py
src/biz/dfch/scnfmixr/core/states/initialise_rc1.py
src/biz/dfch/scnfmixr/core/states/initialise_rc2.py
src/biz/dfch/scnfmixr/core/states/main.py
src/biz/dfch/scnfmixr/core/states/onrecord.py
src/biz/dfch/scnfmixr/core/states/playback.py
src/biz/dfch/scnfmixr/core/states/system.py
src/biz/dfch/scnfmixr/core/transition_event.py
src/biz/dfch/scnfmixr/core/transitions/__init__.py
src/biz/dfch/scnfmixr/core/transitions/cleaning_rc1.py
src/biz/dfch/scnfmixr/core/transitions/cleaning_rc2.py
src/biz/dfch/scnfmixr/core/transitions/clear_date_time_name.py
src/biz/dfch/scnfmixr/core/transitions/deleting_last_take.py
src/biz/dfch/scnfmixr/core/transitions/detecting_ex1.py
src/biz/dfch/scnfmixr/core/transitions/detecting_ex2.py
src/biz/dfch/scnfmixr/core/transitions/detecting_hi1.py
src/biz/dfch/scnfmixr/core/transitions/detecting_hi2.py
src/biz/dfch/scnfmixr/core/transitions/detecting_in1.py
src/biz/dfch/scnfmixr/core/transitions/detecting_in2.py
src/biz/dfch/scnfmixr/core/transitions/disconnecting_storage.py
src/biz/dfch/scnfmixr/core/transitions/formatting_storage.py
src/biz/dfch/scnfmixr/core/transitions/mounting_rc1.py
src/biz/dfch/scnfmixr/core/transitions/mounting_rc2.py
src/biz/dfch/scnfmixr/core/transitions/selecting_language_base.py
src/biz/dfch/scnfmixr/core/transitions/showing_status.py
src/biz/dfch/scnfmixr/core/transitions/skipping_ex1.py
src/biz/dfch/scnfmixr/core/transitions/skipping_ex2.py
src/biz/dfch/scnfmixr/core/transitions/skipping_in1.py
src/biz/dfch/scnfmixr/core/transitions/skipping_in2.py
src/biz/dfch/scnfmixr/core/transitions/skipping_lcl.py
src/biz/dfch/scnfmixr/core/transitions/starting_recording.py
src/biz/dfch/scnfmixr/core/transitions/starting_recording_mixes.py
src/biz/dfch/scnfmixr/core/transitions/toggling_mute.py
src/biz/dfch/scnfmixr/core/transitions/unmounting_rc1.py
src/biz/dfch/scnfmixr/core/transitions/unmounting_rc2.py
src/biz/dfch/scnfmixr/date_time_name_input.py
src/biz/dfch/scnfmixr/devices/storage/detecting_rc_worker.py
src/biz/dfch/scnfmixr/devices/storage/device_operations.py
src/biz/dfch/scnfmixr/input/streamdeck_image_converter.py
src/biz/dfch/scnfmixr/input/streamdeck_image_library.py
src/biz/dfch/scnfmixr/input/streamdeck_input_resolver.py
src/biz/dfch/scnfmixr/jack_commands/alsa_jack_base.py
src/biz/dfch/scnfmixr/jack_commands/zita_bridge_base.py
src/biz/dfch/scnfmixr/mixer/audio_recorder.py
src/biz/dfch/scnfmixr/mixer/device_factory.py
src/biz/dfch/scnfmixr/mixer/jack_alsa_device.py
src/biz/dfch/scnfmixr/mixer/jack_signal_manager.py
src/biz/dfch/scnfmixr/mixer/jack_signal_point_manager.py
src/biz/dfch/scnfmixr/mixer/signal_point.py
src/biz/dfch/scnfmixr/playback/audio_menu.py
src/biz/dfch/scnfmixr/playback/audio_playback.py
src/biz/dfch/scnfmixr/playback/media_player_client.py
src/biz/dfch/scnfmixr/playback/media_player_type.py
src/biz/dfch/scnfmixr/public/__init__.py
src/biz/dfch/scnfmixr/public/audio/alsa_interface_info.py
src/biz/dfch/scnfmixr/public/audio/audio_device.py
src/biz/dfch/scnfmixr/public/audio/bit_depth.py
src/biz/dfch/scnfmixr/public/audio/format.py
src/biz/dfch/scnfmixr/public/constant.py
src/biz/dfch/scnfmixr/public/input/__init__.py
src/biz/dfch/scnfmixr/public/input/event_map_base.py
src/biz/dfch/scnfmixr/public/input/keyboard_event_map.py
src/biz/dfch/scnfmixr/public/input/menu_profile.py
src/biz/dfch/scnfmixr/public/input/streamdeck_event_map.py
src/biz/dfch/scnfmixr/public/messages/audio_recorder.py
src/biz/dfch/scnfmixr/public/mixer/connection_info.py
src/biz/dfch/scnfmixr/public/mixer/connection_policy.py
src/biz/dfch/scnfmixr/public/storage/file_name.py
src/biz/dfch/scnfmixr/public/system/__init__.py
src/biz/dfch/scnfmixr/public/system/usb_port.py
src/biz/dfch/scnfmixr/public/ui/ui_parameters.py
src/biz/dfch/scnfmixr/system/action_descriptor.py
src/biz/dfch/scnfmixr/system/message_queue.py
src/biz/dfch/scnfmixr/system/signal_handler.py
src/biz/dfch/scnfmixr/system/timer.py
src/biz/dfch/scnfmixr/ui/event_handler_base.py
src/biz/dfch/scnfmixr/ui/keyboard_handler.py
src/biz/dfch/scnfmixr/ui/streamdeck_handler.py
src/text/__init__.py
src/text/MultiLineTextParser.py
src/text/MultiLineTextParserContext.py
src/text/TextUtils.py
tests/_text/__init__.py
tests/_text/test_MultiLineTextParser.py
tests/_text/test_TextUtils.py
tests/alsa_usb/test_AlsaStreamInfoVisitor.py
tests/scnfmixr/core/fsm/test_transition_base.py
tests/scnfmixr/input/test_streamdeck_image_converter.py
tests/scnfmixr/input/test_streamdeck_image_library.py
tests/scnfmixr/input/test_streamdeck_input_resolver.py
tests/scnfmixr/mixer/test_signal_point.py
tests/scnfmixr/public/audio/__init__.py
tests/scnfmixr/public/audio/test_format.py
tests/scnfmixr/public/input/__init__.py
tests/scnfmixr/public/input/test_menu_profile.py
tests/scnfmixr/res/test_res_snd_files.py
tests/scnfmixr/res/test_state_de.py
tests/scnfmixr/res/test_transition_de.py
tests/scnfmixr/res/test_transition_en.py
tests/scnfmixr/res/test_transition_fr.py
tests/scnfmixr/res/test_transition_it.py
tests/scnfmixr/test_date_time_name_input.py
tests/test___main__.py
tests/text/__init__.py
tests/text/test_MultiLineTextParser.py
tests/text/test_TextUtils.py"""

    CURRENT_YEAR = "2026"  # or str(datetime.now().year)
    _pattern = re.compile(
        r"^(# Copyright \(c\) )(.+?)( d-fens GmbH, http://d-fens\.ch)$"
    )

    def _update_line(self, value: str) -> str | None:
        m = self._pattern.match(value)
        if not m:
            return None
        prefix, years_part, suffix = m.groups()
        years = re.findall(r"\d{4}", years_part)
        if not years:
            return None

        min_year = min(years)
        max_year = max(years)
        if self.CURRENT_YEAR == max_year:
            return None
        updated_years = f"{min_year} - {self.CURRENT_YEAR}"

        return f"{prefix}{updated_years}{suffix}"

    def _process_file(self, path: Path) -> None:
        assert path.exists(), path
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines:
            return None
        updated = self._update_line(lines[0])
        if not updated:
            return None
        lines[0] = updated
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_something(self):
        """Testing something succeeds."""

        project_dir = Path(__file__).resolve().parent.parent
        for file in self.files.split(sep="\n"):
            full_name = project_dir / file
            if not Path.exists(full_name):
                continue
            print(f"{full_name}")
            self._process_file(full_name)

if __name__ == "__main__":
    unittest.main()
