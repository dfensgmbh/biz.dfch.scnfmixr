---
classification: null
created: '2026-11-25T17:36:34.124+01:00'
id: 35b111f9-9b3c-473e-b913-25473447bc98
status: draft
type: txt
updated: '2026-11-26T06:19:47.224Z'
version: 1.0.0
---

# VT-4 Audio Quality and Mix-Bus Effect Chain Analysis

Analysis notes for a user report that the sound is "bad" when the Roland
VT-4 (USB `0582:021a`) is connected as insert device IN1. The notes also
record the current ecasound bus chain, the options for a limiter, and a
proposed effect chain and gain-staging plan. Nothing in this document is
implemented. It is input for a later feature or decision.

Status of the findings: the analysis comes from reading the code only
(branch `dev`, after commit `d778c1a`). It was not verified on the target
hardware. Items marked *(verify)* are assumptions about the hardware or the
packaged tools.

Tracked in GitHub issue #96:
https://github.com/dfensgmbh/biz.dfch.scnfmixr/issues/96

## Current Signal Flow

Taken from `mixer/device_factory.py` and `core/transitions/detecting_*.py`:

```
LCL (local mic) -> DR0 -(pass)--------------> WT0 --+
EX1 (phone 1)   -> DR1 -> VT-4 (IN1, USB) -> WT1 ---+--> MX0 (master) -> MX1/MX2 tracks 0/1 -> FLAC 24-bit
EX2 (phone 2)   -> DR2 -(pass)--------------> WT2 --+
DR0..DR2 also go to separate tracks in MX1 (dry), WT0..WT2 to separate tracks in MX2 (wet).

Monitors:  MX3 -> LCL headset = DR2 + WT1
           MX4 -> EX1 phone   = DR0 + DR2
           MX5 -> EX2 phone   = DR0 + WT1
```

- JACK runs with the dummy backend: `jackd -R -ddummy -r48000 -p1024`, so
  one period is 21.3 ms.
- Each USB audio device is bridged with `zita-a2j`/`zita-j2a`, which
  resample every device to the JACK clock.
- Each bus (DR*, WT*, MX*) is a separate `ecasound` process.
- `jack_capture` records 24-bit FLAC.
- IN1 wiring (`detecting_in1.py`): DR1 `MST_LEFT/RIGHT` goes to VT-4
  playback `sinks[2]`/`sinks[3]` (hard-coded indices). VT-4 capture goes to
  WT1.
