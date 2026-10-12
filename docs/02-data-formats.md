# The data formats, at a glance

Read on the extracted files (`python -m ndskit.rom ROM --extract
build/extract --nested`), with `tools/dpk.py`, `tools/vx.py` and ndskit's
`sdat`. A recompiled port does not need to understand the game's data:
its own code reads it. What follows is what was checked, to know what is
there and where the movies and the sound come from; *inferred* marks a
reading from shape alone.

## The SDK's formats

* **NARC** archives (1 228 files; 894 more inside the packs, and 770
  compressed there): the
  usual header, `BTAF` (the members' extents), `BTNF` (no names here),
  `GMIF`. 1 to 135 members each (691 of the files have 4). Their members:
  the SDK's **G2D** (NCGR, NCLR, NSCR, NCER, NANR, NMCR, NMAR) and **G3D**
  (NSBMD, NSBCA, NSBTA, NSBTP, NSBMA), and the game's `ADCL` (53, the
  characters' link data, *inferred* from the program's `_CA:LNK.ADCL`).
  The program opens members by name through a path prefix (`_CA:CEL.NCER`,
  `_MA:/ica_%03d.nsbca`, `_BG:BG000.NCGR`, `ARC:TELEPO/PLT.NCLR`, ...).
* G2D and one NSBMD (`data/worldmap/beyrude.nsbmd`) outside archives;
  the effects' and the ending's characters as `.ncbr`/`.NCBR` (NCGR
  inside: `RGCN`).
* **NFTR fonts**: the four members of `data/FontPack.dpk`.
* **The sound**: one SDAT (`sound/sound_data.sdat`, 15 MB), below.

## Packs (`.dpk`)

42 files, 6 533 members. A count, then a record of three words per
member (an id, its offset, its size), the members after the table in
order, each padded to 16 bytes with 0xEE. Every member of every pack lies
inside it (`tools/dpk.py build/extract --list`). What they hold:

