---
classification: null
created: '2026-11-03T07:03:48.420+01:00'
id: feat-095-lingua-monitor-mode
status: planning
type: feat
updated: '2026-11-03T07:09:14.522+01:00'
version: 1.0.0
---

# Feature: LINGUA Monitor Mode on the Main Menu

## Plan

### Overview

GitHub issue #95 (point 5): during an interview the participants hear a different signal from the one that is recorded. This feature adds a "Monitor" mode to the MAIN menu of the Streamdeck. In Monitor mode the LCL headset plays the MX0 bus (the recorded mix-down) instead of its normal monitor bus (MX3). The operator calls the participants on EX1 and EX2, switches to Monitor mode, checks the signal, and then starts the recording. When the operator leaves MAIN (including when the recording starts), the system goes back to Normal mode.

The work runs strictly in sequence: Phase 100 (timing baseline) must be finished, and its result recorded, before Phase 110 starts.

### Requirements

- REQ-001: The MAIN menu has two new keys: "Monitor" on Streamdeck `KEY_07` (event `KEY_2`) and "Normal" on `KEY_08` (event `KEY_3`). `KEY_06` stays unassigned.
- REQ-002: "Monitor" disconnects MX3 from the LCL output ports and connects MX0 to them. "Normal" reverses this. Only LCL is affected; EX1 and EX2 routing is not changed.
- REQ-003: Both keys are idempotent. Pressing "Monitor" in Monitor mode, or "Normal" in Normal mode, changes nothing. After each key the state machine returns to MAIN.
- REQ-004: The mode is Normal after every program start. The current mode is held in `ApplicationContext`.
- REQ-005: Every transition that leaves MAIN restores Normal mode, except HELP and the two new keys. The leaving transitions are: start recording, start playback, System menu, delete last take, set name, stop system.
- REQ-006: A failed restore is logged and never blocks a recording or a playback.
- REQ-007: If the connect of MX0 fails, MX3 stays connected to LCL. If LCL is not present, "Monitor" fails and the state machine re-enters MAIN.
- REQ-008: Monitor mode is not available in the OnRecord menu. The OnRecord menu, its key map and its images are not changed.
- REQ-009: The MAIN-enter prompt (and with it the MAIN help) names the two new keys, in EN, DE, FR and IT.
- REQ-010: A measurement script in the `bin` folder of this feature records the baseline time to switch the routing.

### Acceptance Criteria

- [ ] ACC-001: `bin/measure_monitor_toggle.py` exists and produces CSV and JSON results for the methods and conditions in Phase 100. The results are recorded in this document.
- [ ] ACC-002: In Monitor mode the LCL output ports are connected to MX0 and not to MX3. In Normal mode they are connected to MX3 and not to MX0.
- [ ] ACC-003: Repeated "Monitor" or "Normal" key presses leave the routing unchanged.
- [ ] ACC-004: After each exit from MAIN listed in REQ-005 the routing is Normal. HELP and the two new keys keep the current mode.
- [ ] ACC-005: A recording and a playback start even when the restore fails.
- [ ] ACC-006: After a failed MX0 connect, LCL still receives MX3.
- [ ] ACC-007: The key map for "Main" maps `KEY_07` and `KEY_08` to the new events. No key is mapped twice in "Main". The key maps of the other menus are unchanged.
- [ ] ACC-008: For EN, DE, FR and IT the new key images, transition sounds and updated MAIN-enter text exist. The existing localisation tests pass.
- [ ] ACC-009: The full existing test suite passes.
- [ ] ACC-010: On the LINGUA system the toggle works with the headset worn, and Monitor mode is cleared when a recording starts.
- [ ] ACC-011: Observation only (not pass or fail): the listening test records whether clicks or gaps are audible in either switching order.

### Scope

#### Included

- A Monitor/Normal routing helper for the LCL output, with MX0 as the only monitor source.
- Two new transitions, two new `Main` events, and two new `TransitionEvent` entries.
- Key map entries for "Main".
- Restore of Normal mode on the MAIN exits listed in REQ-005.
- Placeholder resources (plain coloured tiles, silent WAV files) in four languages, and the text entries for the final audio.
- The update of the MAIN-enter prompt text in four languages.
- The timing baseline script and its recorded results.
- Unit tests for routing, FSM transitions, key map and localisation.

#### Explicitly Out Of Scope

