# The runtime: Revenant Wings on ndskit's machine

ndskit's runtime (pc-moon's `docs/11-runtime.md`, `12-picture.md`,
`13-sound.md`; pc-nostalgia's and pc-lufiacots's overlays and
interpreter) runs the recompiled programs. This cartridge asked one thing
of it: the order of the two CPUs at a thread switch.

```sh
ROM="rom/Final Fantasy XII - Revenant Wings (Europe) (En,Fr,De,Es,It).nds"
export PATH=/c/msys64/mingw64/bin:$PATH          # SDL3.dll at run time
build/recomp/b/ndsrun "$ROM" --out build/title --save-size 65536 --vblanks 4789
python -m ndskit.melonds build/oracle/states/title.ml1 --compare build/title
build/recomp/b/ndsrun "$ROM" --window --save-size 65536 --out build/play     # to play
```

## The boot

* Both modules found at once (the program is stored plain); the ARM9
  runs four threads, the ARM7 eight.
* **Overlays**, as the per-function residency tells them: 4 at frame 7
  (the logos and the title), 3 at 506 (the opening movie), 4 again at
  3 547 (the title). Not one function interpreted from the boot to the
  first battle: discovery found everything this stretch runs.
* At frame 6 the program writes over the whole LCDC area
  (0x06800000-0x068A3FFF) with no bank mapped there (`write to unmapped
  VRAM`, once per 16 KiB): dropped, as the DS drops it; at the title all
  656 KiB of VRAM are melonDS's, byte for byte.
* **Headless speed**: 80 s of the DS (to the title) in 4.6 s, about 17
  times the DS; the route into the first battle (6 200 frames) in 12 s.

## The VBlank count and the 30 frames a second

The game's frame (`03-executables.md`: 0x020471C8 starts it, 0x0204722C
ends it) runs at 30 a second by its own rule: the start notes the SDK's
VBlank count (0x027FFC3C) at +0x10 of 0x0208121C, and the end, in the
30-a-second mode (+0xC = 1), waits for one VBlank more when the count
has not moved since. **The ARM7 keeps that count**: its VBlank handler
(0x037FB738, one of the SDK 4.0 ARM7's own functions) stores it.

The first runs had the logos short and the opening movie 276 VBlanks
early (overlay 3 at 267 against melonDS's ~500). Read, not guessed:

* melonDS's states at 2, 4, 6, 8, 10 and 12 s (VBlank 100 to 696) and
  the run at the same counts agreed in memory but for 27 bytes, until the
  run left the logos (at 267, melonDS at ~500);
* the logos' loop (overlay 4, 0x02083CFC) shows each logo for 16 steps
  of fading, 91 steps, 16 of fading (a touch, A or START after 30 steps
  cuts it short: no input was given); 246 steps at two VBlanks each
  is melonDS's ~500;
* `--watch` showed the frame's start storing the count *before* the
  ARM7's handler incremented it, at the same line 192 of the same
  VBlank: the ARM9 runs first in each of the machine's quanta, its
  handler woke the thread and the thread started its frame within the
  quantum. Every frame then looked late, waited for one VBlank only, and
  the game ran at **60 frames a second** — the logos twice as fast, and
  so would every mission have been.

**ndskit now makes a thread switch take the rest of the CPU's quantum**
(`machine.cpp`, `switch_to`: ndskit `ad61a11`): the other CPU runs before
the woken thread, as on the DS, where the SDK's reschedule and the
contexts' save and load are a long path. The opening movie now begins
at frame 506; in the first battle the game's counter 0x020811A0 advances
by 60 over 120 VBlanks: **30 a second**, as melonDS's.

## Against melonDS

`python -m ndskit.melonds STATE --compare RUN` at the same SDK VBlank
count, from a new cartridge with no input:

| Moment | Main RAM apart | Other memories |
|---|---|---|
| the logos (100, 220, 336, 456) | 22 bytes at each | ITCM 0; DTCM 12-13 bytes; swram 0 |
| **the opening movie at its frame 378** (melonDS at VBlank 2 387, the run at 2 347) | **29 bytes** | ITCM 0 |
| the title (4 787) | 35 bytes | ITCM 0, DTCM 15, swram 0; VRAM all equal |

What differs is the RTC's date and time (melonDS's clock against the
runtime's fixed date: the save module keeps a copy at 0x0207ECE8),
counters and the touch screen's sampling indices. **The movie is
decoded byte for byte as melonDS decodes it**: at the same frame the
1.1 MB of frame buffers in main RAM are equal. The run's movie is 8
frames (40 VBlanks) ahead of melonDS's throughout: its start, opening
the files and reading the first frames, is a load the runtime's
cartridge answers at once (ndskit's known gap).

## The route into the first battle

```sh
IN="827:START,1007:tap:128:130"; for v in $(seq 1787 120 5387); do IN="$IN,$v:A"; done
IN="$IN,5507:tap:190:112"
build/recomp/b/ndsrun "$ROM" --out build/route --save-size 65536 --vblanks 6200 --input "$IN" --shots 2600,4400,5700
```

The oracle's presses at the same VBlanks (`06-attack-plan.md`): START
skips the opening, a tap on New Game, A for the lines, a tap on the
Flan. Overlays 4, 2 (at 1 077, briefly), 0, 3 (the second movie, 1 115),
0 (the Glabados Ruins, 2 088). The prologue's card, Vaan's lines,
"COMMENCE!", the tutorial; the tap is taken as an order ("Lift the
stylus to order the selected units to move to that location", then
"Units will automatically attack enemies near their destination"). The
pictures, both screens, are right by eye against melonDS's: the 3D map,
the units, the HUD and the map board.
