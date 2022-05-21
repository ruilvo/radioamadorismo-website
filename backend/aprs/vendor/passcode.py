"""
File related to APRS-IS passcodes
"""


def passcode_generator(callsign: str) -> int:
    """
    Uses the hashing algorithm to generate a passcode for a given callsign.
    From https://apps.magicbug.co.uk/passcode/
    """
    callsign_clean = callsign.split("-")[0].upper()
    callsign_bytes = callsign_clean.encode("ascii")

    result_hash = 0x73E2
    shift = True
    for char in callsign_bytes:
        if shift:
            result_hash ^= char << 8
        else:
            result_hash ^= char
        shift = not shift
    result_hash &= 0x7FFF

    return result_hash


if __name__ == "__main__":
    print(passcode_generator("N0C"))
    print(passcode_generator("N0CALL"))
