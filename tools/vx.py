"""Revenant Wings's movies: the VX files' headers (Actimagine's codec) and the game's movie list.

    python tools/vx.py build/extract/videos            # every .vx's header, then movielist.bvx

A VX file ("VXDS") begins with eleven words after its magic, as read on
this cartridge's twenty files:

    0x04 frames                 0x18 sound's sample rate (0: no sound)
    0x08 width                  0x1C 2 where there is sound, else 0
    0x0C height                 0x20 the largest frame, in bytes (*inferred*)
    0x10 frame rate, 16.16      0x24 an offset into the data where there is sound, else 0
    0x14 a quantiser (*inferred*: 28-31 here)
    0x28 the offset of a table of (frame, offset) pairs at the file's end
    0x2C the number of those pairs (1 here: frame 0 at 0x30, where the data begins)

Each movie is a pair: the upper screen's file, with the sound, and the
lower screen's, without. `movielist.bvx` is a count and that many
entries of 0x68 bytes: a number (1, 2, ...), nine words, then the two
files' names in 32 bytes each.
"""
import argparse
import os
import struct

FIELDS = ("frames", "width", "height", "rate", "quant", "srate", "sound", "maxframe", "soundoff", "seek", "nseek")


def header(data):
    if data[:4] != b"VXDS":
        raise ValueError("not a VX file")
    h = dict(zip(FIELDS, struct.unpack_from("<11I", data, 4)))
    h["seektable"] = [struct.unpack_from("<II", data, h["seek"] + 8 * i) for i in range(h["nseek"])]
    return h


def movielist(data):
    n = struct.unpack_from("<I", data)[0]
    out = []
    for k in range(n):
        o = 4 + 0x68 * k
        words = struct.unpack_from("<10I", data, o)
        up = data[o + 0x28:o + 0x48].split(b"\0")[0].decode("latin1")
        lo = data[o + 0x48:o + 0x68].split(b"\0")[0].decode("latin1")
        out.append((words[0], up, lo, words[1:]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dir", help="the extracted videos/ directory")
    a = ap.parse_args(argv)
    names = sorted(f for f in os.listdir(a.dir) if f.lower().endswith(".vx"))
    for f in names:
        data = open(os.path.join(a.dir, f), "rb").read()
        h = header(data)
        fps = h["rate"] / 65536
        snd = "sound %d Hz" % h["srate"] if h["srate"] else "no sound"
        print("%-10s %8d bytes  %4d frames %dx%d at %g fps (%.1f s)  quant %d  %s  largest frame %d  seek %s" % (
            f, len(data), h["frames"], h["width"], h["height"], fps, h["frames"] / fps, h["quant"],
            snd, h["maxframe"], h["seektable"]))
    ml = os.path.join(a.dir, "movielist.bvx")
    if os.path.exists(ml):
        print("movielist.bvx:")
        for num, up, lo, words in movielist(open(ml, "rb").read()):
            have = all(os.path.exists(os.path.join(a.dir, x)) for x in (up, lo))
            print("  %2d  %-28s %-24s %s%s" % (num, up, lo, " ".join("%X" % w for w in words),
                                              "" if have else "  (not on the cartridge)"))


if __name__ == "__main__":
    main()
