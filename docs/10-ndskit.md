# What this port gave ndskit

ndskit is the game-agnostic DS toolkit born with pc-moon, proven on
pc-nostalgia and hardened on pc-lufiacots. This port is its fourth game.
It is a git submodule at `ndskit/` (URL `../ndskit`, its own repository
beside this one); pc-moon, pc-nostalgia and pc-lufiacots take the same
repository.

The flow of a change: committed in this port's `ndskit/` ("ndskit: ...",
the kit's files only), checked on pc-moon (its build from the recompiler,
the self-test's 81 587 vectors both ways, its run of 466 VBlanks against
melonDS's state: 74 bytes of main RAM, its route into the first room),
pc-nostalgia (115 425 vectors both ways, its route into the first
dungeon with three changes of overlay, about 2 000 bytes of main RAM),
pc-lufiacots (137 231 vectors both ways, its title against melonDS's
state, its route into Soma Temple) and by discovery on six cartridges,
both CPUs, overlays included (Moon, Nostalgia, Lufia, this one, a 2010
cartridge with a compressed ARM9 and 366 overlays, a 2008 one mostly in
Thumb: no new conflict, no function lost or split, the lists diffed
before and after); then fast-forwarded into `D:\Homebrew6\ndskit` and
taken by the three other ports' submodules, each with a commit and its
`10-ndskit.md`. Nothing is pushed until this game is playable.

## Session 1

ndskit at **`5ee24af`** (as published on 2026-10-11), unchanged: this
cartridge asked nothing new of it so far. Everything the session did ran
on the kit as it is: `rom` (the header, both ModuleParams, the ARM7's
found by its shape on SDK 4.0 as on 4.1, 4.2 and 5.4, the six overlays,
2 140 files extracted, every FAT entry named), `sdat` (`--list`,
`--waves`: 53 sequences, 78 sequence archives, 2 237 waves, PSG and
noise programs), `lz` (the packs' LZ10 members), `arm` (`--refs`),
`recomp.discover` (0 conflicts on both CPUs and every overlay; 2 596 of
Ghidra's 2 607 functions as entries, the 11 others the C++ exception
runtime reached only through its tables), `melonds --overlays`,
`ghidra/ExportFuncs.java`.

What the kit may be asked for next (`06-attack-plan.md`): a `drag` in
`ndsrun --input` (the oracle has one; the game's orders are drags),
the window's lower screen as the large one, and whatever the VX movies'
sound and pacing need of the runtime's timing.
