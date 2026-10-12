# Curiosities

Things found on the way that the port does not need.

* **The codec says hello**: Actimagine's "video codec" logo is one of
  the boot's screens, beside the Ivalice Alliance logo, and the codec
  signs the program as the SDK's own libraries do
  (`[SDK+Actimagine:VX]` next to `[SDK+NINTENDO:BACKUP]`).
* **Movies that were never shipped**: `movielist.bvx` names
  `TDL_upper_vx80_audio.vx` and `TDL_lower_vx80.vx` three times (entries
  5, 7 and 9); neither file is on the cartridge. *Inferred*: a test of
  the opening at another quality ("vx80") left in the list.
* **The opening is silent as a file**: TDL, the only movie without a
  sound track, has the sequence `SEQ_56FFTheme` (51) named in its list
  entry; the others carry their own 32 kHz sound.
* **One movie at 32 728 Hz**: CBE's sound is at 32 728 Hz, CBI's at
  32 000, the rest at 32 768.
* **A debug menu's text survives, without its letters**:
  `progtext/*/St_Bt_Debug.btx` holds 40 labels in every language, all
  question marks but "HP", "etc" and a few digits: Japanese text exported
  through Latin-1.
* **The sound archive's header file** ships beside it:
  `sound/sound_data.sadl` is C (`#define PLAYER_BGM 0`, `#define
  WAVE_BGM1 0`, ...) with Windows line ends (*inferred*: the SDK's sound
  tools' output).
* **Japanese in the names**: the sequences are `SEQ_33HikuteiFree1`
  (*hikūtei*, the airship), `SEQ_36Genjyunomori` (*genjū no mori*, the
  forest of phantom beasts), `SEQ_37Tenkujyo` (*tenkūjō*, the castle in
  the sky), `SEQ_44Nitijyo` (everyday life), `SEQ_47Warudakumi` (a
  plot), `SEQ_50Kanasii` (sad); the players `PLAYER_HISSATU_SE` (special
  moves), `PLAYER_EISYOU_SE` (chanting), `PLAYER_SYOUKAN_SE` (summoning),
  `PLAYER_HATUDOU_SE` (activation), `PLAYER_HANKO_SE`,
  `PLAYER_KEIKEN_SE` (experience); the program text
  `St_Tu_Kuuzoku.btx` (*kūzoku*, sky pirates); the battle's
  `senseki` (war record), `hane_yubi_icon` (a feather and a finger: the
  stylus's hint, the feather seen in the tutorial), `fukidashi` (speech
  balloons).
* **Floats on a machine without them**: the maps' records hold IEEE
  floats (`02-data-formats.md`), worked by CodeWarrior's software
  floating point.
* **Portraits twice**: `Illustration/full` and `full_2P` hold the same
  164 portraits' archives at nearly the same size (*inferred*: the
  second player's, mirrored, for the versus mode).
* **Four unused scenes**: `main` loads overlays for scenes 0 and 10-13
  but calls nothing for them (`03-executables.md`).
* **A semihosting console** is linked: three functions that call ARM's
  debugger through `swi 0x123456`, harmless on a DS that never calls
  them, and fatal-looking on one that did (the BIOS would read it as
  SWI 0x12).
