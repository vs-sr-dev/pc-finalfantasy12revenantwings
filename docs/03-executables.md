# The code

Read with ndskit (`arm`, `recomp.discover`) and Ghidra 12.1.2, and seen
running in melonDS through its savestates. *Inferred* marks what is read
from the shape of the code without a run to confirm it.

```sh
ROM="rom/Final Fantasy XII - Revenant Wings (Europe) (En,Fr,De,Es,It).nds"
A9="build/extract/sys/arm9.bin --base 02000000"
python -m ndskit.arm $A9 --at 02000800 --count 110        # crt0
python -m ndskit.arm $A9 --at 02000BB8 --count 170        # main, its scene loop
python -m ndskit.arm $A9 --at 0200D410 --count 62         # FS_StartOverlay
python -m ndskit.recomp.discover "$ROM" --cpu 9 --report --out build/disc/funcs9.tsv
python -m ndskit.recomp.discover "$ROM" --cpu 9 --overlay all --report --out "build/disc/f_{id}.tsv"
python -m ndskit.recomp.discover "$ROM" --cpu 7 --report --out build/disc/funcs7.tsv
```

## The ARM9

* **crt0** at 0x02000800: the SDK's (CP15, the TCMs, the stacks,
  clearing the DTCM, the palettes and OAM), `MIi_UncompressBackward`
  (0x02000950) with ModuleParams' compressed end, which is 0 (the
  program is plain), the autoloads (0x020009FC), the BSS, the ITCM's
  address stored at the DTCM's top, three calls (0x02018170, a lone `bx
  lr`; 0x02000B60; **0x02019694**, which calls each function of the
  static initialisers' table at 0x0206ACB8), then `bx` to **`main` at
  0x02000BB8** with lr = 0xFFFF0000.
* **`main`** (0x02000BB8) initialises (0x0204710C, 0x02047610,
  0x020473AC, the save module 0x020359C4, ...), then loops for ever:
  0x02000D40 loads the overlay of the next scene, `0x02040110` returns
  the scene's number (0-15, a halfword reached through the game's
  manager at 0x020811A8), and a switch calls the scene's entry, **in the resident
  overlay** (most at its first function, 0x020838C0, with arguments
  saying which part):

  | Scene | Overlay loaded | Entry called by `main` |
  |---|---|---|
  | 1 | 4 (title) | 0x02083918 (0) |
  | 2 | 2 (airship) | 0x02095BA8 |
  | 3, 4 | 2 (airship) | 0x020838C0 (0), (1) |
  | 5 | 0 (missions) | 0x020860BC (0, 0x020415FC's result, 0) |
  | 6, 7, 8 | 5 (preparations) | 0x020838C0 (0, 0), (1, 0), (2, 0) |
  | 9 | 1 (license board) | 0x020838C0 |
  | 14, 15 | 3 (movies, ending) | 0x02083B84 (0), 0x02083BE0 (0) |
  | 0, 10-13 | 4, 4, 0, 5, 4 | none: the loop goes round |

  0x02000D40 maps the scene to an index (stored at 0x0206ACC0) into a
  table of overlay ids at 0x0206ACC4 (0, 4, 5, 2, 1, 3) and calls
  **`FS_LoadOverlay` (0x0200D504)**: `FS_LoadOverlayInfo` (0x0200D1F0),
  `FS_LoadOverlayImage` (0x0200D2EC), **`FS_StartOverlay` (0x0200D410)**.
* `FS_StartOverlay` is SDK 4.0's: when the boot type at 0x027FFC40 is 2
  (a downloaded program), the overlay's digest is checked against a
  table at 0x0206D434 (empty here: its start and end are the same
  address), and a mismatch clears the overlay and stops (0x02009144);
  otherwise it undoes the backward LZ when the entry's flag says so
  (never, here), flushes the caches and calls the static initialisers.
  Right after it, at 0x0200D558, lie SHA-1's initial constants (the
  digest's code, *inferred*).
* **The SDK's threads**: `OS_SaveContext` at 0x02007A80 and
  `OS_LoadContext` at 0x02007ACC (`ldm r0, {r0-r14}^; mov r0, r0; subs pc,
  lr, #4`), each saving or restoring the divider's and square root's state
  first (0x0200DDD8, 0x0200DE18: `CP_SaveContext`, `CP_RestoreContext`,
  *inferred*); `OS_Terminate` at 0x02009144 (interrupts off, then CP15's
  wait for interrupt, for ever). How many threads run is to see in the
  runtime.
* **The save module** (0x020359C4, called by `main`): the backup type
  **0x1001** (a 512 Kbit EEPROM) stored at 0x0206B80C, then
  `CARD_LockBackup` and `CARD_IdentifyBackup` (0x0202AED8 calls
  0x0200FE3C and 0x020103E0, *inferred* names from the SDK's order); if
  that fails, `b .`, a stop for ever.
* **C++**: CodeWarrior's, with RTTI (`St9type_info`, the
  `__cxxabiv1` type infos, class names `11BLC_I2DBase`,
  `17BLC_WindowConfirm`, `13Scene_Warning`, ...): the UI is a class
  library (`BLC_`), scenes are classes. The exception machinery is
  linked (below: what Ghidra finds that discovery does not).
