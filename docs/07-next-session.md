# Next session

Session 1 read the cartridge, its formats and its code, drove melonDS
from a new cartridge into the first battle, and wrote the plan
(`00-sessions.md`, `06-attack-plan.md`). Next, phases 2-4 of the plan:

1. **Recompile**: `python -m ndskit.recomp "$ROM" --out build/recomp
   --optest`, then CMake and Ninja. **Done at the end of session 1** as a
   head start: 10 modules (the program, six overlays, the ARM7, the two
   instruction tests), 16 737 functions, none handed to the interpreter;
   2 min 14 s to generate, 1 min 9 s to build, no warning; the instruction
   test 57 781 vectors with no failure, recompiled and `--interp`. Next
   in the self-test: vectors of this game's
   functions that run alone (`python -m ndskit.recomp.selftest "$ROM"
   --cpu 9 --auto`, `--cpu 7`, `--overlay 0`, `--overlay 2`: the program,
   the ARM7, the missions' and the airship's overlays), recompiled and
   `--interp`; a failure is read before anything else.
2. **Boot to the title** (`ndsrun "$ROM" --save-size 65536 --out
   build/title --vblanks 4790`): the logos, the opening movie (overlay 3,
   the ITCM's VX decoder: no `--copy`), the title; against
   `build/oracle/states/opening.ml1` (VBlank 2 387) and `title.ml1`
   (4 787) with `python -m ndskit.melonds STATE --compare build/title`.
   The log's `... interpreted (lr ...)` lines collected; the overlays'
   changes of hands (3 for the opening, 4 at the title).
3. **The movies**: how the VX player paces itself and plays its sound
   (`05-open-questions.md`); the picture on both screens (`--shots` on
   consecutive frames) against melonDS's; the opening's music
   (`SEQ_56FFTheme`, *inferred*) and a movie's own sound by ear.
4. **The route into the Glabados Ruins**: `--input` with START (the
   opening skipped), the tap on New Game, A for the lines, the tap on the
   Flan; the run at the same VBlank as `glabados_tutorial.ml1` (5 984)
   compared. The orders are drags: `ndsrun --input` has `tap` only; a
   `drag` added to ndskit (with the flow of `10-ndskit.md`) if the route
   needs one.
5. **The window**, when the user asks: `ndsrun "$ROM" --window
   --save-size 65536 --out build/play` (MSYS2 on PATH), the mouse on the
   lower screen as the stylus; the save written when the window closes.
6. Then the PC side (`06-attack-plan.md`): the lower screen large, the
   hotkeys, the resolution, the frame rate.

Before starting: MSYS2's tools on PATH (`export
PATH=/c/msys64/mingw64/bin:$PATH`), Windows's Python
(`/c/Python314/python.exe`); the cartridge in `rom/` and extracted
(`build/extract`); melonDS's states in `build/oracle/states/`. ndskit is
at `5ee24af` in this port, the three others and `D:\Homebrew6\ndskit`;
any change to it keeps the flow of `10-ndskit.md`. Nothing is pushed
until the game plays.
