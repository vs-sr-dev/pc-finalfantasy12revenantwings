# Next session

Session 2 recompiled and booted the game, made the movies and the
logos keep melonDS's time (ndskit `ad61a11`), and ran the route into the
first battle (`00-sessions.md`, `09-recompiler.md`, `11-runtime.md`).
Next:

1. **The user's eyes and ears in the window** (`ndsrun "$ROM" --window
   --save-size 65536 --out build/play`, MSYS2 on PATH): done for the
   logos, the movies, their sound, the first battle and the stylus
   (selections single and by a drag), nothing to report (`00-sessions.md`).
   On through the next missions; anything off goes into `12-picture.md`
   and `13-sound.md`.
2. **The gameplay loop**: the first missions, the airship (overlay 2),
   the preparations (5), the license board (1), a save and a load (the
   512 Kbit EEPROM; the window writes it when it closes). The log's
   `... interpreted (lr ...)` lines, if any appear, read and their rules
   found, as pc-nostalgia did.
3. **The movies' pacing and sound** (`05-open-questions.md`): channels
   12 and 13 loop 704 PCM16 samples at 369 Hz through the whole movie
   (*inferred*: the player's clock); the movies with their own sound
   (BRG, CBE, ...), how the player feeds it.
4. **Drags**: the game's orders and selections are stylus drags;
   `ndsrun --input` has `tap` only. A `drag` (ndskit, with the flow of
   `10-ndskit.md`) if a scripted route needs one; the window's mouse does
   drags already.
5. Then the PC side (`06-attack-plan.md`): the lower screen large, the
   hotkeys, the resolution, the frame rate.

Before starting: MSYS2's tools on PATH (`export
PATH=/c/msys64/mingw64/bin:$PATH`), Windows's Python
(`/c/Python314/python.exe`); the cartridge in `rom/` and extracted;
`build/recomp` built (2 minutes to generate, 1 to build); melonDS's
states in `build/oracle/states/` and `build/oracle/logos/`. ndskit is at
`ad61a11` in this port, the three others and `D:\Homebrew6\ndskit`; any
change keeps the flow of `10-ndskit.md`. Nothing is pushed until the game
plays.