* **Debug output through ARM's semihosting**: three functions at
  0x02018174, 0x02018188, 0x0201819C issue `swi 0x123456` with r0 = 3, 7
  and 0x18 (`SYS_WRITEC`, `SYS_READC`, the exit), CodeWarrior's console
  (*inferred*: never called in a release; on a DS `swi 0x123456` would
  be the BIOS's function 0x12). Who calls them is to see.

## The movies' decoder

Actimagine's VX library is linked into the program (`[SDK+Actimagine:VX]`
at 0x02000BA4). **The player is overlay 3** (it opens
`videos/movielist.bvx` and checks the `VXDS` magic at 0x0208623C), and
**the decoder's core is in the ITCM**, placed there by the ARM9's
autoload at the boot (0x6BA0 bytes from 0x0206D440): overlay 3 calls
the ITCM at 0x01FF82F0, 0x01FFDCD0 and 0x01FFE9F8, and the two largest
ITCM functions (0x01FFD6A4, 1 644 bytes; 0x01FFDCD0, 1 372) load
addresses of tables in the DTCM (0x027E0060, 0x027E00AC, 0x027E00CC,
0x027E01A8, 0x027E0B40), which the DTCM's autoload fills from bytes
that look like a codec's quantiser and scan tables (0x020742E0 on); the
main program calls only four small ITCM functions of the SDK's.
*Inferred* from this: the ITCM holds the VX decoder, as Moon's held
Mobiclip's, but statically. **Checked in melonDS**: in a state taken
during the opening movie overlay 3 is resident (`melonds --overlays`:
99.99% of its bytes), and the ITCM's 0x6BA0 bytes are the autoload's,
word for word, as they are at the title and in a battle: nothing is
copied there at run time. ndskit's recompiler takes the autoloads as
segments, so **no `--copy` is needed** here. The ITCM also holds **many functions that overlap**:
entries 12 bytes apart into the same unrolled code (0x01FF97BC,
0x01FF97C8, 0x01FF97D4, ..., each 120 or 488 bytes; 356 ITCM entries
in all), *inferred* the decoder's block copies and interpolations
entered at the right step. Discovery takes each entry as a function of
its own, which the recompiler emits as such.

## Function discovery, and Ghidra

| Program | Functions | Thumb | Switches | Conflicts |
|---|---|---|---|---|
| ARM9 alone (ITCM, main, DTCM) | 3 274 | 9 | 75 (1 087 targets) | 0 |
| ARM9 with what its overlays reach | 3 610 | | | 0 |
| overlay 0 (missions) | 2 621 | 0 | | 0 |
| overlay 1 (license board) | 290 | 0 | | 0 |
| overlay 2 (airship) | 1 595 | 0 | | 0 |
| overlay 3 (movies) | 95 | 0 | | 0 |
| overlay 4 (title) | 11 | 0 | | 0 |
| overlay 5 (preparations) | 273 | 0 | | 0 |
| ARM7 | 942 | 9 | 40 (706 targets) | 0 |

Almost all ARM (the nine Thumb functions are the SDK's veneers), **no
conflict anywhere**: no descent meets data or an undefined instruction,
in the program, any overlay or the ARM7. 4 to 10 functions of each
overlay are reached from outside it. The whole discovery takes about 80
seconds (`--overlay all` 70 of them).

**Against Ghidra** (12.1.2, the ARM9's main block 0x02000000-0x0206D440
as a flat binary with the entry as root, `ndskit/ghidra/ExportFuncs.java`):
2 607 functions. **2 596 are discovery's entries**; the other 11 are
one cluster, 0x020184BC-0x0201966C, which calls itself and is reached
only from code after a function's epilogue (0x0201974C: `bl 0x02019C5C;
add r0, r11, #0; bl 0x0201966C`, after the `pop` that ends 0x02019704):
**the catch blocks and CodeWarrior's exception runtime**, entered by
the unwinder through the exception tables, not by calls (*inferred*, as
pc-moon's and pc-lufiacots's notes). 643 of discovery's functions are not
Ghidra's (methods reached through vtables, thunks, the ITCM's entries).

## The ARM7

SDK 4.x's component (crc32 0x60577F9F), 942 functions, 40 switches, **0
conflicts**. Function by function (each function's words with branch
offsets and addresses in literals masked, `01-cartridge-layout.md`):
**871 of 942 as Moon's**, 873 as Nostalgia's, 454 as Lufia's. The 51 in
none of them: 26 in its main-RAM autoload (0x027E0000-0x027F7600), 24 in
the shared WRAM, one in its crt0's segment (0x0238015C); 9 of them load
wireless registers' addresses (0x04808xxx, 0x04805F7E), others the
VCOUNT, DISPSTAT, IF, IME, KEYCNT and RCNT. *Inferred*: an older
wireless driver and its neighbours; the sound, touch, RTC, power and
backup are Moon's code.

## Anti-piracy

None found. Only the SDK's CARD library reads the card's registers
(ROMCTRL, AUXSPICNT, the data port 0x04100010: 0x020105A4-0x020109C8, by
`CARD_IdentifyBackup` at 0x020103E0); **no overlay** loads the card's
registers, the timers' (0x04000100-0x0400010F) or the DSi's SCFG
(0x04004000) addresses; discovery meets no encrypted or unreadable code
in any overlay. A 2007 game, before such modules were common
(*inferred*).

## The frame

**30 frames a second in a mission**: measured in melonDS from savestates
(`tools/oracle.py`), a counter of the game's at **0x020811A0** (by the
manager object 0x020811A8) advances by half the SDK's VBlank count
(0x027FFC3C) in the first battle (the Glabados Ruins, the tutorial):
+59 over 119 VBlanks, +789 over 1 578. Beside it, 0x0208122C and words
of heap objects (0x021865D8, 0x021994BC, 0x021867B0) follow the VBlank
count itself. At the title and during the opening movie 0x020811A0 stays
0 and no 32-bit word of main RAM other than the VBlank count advances
with it: their rate is not measured yet (the movies are 12 frames a
second as files, `02-data-formats.md`).