- Monitor mode in the OnRecord menu.
- Monitoring on EX1 or EX2 (only LCL).
- Fallback to MX1 or MX2, and any dependency on the `-t` option.
- Final PNG images and voice prompts (supplied by the user).
- A separate USB sound card for monitoring (option b of issue #95).
- Implementation of path removal in `SignalPath` or `SignalPathManager`.
- A pass or fail limit for the toggle time.
- Gain, limiter or clip-meter work, the playback of MP3 files, the MX1 mix-down investigation, and documentation (other points of issue #95).

### Dependencies

#### Depends On

- The Phase 100 baseline result, delivered by the user from the LINGUA system, before Phase 110 starts.
- Issue #89 (commit `d778c1a`): MX0 is the wet-only master mix-down.

#### Blocks

- Nothing.

### Design Notes

**Routing**

- Normal: MX3 feeds the LCL output ports (`core/transitions/detecting_lcl.py`, `bus.connect_to(jack_device.as_sink_set(), DUAL)`).
- Monitor: the LCL sink ports are disconnected from MX3 and connected to MX0 (the first two source ports, as with `DUAL`).
- `SignalPath.remove()` raises `NotImplementedError` and `SignalPathManager.remove` is incomplete. The helper therefore uses `JackPort.connect_to` and `JackPort.disconnect_from` (`jack_commands/jack_port.py`) directly and leaves the path manager records unchanged.
- The order of connect and disconnect (make-before-break or break-before-make) is decided after the Phase 100 baseline and the listening test.
- The buses run all the time. MX0 carries the live signal in MAIN.
- Playback uses its own MPD connection to the LCL output ports (`service/mpd/playback/mpd.conf`). That is why Normal mode must be restored on playback start.

**State and exits**

- The mode flag is stored in `ApplicationContext`, with Normal as the default.
- `Main.on_leave` cannot do the restore, because the FSM calls it for HELP and the monitor keys too and gives it no event (`core/fsm/fsm.py`). The restore is therefore part of each transition that leaves MAIN: `StartingRecordingMixes`, `StartingPlayback`, and the transitions to the System menu, delete last take, set name and stop system.
- `ReturningTrue` is used today for the System menu and delete-last-take transitions. These need a transition type that restores Normal first.
- The restore in `StartingRecordingMixes.invoke` runs before the recording starts.

**Keys and events**

- Free Streamdeck keys in MAIN: 01, 02, 03, 06, 07, 08, 0D. `KEY_07` and `KEY_08` are used. `KEY_06` stays empty, so a slip next to "Record" (`KEY_05`) does not start a recording.
- `Main.Event.SET_MONITOR = InputEventMap.KEY_2` and `Main.Event.SET_NORMAL = InputEventMap.KEY_3`.
- New `TransitionEvent` entries: `SETTING_MONITOR_LEAVE` and `SETTING_NORMAL_LEAVE`.

**Resource files** (base `src/biz/dfch/scnfmixr/res/`, languages EN, DE, FR, IT)

- Key images (512 x 512 PNG, RGBA): `streamdeckeventmap/<LANG>/Main-KEY_07-set_monitor.png` and `streamdeckeventmap/<LANG>/Main-KEY_08-set_normal.png`. The placeholder is a plain coloured tile.
- Sounds (WAV, 16-bit PCM, 48 kHz, stereo): `<LANG>/setting_monitor_leave.wav` and `<LANG>/setting_normal_leave.wav`. The placeholder is a short silent file.
- `<LANG>/main_enter.wav` (mono, 48 kHz) stays unchanged until the user delivers the new recording.
- Text sources: `prep/snd/transition_event_<lang>.py` (two new entries each) and `prep/snd/state_event_<lang>.py` (`StateEvent.MAIN_ENTER` gets lines for the two new keys).
- `Main-default.png` is checked. If it shows the key layout, the user updates it.

**Timing baseline** (`bin/measure_monitor_toggle.py`)

- Python standard library only. It does not change the application.
- It takes the port names as arguments (normal source, monitor source, sink left, sink right) and first prints the current connections from `jack_lsp -c`.
- Method A: one subprocess per operation with verification and polling, like `JackPort`.
- Method B: plain `jack_connect` and `jack_disconnect`, no verification.
- Method C: the `jack` Python client, only if it is already installed. No dependency is added.
- Each method runs in both orders. At least 50 repetitions report min, median, p95 and max in ms. Output is CSV and JSON.
- Conditions: idle, then with a recording running.
- The script restores the original connections on exit, also after an error.
- It has to run on the LINGUA system or an identical Compute Module 5. `jackd` and the JACK tools are not installed on the development machine.
- A separate time from the Streamdeck key press to the end of the transition is taken from the application log.

### Related Decisions

- GitHub issue #95: LINGUA questions and improvements (point 5, option a).
- GitHub issue #89 and commit `d778c1a`: MX0 is fed from the wet strips; monitor-bus feedback removed.

### Task List

#### Phase 100: Timing baseline

- [ ] Task 100.100: Write `bin/measure_monitor_toggle.py` as described in the Design Notes.
- [ ] Task 100.110: Run the script on the LINGUA system, idle and during a recording, and run the listening test in both switching orders.
- [ ] Task 100.120: Record the results in this document (Updates) and decide the connect and disconnect order. Phase 110 starts only after this task.

#### Phase 110: Routing

- [ ] Task 110.100: Add a monitor mode flag to `ApplicationContext`, with Normal as the default.
- [ ] Task 110.110: Add a routing helper that switches the LCL output ports between MX3 and MX0 with `JackPort`. It is idempotent, and it keeps MX3 connected when the connect of MX0 fails.
- [ ] Task 110.120: Add a restore function that sets Normal and only logs a failure.

#### Phase 120: State machine and input

- [ ] Task 120.100: Add `SET_MONITOR` (`KEY_2`) and `SET_NORMAL` (`KEY_3`) to `Main.Event` in `core/states/main.py`.
- [ ] Task 120.110: Add `SETTING_MONITOR_LEAVE` and `SETTING_NORMAL_LEAVE` to `core/transition_event.py`.
- [ ] Task 120.120: Add the transitions `SettingMonitor` and `SettingNormal` in `core/transitions/`, export them, and add them to the MAIN state in `core/state_machine.py`. Both return to MAIN.
- [ ] Task 120.130: Map `KEY_07` and `KEY_08` in the "Main" entry of `public/input/streamdeck_event_map.py`.
- [ ] Task 120.140: Restore Normal in the transitions that leave MAIN (REQ-005). A failed restore must not block the recording or the playback.

#### Phase 130: Resources

- [ ] Task 130.100: Create the placeholder key images for EN, DE, FR and IT (plain coloured tiles, names in the Design Notes).
- [ ] Task 130.110: Create the silent placeholder WAV files for EN, DE, FR and IT (names in the Design Notes).
- [ ] Task 130.120: Add the two new `TransitionEvent` text entries to `prep/snd/transition_event_<lang>.py` for EN, DE, FR and IT.
- [ ] Task 130.130: Add the lines for the two new keys to `StateEvent.MAIN_ENTER` in `prep/snd/state_event_<lang>.py` for EN, DE, FR and IT.
- [ ] Task 130.140: Check `Main-default.png` for the key layout and report to the user if it needs an update.

#### Phase 140: Tests

- [ ] Task 140.100: Write routing tests with fake devices, in the style of `tests/scnfmixr/mixer/test_device_factory.py`: LCL only, idempotence, and a failed connect keeps MX3.
- [ ] Task 140.110: Write state machine tests: both keys return to MAIN, and every exit in REQ-005 restores Normal while HELP and the two keys keep the mode.
- [ ] Task 140.120: Write tests that a recording and a playback start when the restore fails.
- [ ] Task 140.130: Write key map tests: the new keys exist in "Main", no key is mapped twice, and the other menus are unchanged.
- [ ] Task 140.140: Run the localisation tests (`tests/scnfmixr/res`) and the full test suite.

#### Phase 150: On-device check

- [ ] Task 150.100: On the LINGUA system, toggle Monitor and Normal with the headset worn, and start a recording while Monitor is on. Check that Normal is restored.
- [ ] Task 150.110: Record the listening-test observation for clicks and gaps (ACC-011) in this document.

## Progress

### Current Status

**As of 2026-11-03**: Plan created. Implementation has not started. Phase 100 is the first step, and all phases run in sequence.

### Blockers

- Phase 110 and later phases wait for the Phase 100 baseline result from the LINGUA system.
- The final PNG images and voice prompts come from the user.

### Updates

<!-- Newest entry first -- prepend new entries directly below this comment. -->

#### 2026-11-03 06:03:48.420Z - Created

Feature plan created from GitHub issue #95, point 5, option (a). No implementation work has started.

### Decisions Made

<!-- Newest entry first -- prepend new entries directly below this comment. -->

#### 2026-11-03 06:03:48.420Z - Monitor source is MX0 only

MX0 is the recorded mix-down and is always present. There is no fallback to MX1 or MX2 and no dependency on `-t`.

#### 2026-11-03 06:03:48.420Z - Two idempotent keys in MAIN only

Two fixed-state keys (Monitor and Normal) are used instead of one toggle, so a repeated key press does no harm and each key has its own sound. The OnRecord menu is not changed.

#### 2026-11-03 06:03:48.420Z - Normal is restored on every exit from MAIN

Monitor mode ends when the user leaves MAIN, including when the recording or the playback starts. A failed restore never blocks the recording or the playback.

#### 2026-11-03 06:03:48.420Z - Phases run in sequence, clicks are an observation

Phase 110 waits for the Phase 100 baseline. Audible clicks are recorded as an observation and are not a pass or fail criterion.

### Related PRs / Commits

- `d778c1a` fix(issue-89): feed MX0 mix-down from WET strips, drop monitor-bus feedback

### More Information

Source: GitHub issue https://github.com/dfensgmbh/biz.dfch.scnfmixr/issues/95
