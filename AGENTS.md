# AGENTS.md

scnfmixr: a Python app running on Raspberry Pi OS (Pi 5) that drives a JACK/ALSA
audio mixer/recorder via a Stream Deck UI and USB storage. See `README.md` /
`INSTALL.md` for hardware, deployment, and full usage docs — this file only
covers things an agent would otherwise get wrong.

## Layout

- `src/biz/dfch/scnfmixr/` — the application (state machine in `core/`,
  hardware-facing interfaces under `public/`, Stream Deck UI in `ui/`,
  `alsa_usb/`, `jack_commands/` wraps `zita-a2j`/`zita-j2a` and the
  `jack_connect`/`jack_disconnect`/`jack_lsp`/`jack_transport` CLIs).
- `src/biz/dfch/{asyn,i18n,logging,diagnostics,version}/` — small shared
  libraries, imported via relative imports from within scnfmixr.
- `src/text/`, `src/col/` — standalone leaf packages, imported as top-level
  `text`/`col` (NOT nested under `biz.dfch`).
- Entry point is `src/biz/__main__.py`, run as `python -m biz ...`.

## Audio architecture

- `jackd` runs with the **dummy** backend (48 kHz, `-p1024`; see
  `service/jackd.service`). Every USB audio device is bridged into JACK by
  `zita-a2j`/`zita-j2a`, which resample it to the JACK clock.
- Every mix bus is a separate `ecasound` process, built in
  `mixer/jack_bus_device.py` (`EcasoundCommandLineBuilder`). Recording is
  done by `jack_capture` (`mixer/audio_recorder.py`).
- Device names (USB roles, see `args.py`): `LCL` local audio device,
  `EX1`/`EX2` external (phone) audio devices, `IN1`/`IN2` insert (effect)
  devices, `RC1`/`RC2` storage, `HI1`/`HI2`/`HI3` numeric keyboard / Stream
  Deck / MIDI controller.
- Bus names (`public/mixer/mixbus_device.py`): `DR0`..`DR2` dry and
  `WT0`..`WT2` wet channel strips (strip 0 = LCL, 1 = EX1, 2 = EX2; an
  insert sits between `DRn` and `WTn`), `MX0` master, `MX1`/`MX2`
  multichannel dry/wet recording buses (`IsoChannelDry`/`IsoChannelWet`),
  `MX3`..`MX6` monitor buses to headsets and phones.
- The routing is in `mixer/device_factory.py` (`create_mixbus_group`) and
  in the FSM transitions `core/transitions/detecting_*.py` /
  `skipping_*.py`, which connect each detected or skipped device. Most
  audio-path bugs are in these files.

## Dev setup

- `pyproject.toml`/`uv.lock` only declare **build/dev tooling** (pytest,
  flake8, mypy, black...), not the app's runtime deps.
- Actual runtime deps (StreamDeck, Pillow, PyYAML, keyboard, pyinstaller...)
  live only in `requirements.txt` — which is **UTF-16-encoded** (frozen via
  Windows `pip freeze`, per README). Convert before installing:
  `iconv -f UTF-16LE -t UTF-8 requirements.txt > /tmp/req.txt && pip install -r /tmp/req.txt`.
- Without `StreamDeck` installed, importing `biz.dfch.scnfmixr` fails, which
  cascades into many unrelated test import errors (see Testing below).

## Testing

```sh
PYTHONPATH=src GITHUB_ACTIONS=true python -m unittest discover -s tests -t . -p "test_*.py"
# single package/module:
PYTHONPATH=src GITHUB_ACTIONS=true python -m unittest discover -v -s tests/<package> -t . -p "test_*.py"
```

- `PYTHONPATH=src` is required — `biz`, `text`, `col` are separate top-level
  packages under `src/`, not one installable package by default.
- **Always set `GITHUB_ACTIONS=true`.** Without it, `tests/test_copyright_year.py`
  is NOT skipped and rewrites the copyright-year header line of every `*.py`
  file touched since Jan 1 of its hardcoded year (it also shells out to the
  Windows-only `git.exe`, so it just errors on Linux anyway). Don't let the
  full suite run without this env var.
- Expect pre-existing failures/errors unrelated to your change when run off
  the target Pi: JACK-server-dependent tests (`tests/scnfmixr/jack_commands`,
  `tests/scnfmixr/system`) fail without a real JACK server, and if
  `StreamDeck`/other hardware libs aren't installed, one failed import
  cascades into dozens of unrelated `AttributeError`/`ImportError` failures.
  Don't chase these unless they're in the area you're changing.
- `tests/integration/test_audioplayer.py` needs real audio playback hardware
  and has no `__init__.py`, so it's not picked up by `unittest discover` —
  run it explicitly only when relevant.

## Style conventions

- Line length is **80 columns** (`.flake8`, `.pylintrc`), matching the actual
  code and the VS Code default formatter (`autopep8 --max-line-length=80`).
  Ignore `[tool.black] line-length = 120` in `pyproject.toml` — it's unused;
  don't reformat files to 120 cols.
- flake8 import order is `google` style (stdlib, third-party, then local).
- Every `.py` file starts with the GPL header block
  (`# Copyright (c) YYYY[ - YYYY] d-fens GmbH, http://d-fens.ch` + boilerplate)
  — copy it from an existing file for any new file.
- Use `# DFTODO` (not `# TODO`) for inline TODO comments — the project's
  consistent convention.
- Suppress a specific SonarCloud finding inline with `# NOSONAR <ruleId>`
  (e.g. `# NOSONAR python:S3626`); SonarCloud is the quality gate (see
  README badges).

## Commits

Commit messages use `<type>(issue-<n>): <summary>` (e.g.
`fix(issue-89): ...`, `docs(issue-96): ...`) when the change belongs to a
GitHub issue. Work is committed on `dev`.

## Versioning

The version string is duplicated and must be bumped in all three places:
`pyproject.toml` (`[project].version`), `src/biz/dfch/scnfmixr/app.py`
(`App._VERSION`), and the badge in `README.md`.

## Build / deploy

Packaged with `pyinstaller --onefile` (exact command in README "Build"
section) and deployed as a systemd user service on a Raspberry Pi 5
(`service/`, `INSTALL.md`). Not something to run speculatively.