- Since `d778c1a` (issue #89), MX0 is fed from WT0..WT2 and no longer from
  DR0..DR2. Because of this, a defect in the VT-4 path now also reaches
  the master mix and the reference tracks 0/1 of MX1/MX2. Before, it was
  only in the WT1 track and the monitors.

## Possible Causes of the "Bad" Sound

1. **The VT-4 does not process USB input** *(verify)*. EX1 is a phone
   caller that arrives over USB, so the design requires the VT-4 to
   transform its USB playback input. If the VT-4 only transforms its MIC
   IN and mixes the USB playback into its output, WT1 is the
   untransformed caller with added delay and coloration.
2. **Comb filtering or echo from the round trip.** If the VT-4 loops the
   USB playback back into its USB capture (USB loopback setting,
   *(verify)*), WT1 carries the processed signal plus a delayed dry copy.
   The delay is j2a buffer + VT-4 + a2j buffer + 1024-frame JACK periods,
   which can be about 50 to 100 ms.
3. **Monitor latency.** MX3 and MX5 carry WT1 with the full round-trip
   latency. Listeners can describe the delayed voice as "bad".
4. **Clipping.** No limiter or gain stage exists in any bus (see below).
   The VT-4 output is often hot, depending on the effect, and WT0..WT2 are
   summed into MX0 without a pad. The 24-bit FLAC output and the j2a
   outputs hard-clip above 0 dBFS.
5. **Channel or interface selection.** `AlsaStreamInfoParser` selects the
   capture/playback interface with the highest rate <= 48 kHz, then the
   most channels (<= 6). The hard-coded `sinks[2]`/`sinks[3]` require at
   least 4 playback channels. The selected interface or channel pair may
   not be the one the VT-4 expects *(verify with
   `/proc/asound/card<N>/stream0`)*.
6. **USB or xrun problems.** Dropouts in the zita bridges, a full-speed hub
   shared with other audio devices, or ground-loop and bus-power noise.
   These cause clicks or crackles more than a dull or phasey sound.

## Isolation Procedure

1. **Compare the separate tracks of one take.** Compare `DR1_L/R` (MX1
   file) with `WT1_L/R` (MX2 file). If DR1 is clean and WT1 is bad, the
   VT-4 path is the cause. Check levels and clipping with
   `sox <file> -n remix <ch>,<ch> stats` (peak level near 0 dBFS, flat
   factor > 0).
2. **Examine the live graph and device:** `jack_lsp -c` (connections around
   `Alsa:IN1-*`), `cat /proc/asound/card<N>/stream0` (VT-4 channels and
   rates), and `journalctl --user -u scnfmixr | grep -i "IN1\|Selected"`
   (the selected interface).
3. **Disconnect the feed into the VT-4 at runtime** (`jack_disconnect` of
   DR1 to the IN1 playback ports). If the artifact goes away, cause 2
   applies.
4. **Set the VT-4 effects to off or bypass.** If the sound is still bad,
   the cause is transport (latency, resampling, channel mapping), not the
   effect.
5. **Measure the round-trip latency** with `jack_iodelay` through the
   VT-4.
6. **A/B with IN1 skipped** (`SkippingIn1` connects DR1 directly to WT1).
7. **Look for xruns** in the zita-a2j/j2a output and the journal.

## Current ecasound Bus Chain

`EcasoundCommandLineBuilder.create_bus` (`mixer/jack_bus_device.py`)
builds every bus with the same chain. The only effect is `-efh:80` (80 Hz
high-pass). Consequences:

- **No limiter, compressor or gain stage is active anywhere.** JACK and
  ecasound work in float, so peaks above 0 dBFS survive inside the graph.
  They clip at the integer conversion: the 24-bit FLAC output and the j2a
  outputs.
- The high-pass is applied again on each stage. A signal goes through 3
  to 4 cascaded 80 Hz high-pass filters (DR -> WT -> MX0 -> MX1/MX2). This
  cuts the low end several times and adds phase shift.

## Limiter and Plugin Options in ecasound

Built-in effects:

| Option | Type | Brickwall |
|---|---|---|
| `-eal:limit-%` | Amplitude limiter | Only roughly: no lookahead, close to a clipper |
| `-ec:rate,threshold` | Simple compressor | No |
| `-eca:peak-level,release,fast-rate,rate` | Advanced compressor | No |
| `-enm:...` | Noise gate | n/a |
| `-eadb:gain-dB` | Gain | n/a |

Plugin hosting:

- LADSPA: `-el:<label>,p1,...` or `-eli:<unique-id>,p1,...`, from
  `LADSPA_PATH` (default `/usr/lib/ladspa`).
- LV2: `-elv2:<uri>,p1,...`. This works only if the Debian ecasound build
  includes lilv support *(verify)*.
- Parameters are positional, in the order of the plugin's control input
  ports. Get the order with `analyseplugin` (LADSPA, package `ladspa-sdk`)
  or `lv2info <uri>` (package `lilv-utils`). The command
  `ecasound -c`, then `ladspa-register` / `lv2-register`, lists what
  ecasound can see.

Lookahead limiters from the packages that `INSTALL.md` installs, plus one
candidate package:

- x42-plugins: x42-dpl Digital Peak Limiter, LV2,
  `http://gareus.org/oss/lv2/dpl#stereo` (supports true peak).
- lsp-plugins: LSP Limiter Stereo (LV2; LADSPA availability *(verify)*).
- calf-plugins: Calf Limiter, LV2,
  `http://calf.sourceforge.net/plugins/Limiter`.
- zam-plugins: ZaMaximX2, LV2, `urn:zamaudio:ZaMaximX2`.
- swh-plugins (not installed): `fastLookaheadLimiter`, LADSPA, parameters
  input gain dB, limit dB, release s. Example:
  `-el:fastLookaheadLimiter,0,-0.3,0.05`. This is the safest choice if
  the ecasound build has no LV2 support.

Smoke test on the Pi:

```sh
ecasound -f:f32,2,48000 -i:null -o:null -t:1 \
  -elv2:http://gareus.org/oss/lv2/dpl#stereo,0,-0.3,0.05
lv2info http://gareus.org/oss/lv2/dpl#stereo
ecasound -i:in.wav -o:out.wav -el:fastLookaheadLimiter,0,-0.3,0.05
```

## Proposed Effect Chain

Principle: process each signal once, at the correct stage.

| Stage | Purpose | Effects, in order |
|---|---|---|
| DR0/DR1/DR2 (input strips) | Clean dry separate tracks | Input trim (`-eadb`), then high-pass **once** (80 Hz for LCL; 100 to 120 Hz for phone lines) |
| WT0/WT2 (wet strips, no hardware) | Produced voice | Optional noise gate or expander, then a gentle compressor (about 3:1, threshold about -20 dBFS, attack 10 ms, release 100 to 200 ms), then optional EQ (presence 2 to 4 kHz, de-esser) |
| WT1 (after VT-4) | Match the VT-4 output to the other strips | **Post-insert trim** (the VT-4 output level changes with the effect), then the same compressor as WT0/WT2 |
| MX0 (master) | Safe sum | Headroom pad, then an optional slow glue compressor (2:1, <= 3 dB gain reduction), then a **brickwall limiter** with a -1 dBFS ceiling (true peak if available) |
| MX3/MX4/MX5 (monitors) | Hearing protection, phone codec safety | Pad, then a fast limiter at about -3 dBFS, with low or no lookahead to keep the latency low |
| MX1/MX2 | Carry the tracks for recording | **No processing** |

Notes:

- Keep the DR tracks almost unprocessed. They are the safety copy for a
  later remix.
- Do not normalize loudness live (for example to -16 LUFS for a podcast).
  Record with headroom (24-bit) and do loudness normalization in post.
- Put the effects into the existing ecasound processes. Do not add new bus
  stages, because each additional JACK client in the path can add
  latency.
- Lookahead limiters add a few milliseconds of latency. On the monitor
  buses this adds to the VT-4 round-trip latency.
- MX1/MX2 have 8 channels. A stereo limiter plugin would process only
  part of them. This is one more reason to limit before those buses.

## Gain Reduction for Summing

Recommendation: a modest fixed pad plus the limiter, not the full
worst-case pad.

- Summing does not clip inside the graph (float). It clips only at the
  integer conversion.
- Worst case for 3 equally loud sources: +9.5 dB if correlated, about
  +4.8 dB if uncorrelated (different speakers).
- In a conversation, usually one person talks at a time. A full -9.5 dB
  pad would make the master 7 to 9 dB too quiet most of the time.

Plan:

1. **Gain-stage each strip** to the same target: speech peaks at about
   -12 to -10 dBFS. This is more important than the pad, especially after
   the VT-4.
2. **Pad the sums:** about -4.8 dB on MX0 (3 sources), about -3 dB on the
   2-source monitor buses.
3. **Use the limiter as a safety net, not as a loudness tool.** Gain
   reduction that is often more than 2 to 3 dB means the gain staging
   before it is too hot.

Use the `sox ... stats` check on existing MX0 tracks to confirm the need
for more headroom.

## Possible Implementation (Not Started)

- Add an optional per-bus effects list to
  `EcasoundCommandLineBuilder.create_bus` and `JackBusDevice`.
- Move the high-pass filter to the DR strips only.
- Add pads and limiters to MX0 and MX3 to MX5, and a trim on WT1 after
  IN1.
- Add tests for the generated ecasound command lines.

## Open Questions

- Can the VT-4 transform its USB playback input, or only its MIC IN?
- Does the VT-4 have a USB loopback setting, and what is its current
  value?
- Which playback channels does the VT-4 expose, and are `sinks[2]` and
  `sinks[3]` the correct input channels?
- Is the Debian ecasound package built with LV2 (lilv) support?

## Updates

<!-- Newest entry first -- prepend new entries directly below this comment. -->

### 2026-11-26 06:19:47.224Z - Issue reference added

Added a reference to GitHub issue #96, which tracks the VT-4 report.

### 2026-11-25 16:36:34.124Z - Created

Initial analysis of the VT-4 sound-quality report, the current ecasound bus
chain, limiter and plugin options, and the proposed effect chain and gain
staging. Written from code reading only; not verified on hardware.
