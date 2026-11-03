---
classification: null
created: '2026-10-08T19:58:18.553+02:00'
id: feat-088-stop-menu-help-playback
status: planning
type: feat
updated: '2026-10-08T20:51:15.220+02:00'
version: 1.0.0
---

# Feature: Stop Menu Help Playback on Menu Change

## Plan

### Overview

When the user navigates between menus (e.g. Settings to Main, Main to
Settings, Playback to Main), the help message of the menu being left can keep
playing in the background instead of the entered menu's help message starting.
This feature makes the menu audio player (`AudioMenu`, MPD instance
`MediaPlayerType.MENU`) interrupt any lingering menu audio when a *different*
menu is entered, while preserving the current seamless behaviour for
same-menu self-entries (e.g. typing digits in Set Name / Set Date / Set Time).

Tracked as GH issue 88 ("Stop menu help playback when user presses the MENU
button (upper left corner)"), which turned out to describe the symptom via a
partly incorrect mechanism (see Decisions Made).

### Requirements

- REQ-001: When the state machine enters a menu state whose help audio (`UiEventInfo` name) differs from the one started last, the menu audio player shall stop current menu playback and clear the menu playlist before loading the new menu's help audio.
- REQ-002: When a state is entered whose help audio is the same as the one started last (self-transition, e.g. digit entry in Set Name), the menu audio player shall not stop currently playing audio.
- REQ-003: This feature shall not change the behaviour of the content playback player (`AudioPlayback`, MPD instance `MediaPlayerType.PLAYBACK`).
- REQ-004: The "last started menu audio" tracking shall be an in-memory instance field of the `AudioMenu` singleton; it shall not be persisted.

### Acceptance Criteria

- [ ] ACC-001: Unit: on a fresh instance (no persisted state), entering `SYSTEM_ENTER` then `MAIN_ENTER` yields the client call sequence `[stop, clear, load, start, stop, clear, load, start]`.
- [ ] ACC-002: Unit: on a fresh instance (no persisted state), entering `SET_NAME_ENTER` twice yields `[stop, clear, load, start, load, start]` (no stop/clear on the second enter).
- [ ] ACC-003: Unit: on a fresh instance, when the new menu's WAV is missing (`load_menu_queue` returns `[]`), `stop` and `clear` are still executed first and `start` is not called.
- [ ] ACC-004: Unit: (REQ-004) the first enter on a fresh instance — i.e. with no remembered state from a previous process — executes `stop`+`clear` (a no-op on an idle player) then load+start.
- [ ] ACC-005: Regression: `tests/scnfmixr/core/test_state_machine.py` still passes; the new `tests/scnfmixr/playback/test_audio_menu.py` passes; repo lint/typecheck (flake8, mypy) are clean.
- [ ] ACC-006: Manual (Pi): in Settings, after the help has started playing, pressing the return-to-Main key stops it and the Main menu help plays (silence if its WAV is absent).
- [ ] ACC-007: Manual (Pi): MENU in Main plays the System help; MENU in Storage plays the System help; MENU in Playback/PlaybackPaused stops the help (content stop unchanged) and the Main help plays.
- [ ] ACC-008: Manual (Pi): typing digits in Set Name does not restart the menu help (seamless continuation, unchanged behaviour).
- [ ] ACC-009: Manual (Pi): confirm on the deployed MPD 0.23.12 that `mpc clear` without `mpc stop` does not stop the current song (validates the explicit `stop()` in the design).

### Scope

#### Included

- `src/biz/dfch/scnfmixr/playback/audio_menu.py`: new
  `_last_state_enter_name` field and the interrupt guard in
  `_on_state_enter` (design below).

- `src/biz/dfch/scnfmixr/playback/media_player_client.py`: one-line
  docstring fix for `clear()` (it claims "Transport control: stop").

- `tests/scnfmixr/playback/test_audio_menu.py` (+ `__init__.py`): unit tests
  ACC-001..ACC-004.

#### Explicitly Out Of Scope

- Recorded content playback (`AudioPlayback`, `MediaPlayerType.PLAYBACK`).

- The mechanism proposed in GH issue 88 (`InvokingMenuTransition`,
  `on_enter` guards in the state classes,
  `AudioPlayback.PlaybackStopCommand`) — rejected; see Design Notes and
  Decisions Made.

- Pre-existing quirks: STAR/HELP replay not restarting a still-playing help
  message; MENU playlist growth on same-state self-transitions; the stale,
  currently failing `tests/scnfmixr/core/fsm/test_fsm.py`.

- WAV availability on the device (the root-cause trigger); the fix must not
  depend on any specific WAV being present.

### Dependencies

#### Depends On

- None for implementation. Hardware verification (ACC-006..ACC-009) requires
  a Pi with MPD 0.23.12 and mpc 0.34.

### Design Notes

Audio architecture (verified 2026-10-08): two separate MPD instances
(`playback/media_player_type.py`): `PLAYBACK` (content, driven by
`AudioPlayback.*` commands, consumed in `playback/audio_playback.py`) and
`MENU` (help/feedback, driven by `AudioMenu`). Help flow: state/transition
`UiEventInfo` → FSM publishes `UiEventInfo*Message`
(`core/fsm/fsm.py:343,414,438,481`) → `UserInteractionAudio` resolves the
localized WAV path and republishes `UiEventInfoAudioMessage`
(`ui/user_interaction_audio.py:63-78`) → `AudioMenu`'s single FIFO worker
loads the WAV into the MENU playlist and calls `mpc play`
(`playback/audio_menu.py:207-294`).

Root cause of the lingering audio (e.g. Settings → Main via SELECT_MAIN):
leaving the state runs `_on_state_leave` → `mpc clear`, which removes queue
items but does **not** stop the current song (MPD semantics; the docstring of
`MediaPlayerClient.clear()` claiming "Transport control: stop" is
inaccurate). The destination's `_on_state_enter`
(`audio_menu.py:207-223`) does no stop/clear at all and calls `mpc play`
only if the destination WAV is found — if it is missing, the orphaned song of
the left menu continues indefinitely.

Chosen design (Option B, "different menus only"): `AudioMenu` tracks the
`UiEventInfo.name` of the last *state-enter* audio in a new in-memory field
`_last_state_enter_name: StateEvent | None` (initialized `None` in
`__init__`; after a process restart the first enter harmlessly does
stop+clear on an idle player). In `_on_state_enter`, before
`load_menu_queue`+`start`:

```python
if self._last_state_enter_name != message.value.name:
    self._client.stop()
    self._client.clear()
self._last_state_enter_name = message.value.name
```

Why the tracking lives in `AudioMenu`: it is the process-wide singleton that
owns the MENU MPD client and processes all menu-audio messages on one FIFO
worker thread — the only component that both knows what help audio was
started last and can act on it atomically. An FSM-side guard (in the target
state's `on_enter`) is one message too late: the FSM publishes the target's
`UiEventInfoStateEnterMessage` (`fsm.py:343-346`) *before* calling
`on_enter` (`fsm.py:353`), so a stop published there would kill the
destination menu's own announcement (verified experimentally). `ctx.previous`
in the target's `on_enter` is the state *left* (all menu-change transitions
are cross-state), which is why a "previous is the same state" guard never
fires. No lock is needed (single worker thread).

Why both `stop()` and `clear()`: `mpc clear` does not stop the current song;
`mpc play` (no arg) starts from the beginning only when stopped. The
deterministic sequence is stop → clear → add → play. ACC-009
validates this `mpc clear` premise on the deployed MPD 0.23.12; it
underpins REQ-001's explicit `stop()` choice and is premise
verification, not a requirement behaviour.

Behaviour after the change:

| Flow | Before | After |
|---|---|---|
| System → Main (`SELECT_MAIN`) | System help lingers if `MAIN_ENTER.wav` missing | System help stops; Main help plays fresh (or silence) |
| Main → System / Storage → System (`MENU`) | same | same fix |
| Playback/PlaybackPaused → Main (`MENU`) | content stop unchanged; help could linger | help stops; Main help plays |
| Digit typing in SetName/SetDate/SetTime | help continues seamlessly | unchanged |

Unit test construction (no MPD/threads needed): acquire
`AudioMenu.Factory._sync_root` (the private ctor asserts it is locked,
`audio_menu.py:76`), create the instance directly (the worker thread is only
*started* in `acquire()`), inject a call-recording fake for `_client`
(`load_menu_queue`, `start`, `stop`, `clear`), invoke `_on_state_enter`
synchronously, reset `AudioMenu.Factory.__instance` in `tearDown`. Messages
are built exactly as `UserInteractionAudio` does:
`SystemMessage.UiEventInfoAudioMessage(_type=msgt.UiEventInfoStateEnterMessage, path=..., message=UiEventInfo(StateEvent.X, True))`.

### Task List

#### Phase 100: Implementation

- [ ] Task 100.100: Add `_last_state_enter_name` field and the interrupt guard to `AudioMenu._on_state_enter` per Design Notes; correct the `MediaPlayerClient.clear()` docstring (it claims "Transport control: stop").
- [ ] Task 100.110: Add `tests/scnfmixr/playback/__init__.py` and `tests/scnfmixr/playback/test_audio_menu.py` covering ACC-001..ACC-004.
- [ ] Task 100.120: Run the unit suite (new tests plus `tests/scnfmixr/core/test_state_machine.py` regression) and repo lint/typecheck; fix any fallout.

#### Phase 110: Hardware Verification

- [ ] Task 110.100: Execute ACC-006..ACC-009 on the Pi (MPD 0.23.12 + mpc 0.34); record results in a Progress update.

## Progress

### Current Status

**As of 2026-10-08**: Analysis complete and verified against the codebase;
design agreed with the team (Option B, "different menus only");
implementation not started.

### Updates

<!-- Newest entry first -- prepend new entries directly below this comment. -->

#### 2026-10-08 20:51:15.220+02:00 - Refinement pass: corrected acceptance criteria and progress entries

Refinement review of the plan: ACC-001/ACC-002 expected call sequences
corrected for fresh instances (the first enter executes `stop`+`clear`,
per ACC-004 and the design snippet); fresh-instance pre-condition stated
in ACC-001..ACC-003; REQ-004 to ACC-004 linkage made explicit; ACC-009
noted as premise verification underpinning REQ-001's explicit `stop()`;
Task 100.130 dropped (the working plan doc it retired does not exist in
this repository); the `MediaPlayerClient.clear()` docstring fix is scoped
into Task 100.100; Created/Decisions-Made entry timestamps corrected
(they predated the document's own creation).

#### 2026-10-08 19:58:18.553+02:00 - Created

Feature created from the verified analysis of GH issue 88. The earlier
working plan for issue 88 (a scratch document, never committed to this
repository) is superseded by this document.

### Decisions Made

<!-- Newest entry first -- prepend new entries directly below this comment. -->

#### 2026-10-08 19:58:18.553+02:00 - Chose AudioMenu-level enter interrupt ("different menus only")

The menu help player interrupts lingering audio only when the entered
menu's help audio differs from the one started last. Rejected alternatives:
(1) The mechanism proposed in GH issue 88 — `on_enter` guards plus
`AudioPlayback.PlaybackStopCommand`: that command targets the *content*
player, not the help player; the "existing guard" cited at
`core/states/main.py:62` does not exist; and a stop published in the target
state's `on_enter` arrives after the destination's own enter-audio message
(FSM publishes it before `on_enter`, `fsm.py:343` vs `:353`) — verified
experimentally, so it would kill the new menu's announcement. (2) The
"previous state is the same state" guard variant: never fires, because all
menu-change transitions are cross-state (`ctx.previous` is the state left;
verified experimentally). (3) Option A (`InvokingMenuTransition` + new stop
message + rewiring five transitions): viable but about 5× the code and
narrower (does not cover non-MENU lingering gaps). (4) "Always interrupt on
every state-enter": would restart the menu help on every digit press in
SetName/SetDate/SetTime — rejected in favour of the different-menus-only rule.

#### 2026-10-08 19:58:18.553+02:00 - Scope limited to menu help audio

Confirmed with the team: issue 88 is only about the help messages each
menu/state plays on enter (`AudioMenu`, MPD instance
`MediaPlayerType.MENU`). Recorded content playback (`AudioPlayback`,
`MediaPlayerType.PLAYBACK`) is untouched.

### Related PRs / Commits

- [Issue 88](https://github.com/dfensgmbh/biz.dfch.scnfmixr/issues/88):
  "Stop menu help playback when user presses the MENU button (upper left
  corner)".
