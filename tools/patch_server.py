#!/usr/bin/env python3
"""Make electrs advertise NODE_BLAKE2B (service bit 28) in its P2P version message.  patch_server.py ELECTRS_DIR
Bitcoin Knots 29.4.3 and newer will not send blocks above 961,631 to a peer that does not advertise this bit, so
stock electrs stops following the chain without any error. The edit is anchored on the exact line; if upstream
changed it, the build stops instead of shipping an unpatched server."""
import os, sys

OLD = "let services = p2p::ServiceFlags::NONE;"
NEW = ("// NODE_BLAKE2B: this client understands the BLAKE2b header v2 blocks (bit 28 in Bitcoin Knots' protocol.h)\n"
       "    let services = p2p::ServiceFlags::from(1u64 << 28);")


def main():
    if len(sys.argv) != 2:
        print(__doc__); return 2
    path = os.path.join(sys.argv[1], "src/p2p.rs")
    s = open(path, encoding="utf-8").read()
    if "1u64 << 28" in s:
        print("OK  already patched"); return 0
    if s.count(OLD) != 1:
        print("FAIL src/p2p.rs: expected exactly one %r" % OLD); return 2
    open(path, "w", encoding="utf-8").write(s.replace(OLD, NEW))
    print("OK  electrs now advertises NODE_BLAKE2B")
    return 0


if __name__ == "__main__":
    sys.exit(main())
