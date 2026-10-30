# Next session

Session 3 played the first chapter into the second with the user (the
airship, the world map, the preparations, the license board: every one
of the six overlays met, nothing interpreted, `00-sessions.md`) and
published: ndskit with its fourth port, this repository ("playable"),
the three other ports' bumps. The plan agreed with the user: **the PC
additions**, from `06-attack-plan.md`.

1. **The view widened with the mouse wheel** (out from the game's own
   view and back, never closer): the battlefield's map *and its units*
   are 3D (with every OAM sprite hidden, Vaan and the Flan are still
   drawn; the OAM holds only the cursor, the hints and the markers), so
   the way is the game's own camera in overlay 0, its projection's
   distance or field of view found and changed by a hook of the port's
   (ndskit: a generic wheel hook, the kit's first hook: `recomp` has
   none yet), which keeps the markers, the touches and the game's
   culling consistent; widening only the renderer's frustum would leave
   the OAM markers and the touches behind. A wider view draws more of
   the map: the DS's 2 048 polygons and 6 144 vertices will be met
   sooner (`05-open-questions.md`, the picture), and the renderer may
   have to keep what the DS would drop.
2. **The language**: the game takes it from the firmware's settings
   (the runtime's are melonDS's defaults, English); an option for the
   others (Italian: "Galkimasela" for the English "Garchimacera").
3. **The lower screen large**, the hotkeys (the unit tabs, the Espers),
   the resolution, the frame rate.
4. Smaller, any time: the movies' pacing and sound (`05-open-questions.md`:
   channels 12 and 13 loop 704 PCM16 samples at 369 Hz, *inferred* the
   player's clock); a `drag` in `ndsrun --input` if a scripted route
   needs one (the window's mouse drags already); the 3D's full lists
   against melonDS.

The saves: `build/play` (the latest, after the license board opened),
with copies: `session3-ring.sav.bak` (the same), `session3-play1.sav.bak`
(chapter 1's end), `session3-start.sav.bak`, `mission11b.sav.bak`,
`mission11.sav.bak`. The window: `ndsrun "$ROM" --window --save-size
65536 --out build/play`.

Before starting: MSYS2's tools on PATH (`export
PATH=/c/msys64/mingw64/bin:$PATH`), Windows's Python
(`/c/Python314/python.exe`); the cartridge in `rom/` and extracted;
`build/recomp` built (2 minutes to generate, 1 to build); melonDS's
states in `build/oracle/states/` and `build/oracle/logos/`. ndskit is at
`234b110` in this port, the three others and `D:\Homebrew6\ndskit`; any
change keeps the flow of `10-ndskit.md`, and is pushed with each port's
bump once checked.
