# The cartridge

Everything here was read from the cartridge with ndskit (`python -m
ndskit.rom ROM --info`, `--list`, `--extract build/extract --nested`) and
this port's `tools/`, or seen running in melonDS, unless marked
*inferred*.

## Identity

| Field | Value |
|---|---|
| File | `Final Fantasy XII - Revenant Wings (Europe) (En,Fr,De,Es,It).nds`, 128 MiB image, 0x076F794C bytes used; SHA-1 b75f226ea6698ac28dec97218336d080caa06702 |
| Title, code, maker | `FFXIIREWINGS`, `AXFP` (Europe), `GD` (Square Enix) |
| Unit, region, version | 0 (DS), 0, 0 |
| Header CRC, logo CRC | 0xAAAA, 0xCF56: both correct |
| Secure area | decrypted (the 0xE7FFDEFF marker), its CRC 0x4BB0 |
| SDK | **NitroSDK 4.0** (ModuleParams' relstep 30000); Moon and Nostalgia 4.2, Lufia 5.3 |
| Banner | version 1; every language, Japanese included: "FINAL FANTASY XII / REVENANT WINGS / SQUARE ENIX" |
| Middleware | `[SDK+Actimagine:VX]` beside the SDK's `[SDK+NINTENDO:BACKUP]` in the ARM9 (0x02000BA4): Actimagine's VX video codec |

On screen (melonDS, from a new cartridge): the logos of **Square Enix**
(upper screen) and **Think & Feel Inc.** (lower) at about 3 s; then the
**Ivalice Alliance** logo with "Licensed by Nintendo" (upper) and
**Actimagine's "video codec"** logo (lower) at 6 s; then the opening
movie with the staff over it (Director Motomu Toriyama; Co-directors
Katsuyoshi Yamaki (Think & Feel Inc.) and Takanari Ishiyama; Art
Supervisor Isamu Kamikokuryo; Movie Director Eiji Fujii; Music Hitoshi
Sakimoto (Basiscape Co., Ltd.) and Kenichiro Fukui; Lead Graphic
Designer Sho Okamura; Producers Yasuhito Watanabe and Eisuke Yokoyama;
Executive Producer Akitoshi Kawazu); then the logo, and the title at
about 55 s: "New Game", "Continue", and **"© 2007, 2008 SQUARE ENIX
CO.,LTD."** on the lower screen. START during the opening goes straight
to the title (pressed at 14 s, the title at 16 s).

So: a game of 2007 (Japan) released here in 2008, developed by Think &
Feel with Square Enix, as the copyright line and the co-director's
credit say; the year of the Japanese release itself is not on this
cartridge (*inferred* from the line's first year).

## The two programs

| | ARM9 | ARM7 |
|---|---|---|
| Stored at | 0x4000, 0x75038 bytes | 0x154200, 0x26948 bytes |
| Runs at | 0x02000000, entry 0x02000800 | 0x02380000, entry 0x02380000 |
| Compressed | no (ModuleParams' compressed end is 0) | no |
| crc32 | 0x01C5B80E | **0x60577F9F** (Moon's 0x1B16DBE2, Nostalgia's 0x3DFBBAA1, Lufia's 0x3F0CD426) |
| Static BSS | 0x0206D440-0x020838C0 | |
| Autoloads | ITCM 0x01FF8000 (0x6BA0 bytes, from 0x0206D440), DTCM 0x027E0000 (0x1040, BSS 0x20, from 0x02073FE0) | shared WRAM 0x037F8000 (0xF180, BSS 0x3E94), main RAM 0x027E0000 (0x17600, BSS 0x1968) |

The ARM7's ModuleParams (0x02380198) are found by their shape, as on the
other SDK 4 cartridges; its crt0 clears the WRAM, sets the stacks,
copies the autoloads (0x02380100), clears the BSS, calls 0x0238015C and
jumps to 0x037F8000. The ARM7 is the SDK's component of SDK 4.x: of its
942 functions, **871 are Moon's** (the same code but for branch offsets
and addresses in literals), 873 Nostalgia's, 454 Lufia's; 51 (23 412
bytes) are in none of the three, and most of those load the wireless
registers' addresses (0x0480xxxx): the wireless driver of an older SDK,
*inferred* (`03-executables.md`). Its sound driver is Moon's and
Nostalgia's.

## Overlays

Six ARM9 overlays, none for the ARM7, **none compressed**, all at **one
load address, 0x020838C0** (the static BSS's end): one is resident at a
time, chosen by the scene (`03-executables.md`).

| Overlay | Size (BSS) | Functions | What it is (from the files it names and when it is loaded) |
|---|---|---|---|
| 0 | 0x62AC0 (0x860) | 2 621 | **the missions**: the battlefield in real time (stages `Stage.dpk`, maps `map_%04d*.bmd2`, collision `CLD_%04d*.bmd`, routes `Route_%04d_w/f.rte`, AI `AI_%06d.aic`, units, effects, events) |
| 1 | 0x89E0 (0x8A0) | 290 | the **license board** (`data/Shellscreen/wmap/license_*`, `License.bsl`, `St_SL_All.btx`) |
| 2 | 0x571A0 (0x49C0) | 1 595 | **the airship** (the Galbana: `data/homeship/...`, its conversations, shop, trade, the world map `WorldMap.bmw`, events `EventHS_%08d.bev`) |
| 3 | 0x4C20 (0x4C0) | 95 | **the movies** (`videos/movielist.bvx`, the VX player; `VXDS` is checked at 0x0208623C), the ending and its staff scroll (`theend/`, `scroll_%03d.dcg/.dcl`, `St_Ev_Scroll_%03d.bst`) |
| 4 | 0xE60 (0x20) | 11 | **the title** (`title/bg_pack.narc`, `title_obj_font`) |
| 5 | 0x126E0 (0x560) | 273 | the **preparations** before a mission (`preparations/`, party, items, the minimap) |

The scene a number names and the overlay it loads are read in `main`
(`03-executables.md`). In melonDS's states (`python -m ndskit.melonds
STATE --overlays ROM`): overlay 3 is resident during the opening movie,
4 at the title, 0 in the first battle, each with all of its bytes.

## The file system

2 146 FAT entries: **2 140 named files in 202 directories** and the six
overlays. By extension (`--list`, and the census of their first bytes):

| Kind | Files | Bytes | What |
|---|---|---|---|
| `.narc` | 1 228 | 16.5 MB | the SDK's NARC archives: G2D (2 304 NSCR, 1 039 NCLR, 906 NCGR, 820 NCER, 813 NANR, 10 NMCR, 10 NMAR) and G3D (163 NSBMD, 356 NSBMA, 84 NSBCA, 41 NSBTA, 14 NSBTP) members, and the game's `ADCL` (53) |
| `.bmd2` | 72 | 27.5 MB | **maps**: the SDK's G3D model with its animations and two game sections (`02-data-formats.md`) |
| `.dpk` | 42 | 26.3 MB | **packs** of members by id (`tools/dpk.py`) |
| `.vx` | 20 | 22.4 MB | **movies**, Actimagine VX (`tools/vx.py`) |
| `.sdat` | 1 | 15.0 MB | the sound archive |
| `.dcg`, `.dcl` | 2, 2 | 3.0 MB | the ending's scroll pictures and palettes |
| `.rte` | 93 | 2.5 MB | the maps' routes (`Route_<map>_w`, `_f`: walking and flying, *inferred*) |
| `.NCGR`, `.NCLR`, `.NSCR`, `.ncbr`, `.nclr` | 36, 37, 37, 3, 2 | 1.9 MB | G2D files outside archives |
| `.ADCE` | 52 | 1.3 MB | characters' cells (magic `CADP`) |
| `.bmd` | 20 | 1.1 MB | collision and cloud models (`CLD_`, `wmp_*kumo`): the same container as `.bmd2` |
| `.bsk`, `.bit`, `.bch`, `.bjo`, `.blv` | 5, 5, 5, 1, 1 | 1.8 MB | the game's tables: skills (`SKIL`), items (`ITEM`), characters (`CHAR`), jobs (`JOB`), job levels (`JOBL`), per language where they hold text |
| `.hscd`, `.hsrt`, `.hsev`, `.hsnp`, `.hsnl`, `.hsgn`, `.hsld`, `.hsjd`, `.hsar` | 95, 10, 13, 91, 12, 12, 2, 1, 1 | 0.9 MB | the airship: conversations (`HSCD`), results (`HSRD`), events (`HSEV`), its people (`HSNP`, lists `HSNL`), ... |
| `.btx`, `.brt`, `.btk`, `.bst`, `.bmw` | 110, 25, 5, 6, 5 | 1.6 MB | **text**, per language |
| others | 30 kinds | | small tables (`bce` `CelL`, `bpa` `PATT`, `bid`/`boj` `HOBJ`, `bfo` `FORM`, `bol` `EZPL`, `ptrl` `PTRL`, `ban`/`brd`/`brb`/`ben` `RECI`, ...) |

**Languages**: English, French, German, Italian and Spanish, each in its
own directory (`E`, `F`, `G`, `I`, `S`) wherever a file holds text: the
program text (`data/progtext/*/`, 21 files each), the events' text
(`EventPackTxt.dpk`), the airship's conversations, the tables with
names, the mission titles and the minimap labels (as pictures).

Other things on it: `etc/sumicon.bnr`, a second banner (version 1, its
CRC 0xD898; *inferred*: the icon shown to other systems in wireless
play); `data/Shellscreen/network/` and `missiontitle/netvs_start`,
`netvs_clear` (named in the program): a **wireless versus mode**
(*inferred*); `sound/sound_data.sadl` (the sound archive's symbols as C
`#define` lines, a build tool's output) and `sound/se_list.bse`;
`data/license/License.bsl`.

## The save

The game's save module identifies its backup memory as **0x1001**, the
SDK's `CARD_BACKUP_TYPE` of a **512 Kbit EEPROM** (0x020359D4: the type
stored at 0x0206B80C, then `CARD_LockBackup` and `CARD_IdentifyBackup`,
and a stop `b .` if that fails). melonDS makes a 64 KiB `.sav` for it, in
which the game writes at the boot a header "BLIZ" at 0x000 and again at
0x400, the rest 0xFF. ndskit's runtime needs `--save-size 65536` for a
new cartridge, as Nostalgia and Lufia.
