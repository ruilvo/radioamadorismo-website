def passcode_generator(callsign: str) -> int:
    callsign_clean = callsign.split("-")[0].upper()
    callsign_bytes = callsign_clean.encode("ascii")

    hash = 0x73E2

    i = 0
    while i < len(callsign_bytes):
        hash ^= callsign_bytes[i] << 8
        hash ^= callsign_bytes[i + 1]
        i += 2

    hash &= 0x7FFF

    return hash
