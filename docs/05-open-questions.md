# Open questions

What is not known yet, with where to look.

## The movies

* **How the VX sound is played**: decoded on the ARM9 (*inferred*) and
  handed to the sound unit how: a channel looping over a buffer the
  player refills, through the SDK's SND library or the registers
  directly? Where the player waits between frames (12 a second against
  60 VBlanks): the sound's position, a timer, a VBlank count? The answer
  decides how the runtime's timing must behave for the picture and the
  sound to stay together. To read in overlay 3 and in the runtime's
  trace when the opening plays.
* **The header's unknown words**: 0x1C (2 with sound), 0x24 (an offset
  into the data, with sound only), the quantiser's role, the frames'
  layout. Not needed for a recompiled port (the game's own decoder runs);
  needed only for a native decoder, which is not planned.
* **What the ITCM's code is, entry by entry**: the decoder's core is
  inferred from the tables it loads and who calls it; the SDK's own ITCM
  functions (the interrupt handler and the four the program calls) are
  to tell apart.

## The code

* **The threads**: how many, and which, the ARM9 and the ARM7 run
  (`OS_SaveContext`/`OS_LoadContext` known: 0x02007A80, 0x02007ACC).
  In the runtime's log, as pc-moon's session 4 did.
* **The touch input**: the SDK's TP library on the ARM9 (*inferred*), its
  sampling rate, and what the game makes of a drag: the selection box,
  the orders. To trace when the tutorial's taps are replayed with
  `ndsrun --input N:tap:X:Y`; a drag may need `--input` to grow a
  `drag` (the oracle has one).
* **The frame rate outside the missions**: no counter found at the
  title or in a movie (`03-executables.md`); stepping frames in melonDS
  (the oracle's `frames:N`) would tell how often the lower screen
  changes there. The airship, the world map and the menus to measure too.
* **Who calls the semihosting functions** (0x02018174, 0x02018188,
  0x0201819C), if anyone, and whether a `throw` happens in play (the
  exception runtime, 0x020184BC-0x0201966C).
* **Scenes 0 and 10-13**: their overlays are loaded but `main` runs
  nothing for them; what sets them (the versus mode, *inferred*).
* **The unmatched ARM7 functions**: 51 of 942, most of them the
  wireless's; whether any is called at the boot (it would show as
  accesses to 0x0480xxxx in the runtime).

## The data

* **The `.bmd2` game sections** (slots 1, 8, 9, 10), the `.rte` routes,
  the `.bsp` stages, the events' scripts in `EventPack.dpk`: the port
  does not need them; a PC version's improvements might (the map's
  extent for the camera, the units' positions for hotkeys).
* ~~How the units are drawn~~: in the 3D, as the map (session 2: with
  every OAM sprite hidden, Vaan and the Flan still drawn; the OAM holds
  only the cursor, the hints and the markers).

## The picture

* **The 3D's lists full in a battle**: once at the start of a chapter 2
  battle (frame 44 033 of session 3's second play) the runtime dropped
  polygons past the DS's 2 048 polygons or 6 144 vertices, as the DS
  does; nothing amiss to the user's eye. Does melonDS meet the limit at
  the same place (a state there, GXSTAT's bit 13)? A wider view (the
  mouse wheel, `06-attack-plan.md`) will draw more of the map and meet it
  sooner: the renderer could keep the polygons past it, as a PC
  version's choice.

## The oracle

* **START during the second movie** (after New Game) was pressed at 22
  s and did not skip it: too early (the movie loading), or the movie
  cannot be skipped? To try later in the movie.
* Loading a savestate and then giving input: Lufia ignored input after a
  load; untried here.
