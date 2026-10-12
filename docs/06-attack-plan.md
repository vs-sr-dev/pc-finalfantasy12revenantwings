# The porting route

## Verdict: feasible, by static recompilation, as the three before it

The same road as pc-moon (its `06-attack-plan.md` weighs the others),
pc-nostalgia and pc-lufiacots: both programs recompiled to C++ by
ndskit, the DS's hardware replaced at its registers by ndskit's runtime,
melonDS as the oracle. Moon took six sessions from nothing to playing
with picture and sound, Nostalgia three, Lufia two; most of that work is
ndskit's and is reused here as it is. This is ndskit's fourth game, and
on the cartridge it looks like the gentlest: nothing compressed, no
anti-piracy, six overlays at one address, discovery with no conflict
anywhere and Ghidra's functions all found but the exception runtime's.
What is new is what it shows and how it is played: **movies in
Actimagine's VX**, and **a real-time strategy game on the touch
screen**.

What is the same as before (and so already done):

* CodeWarrior's C++ (with RTTI), the SDK's crt0, threads, interrupts,
  IPC, `FS_StartOverlay`; the 3D in the SDK's G3D (the maps are NSBMD
  models), the 2D in its G2D, the music sequenced on the ARM7.
* **The ARM7 is Moon's and Nostalgia's** but for 51 functions of 942,
  mostly the wireless driver's (`03-executables.md`): the sound, touch,
  RTC and power code the runtime already answers.
* IMA-ADPCM samples, PSG and noise instruments, as Nostalgia's and
  Lufia's.
* A 512 Kbit EEPROM (`--save-size 65536`), as Nostalgia's and Lufia's.
* 30 frames a second in a mission, as Nostalgia and Lufia.
* **Overlays at one address**, one resident at a time, as Nostalgia's
  slots: the per-function residency of pc-lufiacots follows that as it
  is.

What is new, and what it may ask of ndskit:

