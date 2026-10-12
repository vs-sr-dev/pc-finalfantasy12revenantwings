# pc-finalfantasy12revenantwings

A native PC port, in the making, of **Final Fantasy XII: Revenant Wings**
(Nintendo DS; © 2007, 2008 Square Enix, developed with Think & Feel), the
sequel to Final Fantasy XII: Vaan, Penelo, the sky pirate Balthier, the
floating continent of Lemurés, fought out as a real-time strategy game
with the stylus. The cartridge's two programs and its six overlays are
to be recompiled statically to C++ and run on a runtime that replaces
the DS's hardware, the 3D drawn by the PC's GPU at the window's
resolution, the mouse as the stylus.

It is the fourth game of [ndskit](https://github.com/vs-sr-dev/ndskit),
the game-agnostic DS toolkit born with
[pc-moon](https://github.com/vs-sr-dev/pc-moon), proven on
[pc-nostalgia](https://github.com/vs-sr-dev/pc-nostalgia) and hardened on
[pc-lufiacots](https://github.com/vs-sr-dev/pc-lufiacots); ndskit is a
git submodule at `ndskit/`: clone with `--recursive` (or run `git
submodule update --init` after a clone).

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data,
no executables, no assets. You need your own cartridge, dumped. The work
is done on the European release, `Final Fantasy XII - Revenant Wings
(Europe) (En,Fr,De,Es,It).nds` (game code AXFP, version 0, NitroSDK 4.0),
a 128 MiB image with its secure area decrypted, placed in `rom/`.

## Layout

    docs/            cartridge, format and code analysis, and the plan
    tools/           Revenant Wings's tools: dpk.py (the packs), vx.py (the movies' headers), oracle.py (melonDS)
    ndskit/          the game-agnostic DS toolkit (a submodule)
    rom/, build/     your cartridge and everything derived from it (ignored by git)

## Tools

Python 3, no dependencies (the oracle needs PIL for its pictures, and a
copy of melonDS for itself: `ORACLE_DIR`, `tools/oracle.py`). From the
repository's root:

```sh
ROM="rom/Final Fantasy XII - Revenant Wings (Europe) (En,Fr,De,Es,It).nds"

# the cartridge: header, programs, autoloads, six overlays at one address, SDK, banner; its files
python -m ndskit.rom "$ROM" --info
python -m ndskit.rom "$ROM" --list
python -m ndskit.rom "$ROM" --extract build/extract --nested

# the game's packs (42, 6 533 members, some LZ10), the movies (Actimagine VX), the sound
python tools/dpk.py build/extract --list
python tools/dpk.py build/extract --extract build/dpk
python tools/vx.py build/extract/videos
python -m ndskit.sdat build/extract/sound/sound_data.sdat --list
python -m ndskit.sdat build/extract/sound/sound_data.sdat --waves

# the code: every function of the ARM9, of each overlay with it, of the ARM7
python -m ndskit.recomp.discover "$ROM" --cpu 9 --overlay all --report --out "build/disc/f_{id}.tsv"
python -m ndskit.recomp.discover "$ROM" --cpu 7 --report --out build/disc/funcs7.tsv
python -m ndskit.arm build/extract/sys/arm9.bin --base 02000000 --at 02000BB8 --count 170   # main, the scenes

# the oracle: melonDS from a new cartridge, the opening skipped, New Game, into the first battle
python tools/oracle.py --fresh --at "14:START,17:tap:128:130,30:A,32:A,34:A,36:A,38:A,40:A,42:A,44:A,46:A,48:A,50:A,52:A,54:A,56:A,58:A,60:A,62:A,64:A,66:A,68:A,70:A,72:A,74:A,76:A,78:A,80:A,82:A,84:A,86:A,88:A,90:A,92:tap:190:112,100:state"
python -m ndskit.melonds build/oracle/t100.ml1 --overlays "$ROM"
```

## Status

Session 1: feasibility. The cartridge read (a plain ARM9 of NitroSDK
4.0, six plain overlays at one load address, one per kind of scene; an
SDK 4 ARM7 all but Moon's; a 512 Kbit EEPROM save; no anti-piracy), the
formats at a glance (the SDK's NARC, G2D and G3D, the game's packs and
maps, Latin-1 text in five languages, one sound archive), the movies
(ten pairs in Actimagine's VX, 12 frames a second, their decoder in the
ITCM's autoload), the code mapped (the ARM9 with its overlays 3 610
functions, the overlays 4 885, the ARM7 942, no conflict; Ghidra's
functions all found but the C++ exception runtime), the oracle driven
from a new cartridge into the first battle, the frame rate measured in
it (30), and the plan (`docs/06-attack-plan.md`).

Session 2: recompiled and running. Both programs and the six overlays
recompiled (16 737 functions, none left to the interpreter; the
self-test's 103 294 vectors pass, recompiled and interpreted). The game
boots, plays its logos and opening movie, reaches the title and, with
scripted presses and taps, the first battle, with no function
interpreted; the VX movie decodes byte for byte as melonDS's, and the
title's memory and VRAM agree with melonDS's but for the clock. ndskit
learnt that a thread switch gives the other CPU the rest of the
quantum: without it the game ran at 60 frames a second instead of 30.

## Playing it

Early days: from a new cartridge through the opening, the title and the
first battle, headless; the window is to be tried. You need Python 3, and
to build: clang, CMake, Ninja and SDL3 (on Windows, MSYS2's
`mingw-w64-x86_64` packages), and a GPU with OpenGL 4.5. From the
repository's root, with your cartridge in `rom/`:

```sh
ROM="rom/Final Fantasy XII - Revenant Wings (Europe) (En,Fr,De,Es,It).nds"
export PATH=/c/msys64/mingw64/bin:$PATH       # Windows: MSYS2's tools, and SDL3.dll at run time
python -m ndskit.recomp "$ROM" --out build/recomp                    # about 2 minutes
cmake -S build/recomp -B build/recomp/b -G Ninja -DCMAKE_CXX_COMPILER=clang++
ninja -C build/recomp/b                                              # about a minute
build/recomp/b/ndsrun "$ROM" --window --save-size 65536 --out build/play
```

The save (a 512 Kbit EEPROM, hence `--save-size` for a new one) is kept
in `build/play` and written when the window closes. The keys are
melonDS's defaults: X, Z, S, A for A, B, X, Y; Q, W for L, R; Enter and
Backspace for START and SELECT; the arrows for the D-pad; the left mouse
button on the lower screen for the stylus; F12 a picture; Escape quits.

## Documentation

* [00-sessions.md](docs/00-sessions.md) — what each session did
* [01-cartridge-layout.md](docs/01-cartridge-layout.md) — header, programs, the overlays, the file system, the save
* [02-data-formats.md](docs/02-data-formats.md) — the SDK's formats, the packs, the maps, the VX movies, text, sound
* [03-executables.md](docs/03-executables.md) — crt0, main and its scenes, the overlays' loading, the movies' decoder, discovery against Ghidra, the ARM7, the frame
* [04-curiosities.md](docs/04-curiosities.md) — things found on the way
* [05-open-questions.md](docs/05-open-questions.md) — what is not known yet
* [06-attack-plan.md](docs/06-attack-plan.md) — what is new against the first three, a better Revenant Wings on PC, the phases, the oracle's route
* [07-next-session.md](docs/07-next-session.md) — the next session's list
* [09-recompiler.md](docs/09-recompiler.md) — the modules, the self-test
* [10-ndskit.md](docs/10-ndskit.md) — what this port gave ndskit
* [11-runtime.md](docs/11-runtime.md) — the boot, the VBlank count and the 30 frames a second, against melonDS, the route

## Licence

MIT — see [LICENSE](LICENSE). Final Fantasy XII: Revenant Wings is ©
2007, 2008 Square Enix; this project contains none of it.
