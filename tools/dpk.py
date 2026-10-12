"""Revenant Wings's packs (.dpk): members by id, some of them BIOS-compressed.

    python tools/dpk.py build/extract --list               # every pack: members, kinds
    python tools/dpk.py data/effect/EffectPack.dpk --list  # one pack (a path under build/extract or not)
    python tools/dpk.py build/extract --extract build/dpk  # every member, compressed ones undone

A pack is a count, then that many records of three words (an id, the
member's offset from the pack's start, its size), the members after the
table in the records' order, each padded to 16 bytes with 0xEE. Ids are
the game's own numbers, ascending (a font's index, an effect's, an event
script's: `EventPack.dpk` and each language's `EventPackTxt.dpk` share
theirs). A member is a file of its own: a NARC, an NFTR font, the SDK's
G2D files, the game's data, or one of those compressed with the BIOS's
LZ77 (its first byte 0x10), which --extract undoes into `.dec` files.
"""
import argparse
import collections
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ndskit import lz  # noqa: E402


def members(data):
    """[(id, offset, size)] of a pack; ValueError if data is not one."""
    if len(data) < 4:
        raise ValueError("too short")
    n = struct.unpack_from("<I", data)[0]
    if n == 0 or 4 + 12 * n > len(data):
        raise ValueError("no table")
    out = [struct.unpack_from("<III", data, 4 + 12 * i) for i in range(n)]
    for i, o, s in out:
        if o < 4 + 12 * n or o + s > len(data):
            raise ValueError("member %d out of the pack" % i)
    return out


def kind(blob):
    m = blob[:4]
    if len(m) == 4 and all(0x20 <= c < 0x7F for c in m):
        return m.decode()
    if lz.probe(blob):
        inner = lz.decompress(blob)[:4]
        if all(0x20 <= c < 0x7F for c in inner):
            return "lz10:" + inner.decode()
        return "lz10"
    return "data"


def packs(path):
    if os.path.isfile(path):
        yield path
        return
    for dp, _, fn in sorted(os.walk(path)):
        for f in sorted(fn):
            if f.lower().endswith(".dpk"):
                yield os.path.join(dp, f)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", help="a .dpk, or a directory to search for them")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--members", action="store_true", help="with --list: every member, not only the totals")
    ap.add_argument("--extract", metavar="DIR")
    a = ap.parse_args(argv)
    root = a.path if os.path.isdir(a.path) else os.path.dirname(a.path)
    total = 0
    for p in packs(a.path):
        data = open(p, "rb").read()
        ms = members(data)
        rel = os.path.relpath(p, root).replace("\\", "/")
        kinds = collections.Counter(kind(data[o:o + s]) for _, o, s in ms)
        total += len(ms)
        if a.list:
            print("%-50s %9d  %4d members, ids %d-%d  %s" % (
                rel, len(data), len(ms), ms[0][0], ms[-1][0],
                ", ".join("%s x%d" % kv for kv in kinds.most_common())))
            if a.members:
                for i, o, s in ms:
                    print("    %10d  %08X %8d  %s" % (i, o, s, kind(data[o:o + s])))
        if a.extract:
            d = os.path.join(a.extract, rel)
            os.makedirs(d, exist_ok=True)
            for i, o, s in ms:
                blob = data[o:o + s]
                with open(os.path.join(d, "%d.bin" % i), "wb") as f:
                    f.write(blob)
                if lz.probe(blob):
                    with open(os.path.join(d, "%d.dec" % i), "wb") as f:
                        f.write(lz.decompress(blob))
    print("%d members" % total)


if __name__ == "__main__":
    main()