| New here | Why it matters | In ndskit |
|---|---|---|
| **VX movies** (10, both screens, 12 fps, with their own sound at 32 kHz in the upper screen's file) | the decoder runs on the ARM9 from the ITCM (statically placed: no `--copy`, `03-executables.md`), hundreds of overlapping entries into unrolled code; the sound is the codec's, not the SDK's streams: decoded on the ARM9 and played through the sound unit, *inferred* (how: to read when the first movie plays) | nothing expected for the code (an autoload is a segment like any other; overlapping entries are functions like any other); the sound unit as it is, its timing checked by ear against melonDS (A/V sync depends on how the player paces itself: a channel's position, a timer, the VBlank) |
| **SDK 4.0** (the oldest yet), its ARM7 with an older wireless driver | the 51 different functions; the wireless is used only by the versus mode (*inferred*) | nothing unless the wireless is started at the boot (the runtime would see writes to 0x0480xxxx) |
| **a game played with the stylus** (selecting units, drawing orders, the unit tabs, the menus) | every interaction is a touch or a drag on the lower screen; the battlefield *is* the lower screen | the window's mouse as the stylus exists (pc-moon); drags must be smooth and continuous (the touch sampled every frame), and the window's layout must make the lower screen the large one (below) |
| **C++ exceptions linked** (the unwinder and catch blocks, the 11 functions Ghidra has and discovery not) | a `throw` at run time would jump into a catch block up the stack: ndskit's known gap | nothing unless one is thrown; the interpreter takes the catch blocks' code if it is reached (*inferred*); to watch for in the log |
| **semihosting calls** (`swi 0x123456`, CodeWarrior's console) | the BIOS's HLE would take one as SWI 0x12 | nothing unless they are called (*inferred*: not in a release); to watch for |
| **the battlefield's 2D units on a 3D map** | units are cells (`.ADCE`, NCER), drawn as 2D sprites or as 3D quads: which decides what "the 3D at the window's resolution" gives the units | to read in the runtime (OAM or polygons) |

What is not here: no compressed code, no anti-piracy, no streams, no
flash save, no nested archives, no Thumb to speak of. Out of scope: the
**wireless versus mode** (ndskit has no wireless; the game's single
player is whole without it).

## Where to cut

Unchanged from pc-moon's plan: everything at the hardware registers, the
BIOS's SWIs in HLE, the ARM7 recompiled and run as a coroutine, the 3D's
geometry engine in software in the DS's fixed point and its rendering on
OpenGL at the window's resolution, overlays told apart function by
function, the interpreter for code no module holds.

## A better Revenant Wings on PC

### The screens

On the DS **the battlefield is the lower screen** (the 3D map, the units,
the orders drawn on it) and the upper screen holds the map board with
the units' marks, the leader's tab and the combat log (the Glabados
Ruins, `00-sessions.md`). On PC: **the lower screen as the main view**,
large, and the upper one as a panel beside it (or above it, smaller), at
the player's choice, with a key to swap them; the menus that use both
screens as they are, side by side.

### The mouse as the stylus

The stylus's whole vocabulary is the mouse's: a click selects, a drag
draws an order (the cursor's boots, the attack's swords), a drag from
empty ground selects units in a rectangle (*inferred*: to see in play).
The window maps the mouse to the lower screen wherever it is drawn and at
whatever size, and samples it every frame so drags are smooth. The right
button could stand for a common action (cancel, or the "order" of the
selected units) once the game's gestures are read.

### Hotkeys

The unit tabs (the leaders at the top of the lower screen) on 1-5, the
summons (Espers) and the party's commands on keys or a gamepad's
buttons, the camera scrolled with the arrows or the screen's edges,
pause on a key: each is a touch at a known place of the lower screen,
which the port can synthesise without changing the game. The DS's own
buttons stay mapped as melonDS's.

### Resolution and frame rate

The 3D maps at the window's resolution, as Moon's and Lufia's; the 2D
(the units if they are sprites, the HUD, the portraits) at 256 × 192
scaled without blurring. The missions run at 30: first **a steady 30**,
then 60 by interpolating the 3D between the game's frames, if the units
and the camera can follow (to read where the frame loop waits). The
movies are 12 frames a second at 256 × 192 and stay so.

## The phases

| Phase | What | Done when |
|---|---|---|
| 1. Recognise (session 1) | the cartridge, the formats, the code, the oracle, this plan | this document |
| 2. Recompile | the program, its six overlays, the ARM7 as modules; the self-test with this game's functions (the program, the ARM7, overlays 0 and 2) and ndskit's instruction test | everything compiles; the self-test has no difference, recompiled and interpreted |
| 3. Runtime | the boot, the logos, the opening movie (overlay 3, the ITCM's decoder), the title; the save (512 Kbit) | its memories against melonDS's states at the same VBlank: the opening, the title |
| 4. The route | New Game, the second movie, the Glabados Ruins' tutorial with taps (`--input N:tap:X:Y`) | the run and `glabados_tutorial.ml1` at the same moment; the interpreter's log (`... interpreted`) read and the misses' rules found |
| 5. Picture | the movies on both screens, the title, the battlefield (3D map, units, HUD), the airship | the pictures against melonDS's at the same frames; the user's eyes |
| 6. Sound | the music and effects (ADPCM, PSG, noise), **the movies' sound** | the channels against melonDS's; the user's ears |
| 7. Publication | ndskit proven on four games: the five repositories, the ports' submodules bumped | Revenant Wings plays "as far as anyone knows" |
| 8. PC | the screens' layout, the mouse as the stylus, hotkeys, the resolution, the frame rate | played by the user |

## Oracle

melonDS (`D:\Tools\melonDS-oracle`), driven by `tools/oracle.py`
(pc-lufiacots's). The route from a new cartridge into the first
controllable moment:

    python tools/oracle.py --fresh --out build/oracle/r3 --at "14:START,17:tap:128:130,30:A,32:A,...,90:A,92:tap:190:112,..."

START at 14 s skips the opening (the title at 16 s); a tap on "New
Game" (128, 130 on the lower screen) at 17 s starts the second movie
(the Glabados Ruins seen from the sky; START pressed at 22 s did not
skip it), which ends at about 37 s; then **"Prologue: In Search of the Eternal / The
Glabados Ruins"** on the lower screen, Vaan's lines (A advances them),
**"COMMENCE!"** at about 67 s, and the tutorial ("Controlling Units"):
its texts advance with A, and it waits for an order (a tap on the Flan
at 190, 112 was taken: the tutorial went on to moving, "Touching an open
space on the battlefield will cause the cursor to change to a pair of
boots"). States kept in `build/oracle/states/`: `opening.ml1` (the
opening movie, VBlank 2 387), `title.ml1` (4 787), `glabados_tutorial.ml1`
and `glabados_tutorial2.ml1` (5 984 and 6 103, two seconds apart),
`glabados_battle.ml1` (7 681). A press at wall-clock second t lands near
VBlank 60 t, less the boot's; the oracle's times differ by a few frames
from run to run.
