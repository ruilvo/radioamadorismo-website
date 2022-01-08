def passcode_generator(callsign: str) -> int:
    callsign_clean = callsign.split("-")[0].upper()
    callsign_bytes = callsign_clean.encode("ascii")

    hash = 0x73E2

    shift = True
    for c in callsign_bytes:
        if shift:
            hash ^= c << 8
        else:
            hash ^= c
        shift = not shift

    hash &= 0x7FFF

    return hash


if __name__ == "__main__":
    print(passcode_generator("N0C"))
    print(passcode_generator("N0CALL"))
