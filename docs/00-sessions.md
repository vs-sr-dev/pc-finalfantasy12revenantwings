# Sessions

## Session 1 (2026-10-12) — the cartridge, the code, the oracle, the plan

* **The repository**: ndskit as a submodule at `ndskit/` (`../ndskit`,
  at `5ee24af`), pc-lufiacots's MIT licence and `.gitignore` (with
  `*.vx`); the cartridge in `rom/`.
* **The cartridge** (`01-cartridge-layout.md`): the European release,
  AXFP, Square Enix (GD), **NitroSDK 4.0**, 128 MiB; on screen the logos
  of Square Enix, Think & Feel, the Ivalice Alliance and Actimagine's
  video codec, the opening's staff, and "© 2007, 2008 SQUARE ENIX
  CO.,LTD." on the title. **The ARM9 plain**, its autoloads to the ITCM
  and the DTCM; **six plain overlays at one address** (0x020838C0): the
  missions (0), the license board (1), the airship (2), the movies and
  the ending (3), the title (4), the preparations (5); **an SDK 4 ARM7**,
  871 of its 942 functions as Moon's; 2 140 files in 202 directories;
  the save a **512 Kbit EEPROM** (0x1001 in the save module; melonDS's
  `.sav` is 64 KiB).
* **The formats** (`02-data-formats.md`): the SDK's NARC (G2D, G3D)
  everywhere; the game's **packs** (`.dpk`, 42 files, 6 533 members, some
  LZ10: `tools/dpk.py`), its **maps** (`.bmd2`, an NSBMD with its
  animations and game sections), its tables; text in Latin-1 per
  language (E, F, G, I, S); **ten movies in Actimagine's VX**, both
  screens, 256 × 192 at 12 fps, their sound in the upper screen's file
  (`tools/vx.py`); one SDAT: 53 sequences, 78 effect archives, 2 237
  waves, PSG and noise, no streams.
* **The code** (`03-executables.md`): crt0, `main` at 0x02000BB8 (a loop
  over scenes, each loading its overlay through `FS_LoadOverlay`
  0x0200D504 and calling its entry), `FS_StartOverlay` 0x0200D410 (SDK
  4.0's), the threads' context switch, the save module; **the VX decoder
  in the ITCM's autoload** (overlay 3 is the player; in melonDS the ITCM
  is the autoload's byte for byte during the opening movie: no run-time
  copy, no `--copy`). Discovery: the ARM9 with its overlays **3 610
  functions, the overlays 4 885, the ARM7 942, 0 conflicts anywhere**;
  Ghidra's 2 607 functions all discovery's entries but 11, the C++
  exception runtime. **No anti-piracy**: only the SDK's CARD library
  touches the card's registers.
* **The oracle**: `tools/oracle.py` (pc-lufiacots's). From a new
  cartridge: START skips the opening (the title at 16 s), "New Game"
  plays a second movie, then the prologue in **the Glabados Ruins**
  ("COMMENCE!" at about 67 s), a battle with a tutorial that waits for
  the stylus's orders (a tap on the enemy taken). States kept: the
  opening, the title, the tutorial (two, two seconds apart), the battle.
  Overlays resident: 3 in the opening movie, 4 at the title, 0 in the
  battle.
* **The frame rate: 30 a second in a mission** (a counter of the game's
  at 0x020811A0 at half the VBlank count); not measured at the title or in
  the movies (no counter there).
* **The plan** (`06-attack-plan.md`): the three ports' road; new here
  the VX movies (their sound and pacing), the stylus as the game's whole
  input (the mouse, drags, the lower screen as the main view), hotkeys
  for the unit tabs and the summons, the 3D at the window's resolution.
* **ndskit**: unchanged (`10-ndskit.md`); everything ran on `5ee24af`.
* **A head start on session 2**: `python -m ndskit.recomp --optest`
  generates 10 modules (16 737 functions, none left to the interpreter),
  which build with no warning; ndskit's instruction test passes, 57 781
  vectors, recompiled and interpreted.

## Session 2 (2026-10-12) — recompiled, booted, the movies exact, into the first battle

* **The recompiler** (`09-recompiler.md`): 10 modules, 16 737 functions,
  none left to the interpreter, built with no warning. The self-test
  with this game's functions (the program, the ARM7, overlays 0 and 2)
  and ndskit's instruction test: **103 294 vectors, no failure**,
  recompiled and interpreted, at the first run.
* **The runtime** (`11-runtime.md`): the boot, the logos, the opening
  movie, the title, headless at about 17 times the DS; **not one
  function interpreted** from the boot into the first battle.
* **The logos were half as long as melonDS's**, and the game would have
  run at 60 frames a second: its frame start read the SDK's VBlank count
  before the ARM7's handler stored it (the ARM9 ran first in the
  machine's quantum). **ndskit `ad61a11`: a thread switch takes the
  rest of the CPU's quantum**; then the logos, the movie and the battle
  (30 a second) keep melonDS's time. Checked on pc-moon, pc-nostalgia and
  pc-lufiacots (their self-tests, runs against melonDS and routes as
  before or closer), fast-forwarded into `D:\Homebrew6\ndskit`, the three
  ports' submodules bumped and committed (`10-ndskit.md`).
* **Against melonDS**: 22 bytes of main RAM apart during the logos, 35
  at the title (the RTC's date, counters), VRAM all equal at the title;
  **the VX movie decoded byte for byte as melonDS's** (29 bytes apart at
  the same movie frame, 1.1 MB of frame buffers equal); the run's movie
  8 frames ahead of melonDS's (its start is a load the runtime's
  cartridge answers at once).
* **The route into the Glabados Ruins** with `--input` (START, a tap on
  New Game, A, a tap on the Flan): the second movie, the prologue,
  "COMMENCE!", the tutorial taking the tap as an order; the pictures
  right by eye.
* **The user's eyes and ears**: in the window from a new cartridge,
  3 min 32 s of play (12 702 frames: the logos and the opening skipped,
  New Game, the second movie, then three minutes of the Glabados Ruins'
  battle): "everything works perfectly" — the battles, the movies, the
  sound, the stylus by the mouse, units selected singly and several at
  once by a drag. No function interpreted; the audio queue never ran dry
  nor was cut (playback ratio 1.0002).
* **The gameplay loop, by the user**: 13 min 23 s from a new cartridge
  (48 027 frames) through the prologue to **mission 1-1**, "everything
  perfect". Overlays 0, 2 and 3 in turn (the missions, the moves
  between them, two more movies: at 28 701 and 34 861), nothing
  interpreted, the audio queue never dry. **Saved twice**, the second
  save showing the first: the game wrote about 26 KiB of the EEPROM
  (0x2000-0x8740, the header at 0x000 naming the airship "Galbana"),
  read back within the session, and to the `.sav` when the window
  closed.
