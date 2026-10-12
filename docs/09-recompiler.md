# The recompiler: Revenant Wings's programs to C++

ndskit's recompiler (`python -m ndskit.recomp`; pc-moon's, pc-nostalgia's
and pc-lufiacots's `09-recompiler.md`) turns both programs and the six
overlays into C++, one module each.

```sh
ROM="rom/Final Fantasy XII - Revenant Wings (Europe) (En,Fr,De,Es,It).nds"
export PATH=/c/msys64/mingw64/bin:$PATH
python -m ndskit.recomp "$ROM" --out build/recomp --optest           # about 2 minutes, most of it discovery
cmake -S build/recomp -B build/recomp/b -G Ninja -DCMAKE_CXX_COMPILER=clang++ && ninja -C build/recomp/b
python -m ndskit.recomp.selftest "$ROM" --cpu 9 --auto --out build/vectors/arm9.txt
python -m ndskit.recomp.selftest "$ROM" --cpu 7 --auto --out build/vectors/arm7.txt
python -m ndskit.recomp.selftest "$ROM" --cpu 9 --overlay 0 --auto --out build/vectors/ov0.txt
python -m ndskit.recomp.selftest "$ROM" --cpu 9 --overlay 2 --auto --out build/vectors/ov2.txt
V="build/recomp/selftest/optest9.txt build/recomp/selftest/optest7.txt build/vectors/arm9.txt build/vectors/arm7.txt build/vectors/ov0.txt build/vectors/ov2.txt"
build/recomp/b/selftest $V               # the recompiled code
build/recomp/b/selftest --interp $V      # the runtime's interpreter, on the same vectors
```

## What it makes

| Module | Functions | Instructions |
|---|---|---|
| ARM9 (the program, with what its overlays reach) | 3 610 | 112 199 |
| ARM9_OV0 (missions) | 2 623 | 96 208 |
| ARM9_OV1 (license board) | 290 | 8 098 |
| ARM9_OV2 (airship) | 1 595 | 82 554 |
| ARM9_OV3 (movies) | 95 | 4 474 |
| ARM9_OV4 (title) | 11 | 834 |
| ARM9_OV5 (preparations) | 273 | 17 822 |
| ARM7 | 942 | 37 273 |
| OPTEST9 / OPTEST7 (ndskit's instruction test) | 3 750 / 3 548 | 9 783 / 9 509 |

10 modules, 16 737 functions, 378 754 instructions, 64 files. The
recompiler takes 2 min 14 s (each overlay discovered twice, the second
time with the 275, 7, 58, 1 and 36 targets other overlays call in
overlays 0, 1, 2, 3 and 5); the build 1 min 9 s with clang 22, **no
warning**. **No function is left to the interpreter**: every discovered
function is emitted. The ITCM's overlapping entries (the VX decoder's
unrolled code, `03-executables.md`) are functions like the others.

## The self-test

The vectors are recorded by ndskit's interpreter (`armemu`) from the
functions that run alone, on their stack or with pointer arguments, and
replayed by the recompiled code and by the runtime's interpreter:

| Vectors | Functions | Vectors | Failures |
|---|---|---|---|
| ndskit's instruction test, ARM9 / ARM7 | 3 749 / 3 547 | 29 724 / 28 057 | 0 |
| the program (483 alone, 553 with pointers) | 1 036 | 16 330 | 0 |
| the ARM7 (89, 78) | 167 | 2 653 | 0 |
| overlay 0, loaded (562, 578) | 1 140 | 18 007 | 0 |
| overlay 2, loaded (390, 150) | 540 | 8 523 | 0 |
| **in all** | **10 179** | **103 294** | **0**, recompiled and `--interp` |

Nothing failed at the first run: the emitter needed nothing new for this
cartridge (almost all ARM, CodeWarrior's switches the earlier ports
already taught it).
