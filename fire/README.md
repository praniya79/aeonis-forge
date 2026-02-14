# FIRE listener (Seventh River)

This is the tiny local “neuron spike” intake.

- Listens on `127.0.0.1:9999`
- Expects simple text lines (e.g. `fire`) followed by `\n`
- Appends spikes to the current daily log under `## Fire spikes` **if** `memory/YYYY-MM-DD.md` exists.

## Test

From another terminal:

```bash
# Linux/mac
printf "fire\n" | nc 127.0.0.1 9999
```

PowerShell:

```powershell
"fire" | ncat 127.0.0.1 9999
```

## NixOS / udev trigger (example)

```udev
ACTION=="change", SUBSYSTEM=="input", RUN+="/run/current-system/sw/bin/bash -c 'echo fire | nc localhost 9999'"
```

(Adjust paths as needed.)