| Pack | Members | Kind |
|---|---|---|
| `FontPack.dpk` | 4 | NFTR fonts |
| `effect/EffectPack.dpk` | 384 | NARCs (the effects, opened as `_PK:B%06d.NARC`) |
| `Illustration/full*/CharaIllust.dpk` | 164 ×2 | NARCs (the characters' portraits; `full_2P`: *inferred*, the second player's in versus) |
| `Shellscreen/minimap/MapNcgr/Nclr/Nscr.dpk` | 70 ×3 | NCGR, NCLR, NSCR of the minimaps, ids by map number |
| `Shellscreen/obj_illust/ObjIllust.dpk`, `unit_icon/UnitBody.dpk`, `UnitHead.dpk` | 63, 109, 10 | NARCs |
| `Shellscreen/missiontitle/*/ChapterClear.dpk`, `MissionTitleNarc.dpk`, `SubtitChapter.dpk` | 11, 131, 12 per language | **LZ10-compressed** NARCs (the BIOS's LZ77; each decodes to its size within the member) |
| `stage/*/Stage.dpk` | 158 per language | LZ10-compressed stage data (the `.bsp` the program names: `data/stage/Stage_%06d.bsp`) |
| `event/EventPack.dpk`, `homeship/event/HsEventPack.dpk` | 497, 148 | the events' scripts (*inferred*), ids 101000-40000000 |
| `event/*/EventPackTxt.dpk`, `homeship/event/*/HsEventPackTxt.dpk` | 496, 148 per language | the events' text, under the scripts' ids |

## Maps (`.bmd2`, `.bmd`)

92 files (72 `.bmd2`, 20 `.bmd`). Eleven words: the first 0x4F in
every file, then ten offsets into the file, 0xFFFFFFFF where a part is
absent:

| Slot | Present in | What it points at |
|---|---|---|
| 2 | all 92 | the SDK's **BMD0** (an NSBMD model), always at 0x2C |
| 3 | 23 | BTP0 (texture pattern animation) |
| 4 | 72 | BTA0 (texture SRT animation) |
| 6 | 13 | BMA0 (material animation) |
| 8 | all 92 | a count, then named records with IEEE floats (`map01`, positions: *inferred* the map's points) |
| 1 | the 72 `.bmd2` | a game section beginning 0x00011000 |
| 9 | 71 | a grid (9 × 9 words in the first file; *inferred* heights or areas) |
| 10 | 2 | a game section |

Slots 5 and 7 are never used here (*inferred*: BCA0 and BVA0 in the SDK's
order of animation kinds; the program knows `.nsbva`). The maps' names
carry their number and a tag (`map_0010_cle`, `map_0110_rab`,
`_shp_in`, `_tpl`, `_sky_mrn`, `_lnd_jng`, `_castle`, `_last`, `wmp_*`
for the world map: *inferred* places, Rabanastre, the airship, temples,
the sky, the land, the last dungeon). The collision models are `.bmd`s named `CLD_<map>`.

## The movies (VX)

20 files in `videos/`, **10 movies**, each a pair: `NAME_U.vx` for the
upper screen and `NAME_L.vx` for the lower. Actimagine's **VX** codec
(the program's `[SDK+Actimagine:VX]`; on screen at the boot, "video
codec"); `tools/vx.py build/extract/videos` reads them:

| Movie | Frames | Length | Sound (in `_U`) |
|---|---|---|---|
| TDL (the opening) | 608 | 50.7 s | none in either file |
| CBI | 193 | 16.1 s | 32 000 Hz |
| CBE | 529 | 44.1 s | 32 728 Hz |
| UFO | 374 | 31.2 s | 32 768 Hz |
| BRG | 552 | 46.0 s | 32 768 Hz |
| FYU | 380 | 31.7 s | 32 768 Hz |
| PAN | 325 | 27.1 s | 32 768 Hz |
| SWD | 401 | 33.4 s | 32 768 Hz |
| PRI | 343 | 28.6 s | 32 768 Hz |
| END (the ending) | 826 | 68.8 s | 32 768 Hz |

Every file is **256 × 192 at 12 frames a second** (16.16 fixed point:
0x000C0000). The header: `VXDS`, frames, width, height, rate, a
quantiser (28-31, *inferred*), the sound's sample rate, 2 where there is
sound, the largest frame (*inferred*), an offset into the data where
there is sound (*meaning unknown*), and a table of (frame, offset)
pairs at the file's end, here one pair: frame 0 at 0x30, where the
frames begin. The sound is the codec's own (not the SDK's STRM; the SDAT
has no streams).

`movielist.bvx`: 13 entries of 0x68 bytes, numbered 1-13, each a pair
of names; entries 5, 7 and 9 name `TDL_upper_vx80_audio.vx` and
`TDL_lower_vx80.vx`, which are not on the cartridge (left from a test,
*inferred*). Entry 1 (TDL, the silent one) has 0x33 in its second word
where the others have 0xFFFFFFFF: **sequence 51 is `SEQ_56FFTheme`**,
*inferred* the music played under the opening.

Moon's movies were Mobiclip, whose decoder the game copied to the ITCM
at run time (pc-moon's `--copy`). Here the decoder's core is **in the
ITCM's autoload** (`03-executables.md`): code the cartridge's image
places there at the boot, not copied by the game.

## Text

Latin-1 (French "données" as 0xE9; German, Italian and Spanish the same
way), one directory per language. `.btx` (110 files): a count, then
(id, offset) pairs, then the strings, each ending in two zero bytes (the
offsets from the strings' start, right after the pairs: `St_Ge_General.btx` begins "Melee", "Ranged",
"Flying", "Yes", "No", ...). `.brt` (`REPO`), `.btk`, `.bst`, `.bmw`, the
tables' names (`CHAR`, `ITEM`, `SKIL` per language) and the events' text
(`EventPackTxt.dpk`) are the rest; *inferred* the same Latin-1 strings
in their own tables.

## The game's tables and the airship's files

Each begins with a four-letter magic: `CHAR` (characters, per language),
`ITEM`, `SKIL`, `JOB`/`JOBL`, `FORM` (formations), `PATT` (patterns),
`CelL` (cell lists), `HOBJ` (the airship's institutions and objects),
`RECI` (recipes, composition), `REPO` (reports, the log book), `EZPL`
(the object list), `PTRL` (patrols), `KUZO` (sky pirates' lore,
*inferred* from `tradition.bku`); the airship's own `HSCD`
(conversations), `HSRD` (results), `HSEV` (events), `HSNP`/`HSNL`
(people and their lists), `HSGN`, `HSLD` (the shop's and the trade's
line-ups), `HSJD`, `HSAR`. The characters' cells (`.ADCE`, magic `CADP`)
go with a NARC of the same name. Routes (`.rte`, 93): `Route_<map>_w` and
`_f`, *inferred* walking and flying units' paths (the battle has flying
units: "Melee", "Ranged", "Flying").

## The sound

One SDAT, `sound/sound_data.sdat` (`python -m ndskit.sdat ... --list`,
`--waves`):

* **53 sequences**, named: `SEQ_01TitleDemo`, `SEQ_02Save`,
  `SEQ_08Field1`, `SEQ_09Battle1`, ..., `SEQ_28BossBattle1`-`4`,
  `SEQ_32LastBoss`, `SEQ_35WorldMap`, `SEQ_38VanTheme`, `SEQ_52MainTheme`,
  `SEQ_54StaffRoll`, `SEQ_56FFTheme`, `SEQ_57Main2`;
* **78 sequence archives** of effects (`SEQ_SE`, `SEQ_SE_PHYSIC`,
  `SEQ_SE_MAGIC` with 197, `SEQ_SE_HISSATU`, `SEQ_SE_EVENT1`, then one per
  event: `SEQ_SE_EV00201000`, ...), 130 banks, 130 wave archives, 74
  groups, **15 players** (`PLAYER_BGM` with a heap of 13 000 bytes, then
  system, battle, magic, event, "hissatsu" (special moves), death, foot,
  summon, level-up ... effects);
* **waves**: 2 152 IMA-ADPCM, 24 PCM16, 61 PCM8, at many rates (44 100
  to 44 108 Hz, 35 002, 30 000, 25 000, ...); **programs**: 2 450 PCM,
  566 key splits, **516 PSG and 74 noise** (4 482 PCM instruments in all).
  No streams.

`sound/sound_data.sadl` is the archive's symbols as C (`#define
PLAYER_BGM 0`, ...); `se_list.bse` a small table (*inferred*: the
effects' list).
