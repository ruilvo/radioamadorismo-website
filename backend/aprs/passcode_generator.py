def passcode_generator(callsign: str) -> int:
    callsign_clean = callsign.split("-")[0].upper()
    callsign_bytes = callsign_clean.encode("ascii")

    chash = 0x73E2

    shift = True
    for c in callsign_bytes:
        if shift:
            chash ^= c << 8
        else:
            chash ^= c
        shift = not shift

    chash &= 0x7FFF

    return chash


if __name__ == "__main__":
    print(passcode_generator("N0C"))
    print(passcode_generator("N0CALL"))
