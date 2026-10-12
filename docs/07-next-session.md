# Next session

Session 2 recompiled and booted the game, made its logos, movies and
battles keep melonDS's time (ndskit `ad61a11`), and the user played it in
the window for 52 minutes, through the prologue and mission 1-1, saving
and loading, with nothing to report (`00-sessions.md`, `09-recompiler.md`,
`11-runtime.md`). The plan agreed with the user: **reach the airship,
then publish**; the PC additions after.

1. **To the airship**: the user plays on from the save in `build/play`
   (copies: `build/play/mission11b.sav.bak`, `mission11.sav.bak`) to the
   airship's own screens (overlay 2 at length), the preparations before a
   mission (overlay 5), the license board (overlay 1), the world map.
   The window: `ndsrun "$ROM" --window --save-size 65536 --out build/play`
   (MSYS2 on PATH; the save written when the window closes). After each
   play, the log: `... interpreted (lr ...)` lines, if any, read and their
   rules found, as pc-nostalgia did; anything off in the picture or the
   sound goes into `12-picture.md` and `13-sound.md`.
2. **The publication**, when the user says the criterion is met and
   authorises it (the PROMPT's list): the repository swept (every blob
   text, no cartridge content), a clean `git clone --recursive` built and
   run to the title, `.recomp.json` with the README's status, the GitHub
   repository created (creation, remote and push as separate commands),
   ndskit's README with its fourth port (the ports table, the layers,
   the checks: this cartridge's movies and the thread switch's order;
   the known gaps) pushed first, then this repository, then the three
   other ports' submodule bumps (already committed locally: pc-moon
   `c7bcad3`, pc-nostalgia `56974e0`, pc-lufiacots `4a694e8`; the README
   commit will need one more bump each), and clones with `--recursive`.
3. **The PC additions** (`06-attack-plan.md`), after the publication:
   * **the view widened with the mouse wheel** (out from the game's own
     view and back, never closer): the battlefield's map *and its units*
     are 3D (checked: with every OAM sprite hidden, Vaan and the Flan are
     still drawn; the OAM holds only the cursor, the hints and the
     markers), so the way is the game's own camera in overlay 0, its
     projection's distance or field of view found and changed by a hook
     of the port's (ndskit: a generic wheel hook), which keeps the
     markers, the touches and the game's culling consistent; widening
     only the renderer's frustum would leave the OAM markers and the
     touches behind;
   * **the language**: the game takes it from the firmware's settings
     (the runtime's are melonDS's defaults, English); an option for the
     others (Italian: "Galkimasela" for the English "Garchimacera");
   * the lower screen large, the hotkeys (the unit tabs, the Espers),
     the resolution, the frame rate.
4. Smaller, any time: the movies' pacing and sound (`05-open-questions.md`:
   channels 12 and 13 loop 704 PCM16 samples at 369 Hz, *inferred* the
   player's clock); a `drag` in `ndsrun --input` if a scripted route
   needs one (the window's mouse drags already).

Before starting: MSYS2's tools on PATH (`export
PATH=/c/msys64/mingw64/bin:$PATH`), Windows's Python
(`/c/Python314/python.exe`); the cartridge in `rom/` and extracted;
`build/recomp` built (2 minutes to generate, 1 to build); melonDS's
states in `build/oracle/states/` and `build/oracle/logos/`. ndskit is at
`ad61a11` in this port, the three others and `D:\Homebrew6\ndskit`; any
change keeps the flow of `10-ndskit.md`. Nothing is pushed until the
user says the game plays and authorises it.
